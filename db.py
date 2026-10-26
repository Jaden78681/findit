"""
FindIt - database layer (storage + app rules)

This file has NO screens. It only:
  1) creates the database tables
  2) holds every "action" (save_item, claim_item, pick_up, spot_check, add_alert, ...)

app.py (the screens) calls these functions.
Keeping rules here and screens in app.py makes both easier to read and test.

Errors and messages are saved as a KEY + details (e.g. "msg_picked_up"),
and lang.py turns them into English or Spanish on the screen.
"""

import json
import os
import random
import sqlite3
from datetime import date, datetime, timedelta

# ---------------------------------------------------------------------------
# Settings (the numbers Jaden picked in the blueprint)
# ---------------------------------------------------------------------------

DB_PATH = os.environ.get("FINDIT_DB", "findit.db")

CATEGORIES = ["Water Bottle", "Clothing", "Book", "Sports Gear",
              "School Supplies", "Bag", "Electronics", "Other"]

# ---------------------------------------------------------------------------
# School map: Round Rock High School, 201 Deep Wood Dr, Round Rock, TX
# Map center from public records: 30.509218, -97.695553
#
# ⚠️ Building positions below are APPROXIMATE starting points.
#    Open the Map screen → "Map setup", click a building on the satellite
#    view to read its exact lat/lon, then paste the numbers here.
# ---------------------------------------------------------------------------

SCHOOL_NAME = "Round Rock High School"
MAP_CENTER = (30.509218, -97.695553)
MAP_ZOOM = 17

# Where items can be FOUND: name -> (number, lat, lon)
LOCATIONS = {
    "Main Building": ("B1", 30.50922, -97.69560),
    "Library":       ("B2", 30.50940, -97.69600),
    "Cafeteria":     ("B3", 30.50950, -97.69520),
    "Gym":           ("B4", 30.51000, -97.69470),
    "Tennis Courts": ("B5", 30.50830, -97.69380),
    "Field":         ("B6", 30.51060, -97.69330),
}

# XP rules
XP_REPORT = 10          # reported an item
XP_DETAIL = 5           # wrote a detailed description
XP_VALUABLE = 15        # turned a valuable in at a Lost & Found desk
XP_RETURN_BONUS = 30    # item really went home
DETAIL_MIN_CHARS = 20   # description this long = "detailed"

# Levels. Level is calculated from XP, never saved.
LEVELS = [(0, "New Finder"), (50, "Finder"), (150, "Super Finder"), (300, "Finder Hero"), (500, "FindIt Legend")]

# Log in (DEMO): every account uses this password for now.
# A real version would save a hashed password per user and send reset emails.
DEMO_PASSWORD = "1212"

DAILY_REPORT_LIMIT = 5   # max reports per person per day
CLAIM_EXPIRE_DAYS = 7    # a valuable nobody picked up at the desk goes back to Found
MOVE_TO_DESK_DAYS = 3    # a left-behind item this old: ask people to take it to a desk
REUSE_AFTER_DAYS = 30    # ⚠️ TENTATIVE: not picked up in 30 days -> school reuse/donation box
                         #    (to be confirmed with the school's Lost & Found policy)
TOP_FINDER_DAYS = 7      # "This week's Top Finders" looks at the last 7 days
SCHOOL_GOAL = 100        # School Return Challenge goal

# Lost & Found desks. Normal items stay where they were found;
# VALUABLES (phone, wallet, keys…) are turned in at one of these desks.
# name -> (number, lat, lon)   (approximate, see above)
RETURN_SPOT_INFO = {
    "Front Office":       ("R1", 30.50895, -97.69560),
    "Library Desk":       ("R2", 30.50935, -97.69615),
    "Gym Office":         ("R3", 30.50985, -97.69455),
    "Counselor's Office": ("R4", 30.50915, -97.69530),
}
RETURN_SPOTS = list(RETURN_SPOT_INFO)

STATUSES = ["Found", "Claimed", "Returned", "Reuse"]


def spot_label(name):
    """e.g. 'R1 Front Office'"""
    return f"{RETURN_SPOT_INFO[name][0]} {name}" if name in RETURN_SPOT_INFO else name


def place_label(name):
    """e.g. 'B5 Tennis Courts'"""
    return f"{LOCATIONS[name][0]} {name}" if name in LOCATIONS else name


