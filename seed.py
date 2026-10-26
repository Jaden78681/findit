"""
FindIt - demo data, so the app can be tried right away.

Run:  python seed.py
WARNING: this deletes findit.db and starts fresh with sample items.
"""

import io
import os
import random
from datetime import date, datetime, timedelta

from PIL import Image, ImageDraw

import db

random.seed(7)

COLORS = {
    "Water Bottle": "#4C8BF5", "Clothing": "#3A3A3A", "Book": "#B5523B",
    "Sports Gear": "#E9C46A", "School Supplies": "#7A5CC2", "Bag": "#2A9D8F",
    "Electronics": "#5A6270", "Other": "#E8833A",
}


COLOR_WORDS = {"blue": "#4C8BF5", "black": "#2B2B2B", "pink": "#F28DB2", "clear": "#BFE3F2",
               "green": "#3FA34D", "red": "#D64545", "gray": "#9AA0A6", "yellow": "#E9C46A",
               "navy": "#1F2F5C", "white": "#EDEDED", "silver": "#C0C4CA"}


PHOTO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "photos")


def real_photo(key):
    """Use a real photo from the photos folder if there is one (e.g. photos/A.jpg, photos/07.png)."""
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG"):
        path = os.path.join(PHOTO_DIR, key + ext)
        if os.path.exists(path):
            img = Image.open(path).convert("RGB")
            img.thumbnail((800, 800))
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=85)
            return buffer.getvalue()
    return None


def photo(key, category, description):
    """Real photo if you added one, otherwise a simple drawing."""
    return real_photo(key) or fake_photo(category, description)


def fake_photo(category, description=""):
    """Draw a simple picture so demo items have photos."""
    img = Image.new("RGB", (480, 360), "#F3EFE6")
    d = ImageDraw.Draw(img)
    color = COLORS[category]
    for word, hex_color in COLOR_WORDS.items():   # use the color named in the description
        if word in description.lower():
            color = hex_color
            break
    if category == "Water Bottle":
        d.rounded_rectangle((200, 60, 280, 320), radius=30, fill=color)
        d.rectangle((215, 30, 265, 70), fill="#16213E")
    elif category == "Book":
        d.rectangle((150, 70, 330, 300), fill=color)
        d.rectangle((165, 70, 175, 300), fill="#FBF8F1")
    elif category == "Sports Gear":
        d.ellipse((170, 110, 310, 250), fill=color)
        d.arc((170, 110, 310, 250), 300, 60, fill="#FBF8F1", width=8)
    elif category == "Clothing":
        d.polygon([(160, 90), (320, 90), (370, 150), (330, 170), (320, 300),
                   (160, 300), (150, 170), (110, 150)], fill=color)
    elif category == "Bag":
        d.rounded_rectangle((150, 120, 330, 300), radius=24, fill=color)
        d.arc((190, 60, 290, 170), 180, 360, fill=color, width=14)
    else:
        d.rounded_rectangle((160, 100, 320, 260), radius=20, fill=color)
    d.text((16, 330), category, fill="#16213E")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=80)
    return buffer.getvalue()


# (category, description, location, valuable)
# Normal items stay where they were found. Valuables are turned in at a Lost & Found desk.
SAMPLES = [
    ("Water Bottle", "Blue water bottle with a tennis ball sticker", "Tennis Courts", False),
    ("Water Bottle", "Black metal bottle with a silver cap", "Gym", False),
    ("Water Bottle", "Pink bottle with flower stickers", "Field", False),
    ("Water Bottle", "Clear plastic bottle with a straw", "Cafeteria", False),
    ("Water Bottle", "Green bottle with a state parks logo", "Tennis Courts", False),
    ("Clothing", "Black hoodie, size M, tiger print on back", "Gym", False),
    ("Clothing", "Red rain jacket", "Main Building", False),
    ("Clothing", "Gray beanie", "Field", False),
    ("Book", "Algebra 2 textbook with a blue cover", "Library", False),
    ("Book", "Spanish workbook", "Main Building", False),
    ("Book", "Novel: paperback with a yellow cover", "Cafeteria", False),
    ("Sports Gear", "Tennis racket in a black case", "Tennis Courts", False),
    ("Sports Gear", "White soccer cleats, size 9", "Field", False),
    ("Sports Gear", "Basketball with signatures", "Gym", False),
    ("School Supplies", "Graphing calculator TI-84", "Library", True),
    ("School Supplies", "Pencil case with cat pattern", "Main Building", False),
    ("Bag", "Navy lunch bag with a zipper", "Cafeteria", False),
    ("Bag", "Gym bag, black with white stripes", "Gym", False),
    ("Electronics", "White wireless earbuds case", "Library", True),
    ("Other", "Silver key ring with 2 keys", "Main Building", True),
]

# Many different students post items (nicknames only)
FINDERS = ["TennisAce27", "BookWorm9", "SkaterSam", "LunchHero", "QuietOwl", "Nana", "Max", "Rayna",
           "ArtKid22", "BlueJay"]
OWNERS = ["SoccerStar", "MathWhiz", "NightReader", "Leo_K", "Mia2010", "DrumKid", "Sunny", "Ollie"]

