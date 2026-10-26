"""
FindIt - story test: plays the main stories in code and checks every rule.

Run:  python test_story.py
It uses a separate test database, so your real data is safe.
"""

import os
from datetime import datetime, timedelta

os.environ["FINDIT_DB"] = "test_findit.db"
import db  # noqa: E402  (must come after setting FINDIT_DB)


def check(label, condition):
    print(("PASS  " if condition else "FAIL  ") + label)
    assert condition, label


def expect_error(label, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except ValueError:
        check(label, True)
        return
    check(label, False)


def last_msg(name):
    """Key of the newest message for this user."""
    return db.message_parts(db.get_messages(name)[0])[0]


def main():
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    db.init_db()
    now = datetime.now()

    # --- Story 1: normal item. Leave it there, the owner says "It's mine!" ---
    db.add_alert("Sam", "blue bottle")
    bottle = db.save_item("Alex", "Water Bottle", "Blue water bottle with a tennis sticker",
                          "Tennis Courts", "2026-10-04")
    it = db.get_item(bottle)
    check("1. normal item saved as Found (no question/answer)", it["status"] == "Found" and not it["kept_at"])
    check("1. Sam's 'blue bottle' alert sent him a message", last_msg("Sam") == "msg_alert_match")
    check("1. Alex has 15 pending XP", db.calc_xp("Alex") == (0, 15))
    check("1. search 'bottle' finds it", bottle in [i["item_id"] for i in db.search_items("bottle")])
    db.spot_check(bottle, "Kai", True)
    check("1. Kai says it's still there", db.last_check(bottle)["still_there"] == 1)
    expect_error("1. Alex cannot claim his own report", db.claim_item, bottle, "Alex")
    badges = db.claim_item(bottle, "Sam")
    it = db.get_item(bottle)
    check("1. Sam: It's mine! I picked it up -> Returned", it["status"] == "Returned" and it["claimed_by"] == "Sam")
    check("1. Alex's XP is now real: 10 + 5 + 30 = 45", db.calc_xp("Alex") == (45, 0))
    check("1. Alex got a 'went home' message", last_msg("Alex") == "msg_picked_up")
    check("1. Alex earned Sports Finder (tennis courts)", "Sports Finder" in badges)
    check("1. Alex is on This week's Top Finders", db.top_finders()[0][:2] == ("Alex", 45))
    expect_error("1. can't claim twice", db.claim_item, bottle, "Sam")
    expect_error("1. no 'still there' check after it went home", db.spot_check, bottle, "Kai", True)

    # --- Story 2: valuable item, turned in at a Lost & Found desk ---
    expect_error("2. a valuable must say which desk it went to", db.save_item,
                 "Kim", "Electronics", "White earbuds case", "Cafeteria", "2026-10-04", valuable=True)
    ear = db.save_item("Kim", "Electronics", "White earbuds case", "Cafeteria", "2026-10-04",
                       valuable=True, kept_at="Library Desk")
    check("2. valuable is kept at the Library Desk", db.get_item(ear)["kept_at"] == "Library Desk")
    check("2. valuable bonus: 10 + 0 + 15 = 25 pending XP", db.calc_xp("Kim") == (0, 25))
    expect_error("2. no 'still there' check for desk items", db.spot_check, ear, "Kai", False)
    expect_error("2. can't tap 'I picked it up' before 'It's mine!'", db.pick_up, ear, "Lee")
    db.claim_item(ear, "Lee")
    it = db.get_item(ear)
    check("2. It's mine! -> Claimed by Lee", it["status"] == "Claimed" and it["claimed_by"] == "Lee")
    check("2. Lee was told which desk to go to", last_msg("Lee") == "msg_go_to_desk")
    check("2. Kim got a message", last_msg("Kim") == "msg_owner_coming")
    expect_error("2. someone else can't claim it now", db.claim_item, ear, "Max")
    expect_error("2. someone else can't pick it up", db.pick_up, ear, "Max")
    db.pick_up(ear, "Lee")
    check("2. Lee picked it up at the desk -> Returned", db.get_item(ear)["status"] == "Returned")
    check("2. Kim's XP: 10 + 15 + 30 = 55", db.calc_xp("Kim") == (55, 0))

    # --- Story 3: left behind for days -> "not there" / taken to a desk / reuse box ---
    old = (now - timedelta(days=4)).isoformat(timespec="seconds")
    cap = db.save_item("Bea", "Clothing", "Gray beanie", "Field", "2026-10-01", created_at=old)
    db.spot_check(cap, "Kai", False)
    check("3. 'not there anymore' is shown and Bea is told", db.last_check(cap)["still_there"] == 0
          and last_msg("Bea") == "msg_gone")
    check("3. 4 days old -> ask people to take it to a desk", db.needs_desk(db.get_item(cap)))
    db.move_to_desk(cap, "Kai", "Gym Office")
    check("3. Kai took it to the Gym Office", db.get_item(cap)["kept_at"] == "Gym Office"
          and last_msg("Bea") == "msg_moved")
    very_old = (now - timedelta(days=31)).isoformat(timespec="seconds")
    book = db.save_item("Bea", "Book", "Old history book", "Library", "2026-09-01", created_at=very_old)
    phone = db.save_item("Bea", "Electronics", "Black phone in a clear case", "Library", "2026-09-01",
                         created_at=very_old, valuable=True, kept_at="Front Office")
    db.move_old_to_reuse()
    check("3. 31 days, nobody came -> reuse box (tentative rule)", db.get_item(book)["status"] == "Reuse")
    check("3. valuables are never sent to the reuse box", db.get_item(phone)["status"] == "Found")
    check("3. reuse: report XP becomes real, no return bonus", db.item_xp(db.get_item(book)) == 10)

    # --- Search, where it is now, this week's numbers ---
    res = db.search_items("blue bottle")
    check("Search 'blue bottle' finds 'Blue water bottle…' (word by word)", bottle in [i["item_id"] for i in res])
    check("Search: best match first", db.match_score(res[0], ["blue", "bottle"]) == 2)
    check("Search: last 7 days filter hides an old item", book not in [i["item_id"] for i in db.search_items(days=7)])
    cap_item = db.get_item(cap)
    check("Map pin moves to the desk when an item is taken there",
          abs(db.map_position(cap_item)[0] - db.RETURN_SPOT_INFO["Gym Office"][1]) < 0.0002)
    check("Impact: items returned this week are counted", db.get_stats()["this_week"] >= 2)

    # --- Findy levels 1-5 ---
    check("Level 1 at 0 XP, level 3 at 180 XP, level 5 at 500 XP",
          (db.level_number(0), db.level_number(180), db.level_number(500)) == (1, 3, 5))

    # --- Accounts: sign up, log in (demo password 1212) ---
    check("Sign up makes a new account", db.sign_up("NewKid7", "kid@school.org", "abc", "abc") == "NewKid7")
    expect_error("Sign up: nickname already taken", db.sign_up, "NewKid7", "x@school.org", "a", "a")
    expect_error("Sign up: bad email", db.sign_up, "Other1", "not-an-email", "a", "a")
    expect_error("Sign up: passwords must match", db.sign_up, "Other1", "o@school.org", "a", "b")
    expect_error("Sign up: nickname too short", db.sign_up, "ab", "o@school.org", "a", "a")
    check("Log in with the demo password 1212", db.log_in("NewKid7", "1212") == "NewKid7")
    expect_error("Log in: wrong password", db.log_in, "NewKid7", "0000")
    expect_error("Log in: no such account", db.log_in, "Nobody99", "1212")

    # --- Other rules ---
    expect_error("An alert needs words", db.add_alert, "Sam", "  ")
    for n in range(3):
        db.save_item("Alex", "Other", f"test item {n}", "Gym", "2026-10-04")
    a2 = db.save_item("Alex", "Other", "second thing", "Gym", "2026-10-04")
    expect_error("Daily limit: 6th report today is blocked", db.save_item,
                 "Alex", "Other", "one too many", "Gym", "2026-10-04")
    expect_error("Fair play: Sam can't take 2 items from Alex in one day", db.claim_item, a2, "Sam")

    db.claim_item(phone, "Cy", now=now - timedelta(days=8))
    db.reset_old_claims()
    check("7-day reset: a valuable nobody picked up went back to Found", db.get_item(phone)["status"] == "Found")

    stats = db.get_stats()
    check("Impact stats add up", stats["reported"] ==
          stats["claimed"] + stats["returned"] + stats["waiting"] + stats["reused"])

    os.remove(db.DB_PATH)
    print("\nAll story checks passed. ✅")


if __name__ == "__main__":
    main()