# Badge names (descriptions live in lang.py)
BADGES = ["Water Bottle Hunter", "Book Finder", "Sports Finder", "Return Hero"]   # special badges (levels are separate)


class RuleError(ValueError):
    """A rule was broken. args = (key, details) so the screen can show it in any language."""

    def __init__(self, key, **details):
        super().__init__(key, details)
        self.key, self.details = key, details


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # lets us use row["column_name"]
    return conn


def init_db():
    """Create the tables if they do not exist yet."""
    with connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname     TEXT UNIQUE NOT NULL,
            email        TEXT,                 -- school email, only for "forgot password" (coming later)
            joined_date  TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS items (
            item_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            photo        BLOB,                 -- photo saved inside the DB
            category     TEXT NOT NULL,
            description  TEXT NOT NULL,
            location     TEXT NOT NULL,        -- where it was found
            date_found   TEXT NOT NULL,
            status       TEXT NOT NULL DEFAULT 'Found',   -- Found / Claimed / Returned / Reuse
            found_by     TEXT NOT NULL,        -- finder nickname
            claimed_by   TEXT,                 -- owner nickname ("It's mine!")
            valuable     INTEGER DEFAULT 0,    -- 1 = phone, wallet, keys… (turned in at a desk)
            kept_at      TEXT,                 -- Lost & Found desk (NULL = left where found)
            map_x        REAL,                 -- pin longitude
            map_y        REAL,                 -- pin latitude
            claimed_at   TEXT,                 -- for the 7-day reset
            returned_at  TEXT,                 -- for the weekly chart + Top Finders
            reused_at    TEXT,                 -- went to the reuse/donation box
            created_at   TEXT NOT NULL         -- for the 5-per-day limit
        );

        CREATE TABLE IF NOT EXISTS user_badges (
            user_id      INTEGER NOT NULL,
            badge        TEXT NOT NULL,
            date_earned  TEXT NOT NULL,
            UNIQUE (user_id, badge)
        );

        -- In-app messages (no phone numbers, no emails). text = message key + details (JSON)
        CREATE TABLE IF NOT EXISTS messages (
            message_id  INTEGER PRIMARY KEY AUTOINCREMENT,
            to_user     TEXT NOT NULL,
            item_id     INTEGER,
            text        TEXT NOT NULL,
            created_at  TEXT NOT NULL,
            is_read     INTEGER DEFAULT 0
        );

        -- "Still there" / "Not there anymore" taps from people walking by
        CREATE TABLE IF NOT EXISTS spot_checks (
            check_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id      INTEGER NOT NULL,
            nickname     TEXT NOT NULL,
            still_there  INTEGER NOT NULL,     -- 1 = still there, 0 = not there anymore
            created_at   TEXT NOT NULL
        );

        -- "I lost something": get a message when a matching item is posted
        CREATE TABLE IF NOT EXISTS lost_alerts (
            alert_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname    TEXT NOT NULL,
            words       TEXT NOT NULL,         -- e.g. "blue bottle"
            category    TEXT NOT NULL DEFAULT 'All',
            created_at  TEXT NOT NULL
        );
        """)
        # Older findit.db files: add the new columns so they still open
        existing = {row["name"] for row in conn.execute("PRAGMA table_info(items)")}
        for column, kind in (("kept_at", "TEXT"), ("valuable", "INTEGER DEFAULT 0"), ("reused_at", "TEXT")):
            if column not in existing:
                conn.execute(f"ALTER TABLE items ADD COLUMN {column} {kind}")
        if "email" not in {row["name"] for row in conn.execute("PRAGMA table_info(users)")}:
            conn.execute("ALTER TABLE users ADD COLUMN email TEXT")


def _now(now=None):
    return (now or datetime.now()).isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# Messages
# ---------------------------------------------------------------------------

def item_ref(item):
    """What a message needs to name an item in any language."""
    return {"cat": item["category"], "id": item["item_id"]}


def send_message(to_user, item_id, key, now=None, **details):
    text = json.dumps({"key": key, **details})
    with connect() as conn:
        conn.execute("INSERT INTO messages (to_user, item_id, text, created_at) VALUES (?, ?, ?, ?)",
                     (to_user, item_id, text, _now(now)))


def message_parts(message):
    """(key, details) of a saved message."""
    try:
        data = json.loads(message["text"])
        return data.pop("key"), data
    except (ValueError, KeyError, TypeError):
        return "raw", {"text": message["text"]}


def get_messages(nickname):
    with connect() as conn:
        return conn.execute("SELECT * FROM messages WHERE to_user = ? ORDER BY message_id DESC",
                            (nickname,)).fetchall()


def count_unread(nickname):
    with connect() as conn:
        return conn.execute("SELECT COUNT(*) FROM messages WHERE to_user = ? AND is_read = 0",
                            (nickname,)).fetchone()[0]


def mark_read(nickname):
    with connect() as conn:
        conn.execute("UPDATE messages SET is_read = 1 WHERE to_user = ?", (nickname,))


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

def get_or_create_user(nickname):
    """Used by seed.py and the tests to make demo accounts."""
    nickname = nickname.strip()
    with connect() as conn:
        row = conn.execute("SELECT * FROM users WHERE nickname = ?", (nickname,)).fetchone()
        if row:
            return row
        conn.execute("INSERT INTO users (nickname, joined_date) VALUES (?, ?)",
                     (nickname, date.today().isoformat()))
        return conn.execute("SELECT * FROM users WHERE nickname = ?", (nickname,)).fetchone()


def get_user(nickname):
    with connect() as conn:
        return conn.execute("SELECT * FROM users WHERE nickname = ?", (nickname.strip(),)).fetchone()


def log_in(nickname, password):
    """Returns the nickname if the account exists and the password is right."""
    nickname = nickname.strip()
    if not nickname or not password:
        raise RuleError("err_login_empty")
    user = get_user(nickname)
    if user is None:
        raise RuleError("err_no_account")
    if password != DEMO_PASSWORD:
        raise RuleError("err_wrong_password")
    return user["nickname"]


def sign_up(nickname, email, password, confirm):
    """Make a new account. Nickname only: no real names. (DEMO: the password is always 1212.)"""
    nickname, email = nickname.strip(), email.strip()
    if not (3 <= len(nickname) <= 20) or not nickname.replace("_", "").isalnum():
        raise RuleError("err_bad_nickname")
    if get_user(nickname) is not None:
        raise RuleError("err_nickname_taken")
    if "@" not in email or "." not in email.split("@")[-1]:
        raise RuleError("err_bad_email")
    if not password or password != confirm:
        raise RuleError("err_password_match")
    with connect() as conn:
        conn.execute("INSERT INTO users (nickname, email, joined_date) VALUES (?, ?, ?)",
                     (nickname, email, date.today().isoformat()))
    return nickname


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def is_detailed(description):
    return len(description.strip()) >= DETAIL_MIN_CHARS


def count_today_reports(nickname):
    today = date.today().isoformat()
    with connect() as conn:
        row = conn.execute(
            "SELECT COUNT(*) FROM items WHERE found_by = ? AND substr(created_at, 1, 10) = ?",
            (nickname, today)).fetchone()
        return row[0]


def random_point_in(location):
    """Pick a pin spot a few meters around the location, so pins don't stack.
    Returns (map_x, map_y) = (longitude, latitude)."""
    _, lat, lon = LOCATIONS[location]
    return (round(lon + random.uniform(-0.00012, 0.00012), 6),
            round(lat + random.uniform(-0.00008, 0.00008), 6))


def pin_position(item):
    """(lat, lon) of an item's pin."""
    x, y = item["map_x"], item["map_y"]
    if x is not None and y is not None and -180 <= x < 0 and 0 < y <= 90:
        return y, x
    _, lat, lon = LOCATIONS.get(item["location"], ("", *MAP_CENTER))
    return lat, lon