# How many days ago each sample was found (sample 01 is skipped: Jaden reports that bottle live)
DAYS_AGO = [None, 0, 2, 1, 16, 1, 3, 5, 6, 8, 31, 9, 4, 11, 13, 33, 14, 19, 10, 34]
# Samples Jaden found in the past (they went home: that is where his XP comes from)
JADEN_SAMPLES = {5: 16, 12: 9}     # sample number -> days ago it went home


def main():
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    db.init_db()
    for name in FINDERS + OWNERS + ["Jaden"]:
        db.get_or_create_user(name)

    today = date.today()
    now = datetime.now()

    for n, (category, desc, location, valuable) in enumerate(SAMPLES):
        if DAYS_AGO[n] is None:
            continue
        number = n + 1
        days_ago = DAYS_AGO[n]
        finder = "Jaden" if number in JADEN_SAMPLES else FINDERS[n % len(FINDERS)]
        if number in JADEN_SAMPLES:
            days_ago = JADEN_SAMPLES[number] + 1
        found_on = today - timedelta(days=days_ago)
        created = datetime.combine(found_on, datetime.min.time()) + timedelta(hours=9 + n % 6)
        created = min(created, now - timedelta(hours=2))
        kept_at = db.RETURN_SPOTS[n % len(db.RETURN_SPOTS)] if valuable else None
        item_id = db.save_item(finder, category, desc, location, found_on,
                               photo(f"{number:02d}", category, desc), created.isoformat(timespec="seconds"),
                               valuable=valuable, kept_at=kept_at)

        # What happened to each item (older ones: about half went home)
        owner = OWNERS[n % len(OWNERS)]
        try:
            if number in JADEN_SAMPLES or (n % 4 in (0, 1) and days_ago > 3):
                when = created + timedelta(hours=20)
                db.claim_item(item_id, owner, now=when)
                if valuable:
                    db.pick_up(item_id, owner, now=when + timedelta(hours=3))
            elif n % 4 == 2 and valuable and days_ago > 1:
                db.claim_item(item_id, owner, now=now - timedelta(days=1))
            elif not valuable and days_ago <= 6:
                db.spot_check(item_id, OWNERS[(n + 3) % len(OWNERS)], True, now=now - timedelta(hours=n + 2))
        except db.RuleError:
            pass   # fair-play limit hit: this one just stays waiting

    db.move_old_to_reuse(now)   # tentative rule: 30+ days old -> reuse box

    # Clear the messages made while building the history, so the demo starts with a clean inbox
    with db.connect() as conn:
        conn.execute("DELETE FROM messages")

    add_jaden(today, now)


def add_jaden(today, now):
    """Demo story: everything is shown as Jaden (no switching accounts).
      Jaden's past finds: A navy bottle (Max picked it up 2 days ago), B notebook, + 2 samples
                          -> 180 XP = level 3, Super Finder
      C  black hoodie  -> Jaden found it yesterday in the gym, still waiting
      Jaden LOST his white earbuds and turned on an alert ("white earbuds") 4 days ago.
      D  earbuds case  -> Nana found them yesterday and turned them in at the Library Desk
                          -> Jaden got an alert message
    Demo walkthrough as Jaden: reports a blue bottle -> adds a new alert -> reads the alert message
                        -> "It's mine!" on the earbuds -> picks them up at the Library Desk.
    """
    def report(finder, key, category, desc, location, days_ago, hour, valuable=False, kept_at=None):
        found_on = today - timedelta(days=days_ago)
        created = datetime.combine(found_on, datetime.min.time()) + timedelta(hours=hour)
        created = min(created, now - timedelta(hours=1))
        item_id = db.save_item(finder, category, desc, location, found_on,
                               photo(key, category, desc), created.isoformat(timespec="seconds"),
                               valuable=valuable, kept_at=kept_at)
        return item_id, created

    b, created = report("Jaden", "B", "Book", "Algebra notebook with a purple cover", "Library", 12, 11)
    db.claim_item(b, "Rayna", now=created + timedelta(hours=26))
    a, created = report("Jaden", "A", "Water Bottle", "Navy water bottle with a cross-country logo",
                        "Tennis Courts", 3, 15)
    db.claim_item(a, "Max", now=now - timedelta(days=2))
    report("Jaden", "C", "Clothing", "Black cropped hoodie with silver stars on the front", "Gym", 1, 14)

    with db.connect() as conn:   # older history = already read
        conn.execute("UPDATE messages SET is_read = 1")
    # ...but keep "Max picked up your bottle" as a NEW message for the demo
    with db.connect() as conn:
        conn.execute("""UPDATE messages SET is_read = 0 WHERE to_user = 'Jaden' AND item_id = ?
                        AND text LIKE '%msg_picked_up%'""", (a,))

    # Jaden lost his earbuds: alert set 4 days ago. Nana posts them yesterday -> alert message
    db.add_alert("Jaden", "white earbuds", "Electronics", now=now - timedelta(days=4))
    report("Nana", "D", "Electronics", "White wireless earbuds case", "Cafeteria", 1, 12,
           valuable=True, kept_at="Library Desk")

    print("Tip: log in as Jaden (password 1212). Demo: report a bottle -> add an alert -> "
          "read the alert message -> It's mine! on the earbuds -> pick them up at the Library Desk.")


if __name__ == "__main__":
    main()