def map_position(item):
    """Where to put the pin NOW: at the Lost & Found desk if the item is kept there,
    otherwise where it was found."""
    if item["kept_at"] in RETURN_SPOT_INFO and item["status"] in ("Found", "Claimed"):
        _, lat, lon = RETURN_SPOT_INFO[item["kept_at"]]
        k = item["item_id"] % 6                      # small spread so pins don't stack
        return lat + (k // 3 - 0.5) * 0.00004, lon + (k % 3 - 1) * 0.00005
    return pin_position(item)


def save_item(found_by, category, description, location, date_found,
              photo_bytes=None, created_at=None, valuable=False, kept_at=None):
    """Save a new found item with status Found. Returns the new item_id.

    Normal items: leave it where you found it (kept_at = None).
    Valuables:    turn it in at a Lost & Found desk (kept_at = desk name).
    No question/answer step: the owner just says "It's mine!" and picks it up.
    Anyone with a matching "I lost something" alert gets a message."""
    if not description.strip():
        raise RuleError("err_no_description")
    if location not in LOCATIONS:
        raise RuleError("err_no_location")
    if valuable and kept_at not in RETURN_SPOTS:
        raise RuleError("err_no_desk")
    if not valuable:
        kept_at = None
    if count_today_reports(found_by) >= DAILY_REPORT_LIMIT:
        raise RuleError("err_daily_limit", limit=DAILY_REPORT_LIMIT)

    x, y = random_point_in(location)
    created_at = created_at or _now()
    with connect() as conn:
        cur = conn.execute("""
            INSERT INTO items (photo, category, description, location, date_found, found_by,
                               map_x, map_y, created_at, valuable, kept_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (photo_bytes, category, description.strip(), location, str(date_found), found_by,
             x, y, created_at, 1 if valuable else 0, kept_at))
        item_id = cur.lastrowid
    _notify_alerts(get_item(item_id))
    return item_id


# ---------------------------------------------------------------------------
# Search / read
# ---------------------------------------------------------------------------

def get_item(item_id):
    with connect() as conn:
        return conn.execute("SELECT * FROM items WHERE item_id = ?", (item_id,)).fetchone()


def search_items(keyword="", category="All", location="All", status="All", days=None):
    """Find items. Keywords are matched word by word ("blue bottle" finds "Blue water bottle"),
    and the best matches come first. days = only items found in the last N days."""
    sql = "SELECT * FROM items WHERE 1=1"
    params = []
    if category != "All":
        sql += " AND category = ?"
        params.append(category)
    if location != "All":
        sql += " AND location = ?"
        params.append(location)
    if status != "All":
        sql += " AND status = ?"
        params.append(status)
    if days:
        sql += " AND date_found >= ?"
        params.append((date.today() - timedelta(days=days)).isoformat())
    sql += " ORDER BY date_found DESC, item_id DESC"
    with connect() as conn:
        rows = conn.execute(sql, params).fetchall()
    words = _words(keyword)
    if not words:
        return rows
    scored = [(match_score(i, words), i) for i in rows]
    scored = [(sc, i) for sc, i in scored if sc > 0]
    scored.sort(key=lambda pair: -pair[0])          # stable: newest first among equal scores
    return [i for _, i in scored]


def match_score(item, words):
    """How many of the search words appear in the item's description or type."""
    text = f"{item['description']} {item['category']}".lower()
    return sum(1 for w in words if w in text)


def recent_items(limit=6):
    with connect() as conn:
        return conn.execute(
            "SELECT * FROM items WHERE status IN ('Found', 'Claimed') ORDER BY created_at DESC LIMIT ?",
            (limit,)).fetchall()


def days_waiting(item, now=None):
    created = datetime.fromisoformat(item["created_at"])
    return ((now or datetime.now()) - created).days


# ---------------------------------------------------------------------------
# "It's mine!" -> pick up   (no question/answer step)
#   Normal item : the owner grabs it where it was left -> Returned right away
#   Valuable    : "It's mine!" -> Claimed (go to the desk; staff hand it over in person)
#                 -> "I picked it up" -> Returned
# ---------------------------------------------------------------------------

def _mark_returned(item, owner, now):
    with connect() as conn:
        conn.execute("""UPDATE items SET status = 'Returned', claimed_by = ?,
                        claimed_at = COALESCE(claimed_at, ?), returned_at = ? WHERE item_id = ?""",
                     (owner, _now(now), _now(now), item["item_id"]))
    send_message(item["found_by"], item["item_id"], "msg_picked_up", now, owner=owner, **item_ref(item))
    return give_badges(item["found_by"])


def _check_pair_limit(item, nickname, now):
    """Fair play: one person can take home at most ONE item from the same finder per day.
    Stops two friends from farming XP by posting and "picking up" fake items."""
    day = now.date().isoformat()
    with connect() as conn:
        used = conn.execute("""
            SELECT COUNT(*) FROM items WHERE found_by = ? AND claimed_by = ?
            AND substr(claimed_at, 1, 10) = ?""", (item["found_by"], nickname, day)).fetchone()[0]
    if used:
        raise RuleError("err_pair_limit", finder=item["found_by"])


def claim_item(item_id, nickname, now=None):
    """The owner taps "It's mine!".
    Normal item -> it is Returned right away (they picked it up where it was left).
    Valuable    -> it becomes Claimed and the owner gets a message saying which desk to go to.
    Returns the list of new badges the finder earned (empty for valuables)."""
    item = get_item(item_id)
    if item is None:
        raise RuleError("err_no_item")
    if nickname == item["found_by"]:
        raise RuleError("err_own_item")
    if item["status"] in ("Returned", "Reuse"):
        raise RuleError("err_already_home")
    if item["status"] == "Claimed":
        if nickname == item["claimed_by"]:
            raise RuleError("err_already_yours")
        raise RuleError("err_someone_else")
    now = now or datetime.now()
    _check_pair_limit(item, nickname, now)
    if not item["valuable"]:
        return _mark_returned(item, nickname, now)
    with connect() as conn:
        conn.execute("UPDATE items SET status = 'Claimed', claimed_by = ?, claimed_at = ? WHERE item_id = ?",
                     (nickname, _now(now), item_id))
    send_message(nickname, item_id, "msg_go_to_desk", now, desk=spot_label(item["kept_at"]), **item_ref(item))
    send_message(item["found_by"], item_id, "msg_owner_coming", now,
                 owner=nickname, desk=spot_label(item["kept_at"]), **item_ref(item))
    return []


def pick_up(item_id, nickname, now=None):
    """Valuable: the owner got it at the desk. Returns new badges for the finder."""
    item = get_item(item_id)
    if item is None:
        raise RuleError("err_no_item")
    if item["status"] != "Claimed":
        raise RuleError("err_tap_mine_first")
    if nickname != item["claimed_by"]:
        raise RuleError("err_someone_else")
    return _mark_returned(item, nickname, now or datetime.now())


def reset_old_claims(now=None):
    """A valuable nobody picked up at the desk in 7 days goes back to Found."""
    now = now or datetime.now()
    cutoff = (now - timedelta(days=CLAIM_EXPIRE_DAYS)).isoformat(timespec="seconds")
    with connect() as conn:
        cur = conn.execute("""
            UPDATE items SET status = 'Found', claimed_by = NULL, claimed_at = NULL
            WHERE status = 'Claimed' AND claimed_at < ?""", (cutoff,))
        return cur.rowcount


# ---------------------------------------------------------------------------
# "Still there?" — people walking by keep the info fresh
# ---------------------------------------------------------------------------

def spot_check(item_id, nickname, still_there, now=None):
    """Someone walked by: is the item still where it was left?"""
    item = get_item(item_id)
    if item is None:
        raise RuleError("err_no_item")
    if item["status"] != "Found" or item["kept_at"]:
        raise RuleError("err_no_check_needed")
    with connect() as conn:
        conn.execute("INSERT INTO spot_checks (item_id, nickname, still_there, created_at) VALUES (?, ?, ?, ?)",
                     (item_id, nickname, 1 if still_there else 0, _now(now)))
    if not still_there and nickname != item["found_by"]:
        send_message(item["found_by"], item_id, "msg_gone", now,
                     who=nickname, place=place_label(item["location"]), **item_ref(item))


def last_check(item_id):
    """The newest "still there / not there" tap, or None."""
    with connect() as conn:
        return conn.execute("SELECT * FROM spot_checks WHERE item_id = ? ORDER BY check_id DESC LIMIT 1",
                            (item_id,)).fetchone()


def move_to_desk(item_id, nickname, desk, now=None):
    """An item was left behind for a while: someone takes it to a Lost & Found desk."""
    item = get_item(item_id)
    if item is None:
        raise RuleError("err_no_item")
    if item["status"] != "Found" or item["kept_at"]:
        raise RuleError("err_no_check_needed")
    if desk not in RETURN_SPOTS:
        raise RuleError("err_no_desk")
    with connect() as conn:
        conn.execute("UPDATE items SET kept_at = ? WHERE item_id = ?", (desk, item_id))
    if nickname != item["found_by"]:
        send_message(item["found_by"], item_id, "msg_moved", now,
                     who=nickname, desk=spot_label(desk), **item_ref(item))


def needs_desk(item, now=None):
    """True if a left-behind item has waited long enough that it should go to a desk."""
    return item["status"] == "Found" and not item["kept_at"] and days_waiting(item, now) >= MOVE_TO_DESK_DAYS


# ---------------------------------------------------------------------------
# "I lost something" alerts
# ---------------------------------------------------------------------------

def _words(text):
    return [w for w in text.lower().replace(",", " ").split() if len(w) >= 2]


def _matches(item, words, category):
    if category != "All" and item["category"] != category:
        return False
    text = f"{item['description']} {item['category']}".lower()
    return all(w in text for w in _words(words))


def add_alert(nickname, words, category="All", now=None):
    """Save an alert. Returns the items ALREADY posted that match it."""
    if not _words(words):
        raise RuleError("err_alert_words")
    with connect() as conn:
        conn.execute("INSERT INTO lost_alerts (nickname, words, category, created_at) VALUES (?, ?, ?, ?)",
                     (nickname, words.strip(), category, _now(now)))
    return alert_matches(words, category, nickname)


def alert_matches(words, category="All", nickname=None):
    with connect() as conn:
        rows = conn.execute("SELECT * FROM items WHERE status = 'Found' ORDER BY created_at DESC").fetchall()
    return [i for i in rows if _matches(i, words, category) and i["found_by"] != nickname]


def my_alerts(nickname):
    with connect() as conn:
        return conn.execute("SELECT * FROM lost_alerts WHERE nickname = ? ORDER BY alert_id DESC",
                            (nickname,)).fetchall()


def delete_alert(alert_id, nickname):
    with connect() as conn:
        conn.execute("DELETE FROM lost_alerts WHERE alert_id = ? AND nickname = ?", (alert_id, nickname))


def _notify_alerts(item):
    with connect() as conn:
        alerts = conn.execute("SELECT * FROM lost_alerts WHERE nickname != ?", (item["found_by"],)).fetchall()
    told = set()
    for a in alerts:
        if a["nickname"] not in told and _matches(item, a["words"], a["category"]):
            send_message(a["nickname"], item["item_id"], "msg_alert_match", None,
                         words=a["words"], place=place_label(item["location"]), **item_ref(item))
            told.add(a["nickname"])


# ---------------------------------------------------------------------------
# Reuse  (⚠️ TENTATIVE rule — check with the school's Lost & Found policy)
# ---------------------------------------------------------------------------

def move_old_to_reuse(now=None):
    """Normal items nobody picked up in REUSE_AFTER_DAYS go to the school reuse/donation box.
    Valuables are never donated: they stay at the desk."""
    now = now or datetime.now()
    cutoff = (now - timedelta(days=REUSE_AFTER_DAYS)).isoformat(timespec="seconds")
    with connect() as conn:
        old = conn.execute("""SELECT * FROM items WHERE status = 'Found' AND valuable = 0
                              AND created_at < ?""", (cutoff,)).fetchall()
        conn.execute("""UPDATE items SET status = 'Reuse', reused_at = ?
                        WHERE status = 'Found' AND valuable = 0 AND created_at < ?""", (_now(now), cutoff))
    for item in old:
        send_message(item["found_by"], item["item_id"], "msg_reuse", now,
                     days=REUSE_AFTER_DAYS, **item_ref(item))
    return len(old)


# ---------------------------------------------------------------------------
# XP, level, badges  (report XP is "pending" until the item goes home)
# ---------------------------------------------------------------------------

def item_xp(item):
    """XP one item is worth to its finder right now."""
    xp = XP_REPORT + (XP_DETAIL if is_detailed(item["description"]) else 0)
    if item["valuable"]:
        xp += XP_VALUABLE
    if item["status"] == "Returned":
        xp += XP_RETURN_BONUS
    return xp


def calc_xp(nickname):
    """Returns (confirmed_xp, pending_xp).
    Returned items: all XP is real. Reuse items: the report XP becomes real (no return bonus)."""
    with connect() as conn:
        items = conn.execute("SELECT * FROM items WHERE found_by = ?", (nickname,)).fetchall()
    confirmed = sum(item_xp(i) for i in items if i["status"] in ("Returned", "Reuse"))
    pending = sum(item_xp(i) for i in items if i["status"] in ("Found", "Claimed"))
    return confirmed, pending


def level_number(xp):
    """1 to 5: which step of the level ladder this XP reaches."""
    return sum(1 for needed, _ in LEVELS if xp >= needed)


def calc_level(xp):
    """Returns (level_name, next_level_xp or None at the top)."""
    name, next_xp = LEVELS[0][1], None
    for i, (needed, level_name) in enumerate(LEVELS):
        if xp >= needed:
            name = level_name
            next_xp = LEVELS[i + 1][0] if i + 1 < len(LEVELS) else None
    return name, next_xp


def give_badges(nickname):
    """Check badge rules for this finder and save any new ones."""
    with connect() as conn:
        returned = conn.execute(
            "SELECT * FROM items WHERE found_by = ? AND status = 'Returned'", (nickname,)).fetchall()
    confirmed_xp, _ = calc_xp(nickname)

    earned = []
    if sum(1 for i in returned if i["category"] == "Water Bottle") >= 5:
        earned.append("Water Bottle Hunter")
    if any(i["category"] == "Book" for i in returned):
        earned.append("Book Finder")
    if any(i["category"] == "Sports Gear" or i["location"] == "Tennis Courts" for i in returned):
        earned.append("Sports Finder")
    if len(returned) >= 5:
        earned.append("Return Hero")

    user = get_or_create_user(nickname)
    new_badges = []
    with connect() as conn:
        for badge in earned:
            cur = conn.execute(
                "INSERT OR IGNORE INTO user_badges (user_id, badge, date_earned) VALUES (?, ?, ?)",
                (user["user_id"], badge, date.today().isoformat()))
            if cur.rowcount:
                new_badges.append(badge)
    return new_badges


def get_badges(nickname):
    user = get_or_create_user(nickname)
    with connect() as conn:
        rows = conn.execute("SELECT badge FROM user_badges WHERE user_id = ?",
                            (user["user_id"],)).fetchall()
    return [r["badge"] for r in rows]


def top_finders(limit=5, now=None):
    """This week's Top Finders: XP earned from items that went home in the last 7 days.
    Returns [(nickname, xp, items_returned), ...] best first. Nicknames only."""
    now = now or datetime.now()
    since = (now - timedelta(days=TOP_FINDER_DAYS)).isoformat(timespec="seconds")
    with connect() as conn:
        rows = conn.execute("SELECT * FROM items WHERE status = 'Returned' AND returned_at >= ?",
                            (since,)).fetchall()
    board = {}
    for i in rows:
        xp, n = board.get(i["found_by"], (0, 0))
        board[i["found_by"]] = (xp + item_xp(i), n + 1)
    ranked = sorted(board.items(), key=lambda kv: (-kv[1][0], kv[0]))
    return [(name, xp, n) for name, (xp, n) in ranked[:limit]]


# ---------------------------------------------------------------------------
# My activity + Impact
# ---------------------------------------------------------------------------

def my_activity(nickname):
    with connect() as conn:
        reported = conn.execute(
            "SELECT * FROM items WHERE found_by = ? ORDER BY created_at DESC", (nickname,)).fetchall()
        my_items = conn.execute(
            "SELECT * FROM items WHERE claimed_by = ? ORDER BY created_at DESC", (nickname,)).fetchall()
    return {"reported": reported, "my_items": my_items}


def get_stats(weeks=6):
    with connect() as conn:
        rows = conn.execute("SELECT status, returned_at FROM items").fetchall()
    count = {s: sum(1 for r in rows if r["status"] == s) for s in STATUSES}
    week_ago = (datetime.now() - timedelta(days=7)).isoformat(timespec="seconds")
    this_week = sum(1 for r in rows if r["status"] == "Returned" and (r["returned_at"] or "") >= week_ago)
    reported = len(rows)

    # Returned items per week, for the last few weeks (oldest first)
    start_of_this_week = date.today() - timedelta(days=date.today().weekday())
    weekly = []
    for w in range(weeks - 1, -1, -1):
        start = start_of_this_week - timedelta(weeks=w)
        end = start + timedelta(days=7)
        n = sum(1 for r in rows if r["returned_at"]
                and start.isoformat() <= r["returned_at"][:10] < end.isoformat())
        weekly.append((start.strftime("%m/%d"), n))

    return {
        "reported": reported,
        "claimed": count["Claimed"],
        "returned": count["Returned"],
        "waiting": count["Found"],
        "reused": count["Reuse"],
        "this_week": this_week,
        "return_rate": round(100 * count["Returned"] / reported) if reported else 0,
        "weekly": weekly,
    }
