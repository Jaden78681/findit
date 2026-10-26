"""
FindIt - Find it. Return it. Reuse it.
A game-powered Lost & Found app for our school.

Run:  streamlit run app.py

This file is only the SCREENS. All rules and saving live in db.py.
Every word on the screen comes from lang.py (English / Spanish).
"""

import html
import io
from datetime import date, datetime

import folium
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

import db
import lang
import themes

import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
st.set_page_config(page_title="FindIt", page_icon=os.path.join(ASSETS, "icon.png"), layout="wide")
st.markdown(themes.css(), unsafe_allow_html=True)   # the app's look: see themes.py
st.markdown("""<style>
.card-desc { height: 3em; line-height: 1.5em; overflow: hidden;
             display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
</style>""", unsafe_allow_html=True)   # item cards: description always takes 2 lines

if not os.path.exists(db.DB_PATH):   # first start (for example on a web server): build the demo data
    import seed
    seed.main()
db.init_db()
db.reset_old_claims()      # valuables nobody picked up at the desk in 7 days -> back to Found
db.move_old_to_reuse()     # ⚠️ tentative: 30 days, nobody came -> school reuse box

PAGES = ["Home", "Report", "Lost", "Search", "Map", "My Activity", "Profile", "Impact"]

st.session_state.setdefault("detail_item", None)
st.session_state.setdefault("page", "Home")
st.session_state.setdefault("lang_pick", "en")


def LANG():
    """'en' or 'es' (English if nothing is selected)."""
    return st.session_state.get("lang_pick") or "en"


def T(key, **values):
    """Screen text in the language the user picked."""
    return lang.t(key, LANG(), **values)


def status_label(status):
    return T(f"status_{status}")


def cat(category):
    return lang.cat(category, LANG())


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def open_item(item_id):
    """Button callback: show the Item Detail screen for this item."""
    st.session_state.detail_item = item_id


def close_item():
    st.session_state.detail_item = None


def go_to(page):
    st.session_state.detail_item = None
    st.session_state.page = page


def shrink_photo(uploaded_file, max_size=800):
    """Make the photo smaller before saving, so the database stays small."""
    img = Image.open(uploaded_file).convert("RGB")
    img.thumbnail((max_size, max_size))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=80)
    return buffer.getvalue()


def when_text(iso):
    days = (datetime.now() - datetime.fromisoformat(iso)).days
    return T("today") if days == 0 else T("days_ago", n=days)


def now_text(item):
    """One line: where the item is right now."""
    if item["status"] == "Returned":
        return T("now_home")
    if item["status"] == "Reuse":
        return T("now_reuse")
    if item["kept_at"]:
        return T("now_desk", desk=db.spot_label(item["kept_at"]))
    return T("now_spot", place=db.place_label(item["location"]))


def where_text(item):
    if item["kept_at"]:
        return T("where_desk", desk=db.spot_label(item["kept_at"]))
    return T("where_left", place=db.place_label(item["location"]))


def item_card(item, key_prefix):
    """One item in a list: photo, short info, and a View button."""
    with st.container(border=True, key=f"card_{key_prefix}_{item['item_id']}"):
        if item["photo"]:
            st.image(item["photo"], width="stretch")
        line = f"**{cat(item['category'])}** · {status_label(item['status'])}" + (" · 💎" if item["valuable"] else "")
        check = db.last_check(item["item_id"]) if item["status"] == "Found" and not item["kept_at"] else None
        if check is not None and not check["still_there"]:
            line += f" · {T('maybe_gone')}"
        st.markdown(line)
        st.caption(T("card_found", place=db.place_label(item["location"]), d=item["date_found"]))
        st.caption(now_text(item))
        # Same height for every card: always 2 lines of description (cut with … if longer)
        st.markdown(f'<div class="card-desc">{html.escape(item["description"])}</div>',
                    unsafe_allow_html=True)
        st.button(T("view_details"), key=f"{key_prefix}_{item['item_id']}",
                  on_click=open_item, args=(item["item_id"],), width="stretch")


def item_grid(items, key_prefix, columns=3):
    if not items:
        st.info(T("no_items"))
        return
    # Build the grid one row at a time, so every row starts on the same line
    for start in range(0, len(items), columns):
        cols = st.columns(columns)
        for col, item in zip(cols, items[start:start + columns]):
            with col:
                item_card(item, key_prefix)


def show_errors(func, *args):
    """Run an action from db.py. Show its rule message (in the user's language) instead of crashing."""
    try:
        return func(*args), True
    except db.RuleError as err:
        st.error(T(err.key, **err.details))
        return None, False


def badge_toasts(item, badges):
    for badge in badges or []:
        st.toast(T("badge_toast", name=item["found_by"], badge=badge))


# ---------------------------------------------------------------------------
# Log in / sign up / log out
#   DEMO: every account's password is 1212 (db.DEMO_PASSWORD).
#   "Forgot password" shows the email form, but sending is not connected yet.
# ---------------------------------------------------------------------------

st.session_state.setdefault("user", None)


def log_out():
    st.session_state.user = None
    st.session_state.detail_item = None
    st.session_state.page = "Home"
    st.session_state.just_logged_out = True


def login_screen():
    st.title(T("welcome"))
    st.write(T("welcome_sub"))
    if st.session_state.pop("just_logged_out", False):
        st.success(T("logged_out"))

    left, _ = st.columns([3, 2])
    with left:
        tab_in, tab_up = st.tabs([T("tab_login"), T("tab_signup")])

        with tab_in:
            with st.form("login_form"):
                name = st.text_input(T("nickname"), help=T("nickname_help"))
                password = st.text_input(T("password"), type="password")
                go = st.form_submit_button(T("btn_login"), type="primary")
            if go:
                user, ok = show_errors(db.log_in, name, password)
                if ok:
                    st.session_state.user = user
                    st.session_state.page = "Home"
                    st.rerun()
            with st.expander(T("forgot")):
                st.caption(T("forgot_info"))
                st.text_input(T("email"), key="reset_email", placeholder="name@school.org")
                if st.button(T("btn_send_reset"), key="send_reset"):
                    st.info(T("reset_soon"))      # placeholder: email sending comes later

        with tab_up:
            with st.form("signup_form", clear_on_submit=True):
                new_name = st.text_input(T("nickname"), help=T("nickname_help"))
                email = st.text_input(T("email"), help=T("email_help"), placeholder="name@school.org")
                c1, c2 = st.columns(2)
                pw1 = c1.text_input(T("password"), type="password")
                pw2 = c2.text_input(T("password_confirm"), type="password")
                made = st.form_submit_button(T("btn_signup"), type="primary")
            if made:
                user, ok = show_errors(db.sign_up, new_name, email, pw1, pw2)
                if ok:
                    st.success(T("signup_done", name=user))


def account_bar():
    """Always-visible account box at the top right of every screen."""
    _, who, out = st.columns([7, 1.4, 1.2], vertical_alignment="center")
    who.markdown(f"<div style='text-align:right'><b>{T('logged_in_as', name=html.escape(nickname))}</b></div>",
                 unsafe_allow_html=True)
    out.button(T("btn_logout"), key="logout_top", on_click=log_out, width="stretch")


# ---------------------------------------------------------------------------
# Opening slides (optional, for presentations)
#   OFF by default: the app opens straight to the log-in screen.
#   To show Jaden's slides (assets/slides/slide-1.jpg …) full screen first,
#   add ?slides=on at the end of the address. Click = next slide; the last click opens the log-in screen.
# ---------------------------------------------------------------------------

SLIDE_DIR = os.path.join(ASSETS, "slides")
SLIDES = sorted(f for f in os.listdir(SLIDE_DIR) if f.lower().endswith((".jpg", ".png"))) if os.path.isdir(SLIDE_DIR) else []
if "slide" not in st.session_state:
    st.session_state.slide = 0 if st.query_params.get("slides") == "on" else len(SLIDES)


def next_slide():
    st.session_state.slide += 1


@st.cache_data
def slide_src(name):
    with open(os.path.join(ASSETS, "slides", name), "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()


if st.session_state.user is None and st.session_state.slide < len(SLIDES):
    st.markdown(f"""<style>
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"], header, [data-testid="stToolbar"] {{display:none !important}}
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{background:#000 !important}}
.block-container {{padding:0 !important; max-width:100% !important}}
.slide-img {{position:fixed; inset:0; width:100vw; height:100vh; object-fit:contain; background:#000; z-index:1}}
.st-key-slide_next button {{position:fixed !important; inset:0 !important; width:100vw !important; height:100vh !important;
  opacity:0 !important; z-index:5 !important; cursor:pointer; border:none !important}}
</style>
<img class="slide-img" src="{slide_src(SLIDES[st.session_state.slide])}" alt="slide {st.session_state.slide + 1}">""",
                unsafe_allow_html=True)
    st.button("next", key="slide_next", on_click=next_slide)
    st.stop()


# ---------------------------------------------------------------------------
# Sidebar: language, account, navigation
# ---------------------------------------------------------------------------

with st.sidebar:
    st.image(os.path.join(ASSETS, "logo.png"), width="stretch")
    st.segmented_control(T("language"), list(lang.LANGS), key="lang_pick",
                         format_func=lambda code: lang.LANGS[code], selection_mode="single")
    nickname = st.session_state.user
    if nickname:
        st.markdown(f"**{T('logged_in_as', name=html.escape(nickname))}**")
        st.button(T("btn_logout"), key="logout_side", on_click=log_out, width="stretch")
        st.radio(T("go_to"), PAGES, key="page", on_change=close_item, format_func=lambda p: T(f"page_{p}"))
        unread = db.count_unread(nickname)
        if unread:
            st.warning(T("new_messages", n=unread))

if not nickname:
    login_screen()
    st.stop()

account_bar()


# ---------------------------------------------------------------------------
# Screens
# ---------------------------------------------------------------------------

def top_finders_box():
    st.subheader(T("top_finders"))
    st.caption(T("top_finders_cap"))
    board = db.top_finders()
    if not board:
        st.info(T("top_empty"))
        return
    medals = ["🥇", "🥈", "🥉", "4.", "5."]
    with st.container(border=True, key="card_top_finders"):
        for medal, (name, xp, n) in zip(medals, board):
            st.markdown(f"{medal} " + T("top_row", name=html.escape(name), xp=xp, n=n)
                        + ("  ⬅️" if name == nickname else ""))


@st.cache_data
def level_svg(level):
    with open(os.path.join(ASSETS, "levels", f"level{level}.svg"), "rb") as f:
        return "data:image/svg+xml;base64," + base64.b64encode(f.read()).decode()


def findy_img(level, size, gray=False):
    """The level character (Findy) as an <img>. Gray = not reached yet."""
    style = f"width:{size}px;height:{size}px"
    if gray:
        style += ";filter:grayscale(1);opacity:.45"
    return f'<img src="{level_svg(level)}" style="{style}" alt="level {level}">'


def home_screen():
    level_no = db.level_number(db.calc_xp(nickname)[0])
    pic, title = st.columns([1, 9], vertical_alignment="center")
    pic.markdown(findy_img(level_no, 96), unsafe_allow_html=True)
    title.title(T("hi", name=nickname))

    confirmed, pending = db.calc_xp(nickname)
    level, _ = db.calc_level(confirmed)
    stats = db.get_stats()

    c1, c2, c3 = st.columns(3)
    c1.metric(T("my_level"), level)
    c2.metric(T("my_xp"), confirmed, help=T("my_xp_help"))
    c3.metric(T("pending_xp"), pending, help=T("pending_xp_help"))

    left, right = st.columns([3, 2])
    with left:
        st.subheader(T("challenge"))
        st.progress(min(stats["returned"] / db.SCHOOL_GOAL, 1.0),
                    text=T("challenge_bar", n=stats["returned"], goal=db.SCHOOL_GOAL))
    with right:
        top_finders_box()

    st.subheader(T("recently_found"))
    item_grid(db.recent_items(6), "home")

    st.button(T("i_found"), on_click=go_to, args=("Report",), type="primary")


def report_screen():
    st.title(T("report_title"))
    used = db.count_today_reports(nickname)
    st.caption(T("reports_today", n=used, limit=db.DAILY_REPORT_LIMIT))
    st.info(T("rule_leave_it"))

    valuable = st.toggle(T("valuable_toggle"), key="report_valuable")
    if valuable:
        st.warning(T("valuable_warn"))

    with st.form("report_form", clear_on_submit=True):
        photo = st.file_uploader(T("photo"), type=["jpg", "jpeg", "png", "webp"])
        st.caption(T("photo_tip"))
        c1, c2, c3 = st.columns(3)
        category = c1.selectbox(T("type"), db.CATEGORIES, format_func=cat)
        location = c2.selectbox(T("found_at"), list(db.LOCATIONS), format_func=db.place_label)
        found_on = c3.date_input(T("date_found"), value=date.today(), max_value=date.today())
        description = st.text_area(
            T("description"), placeholder=T("desc_placeholder"),
            help=T("desc_help", n=db.DETAIL_MIN_CHARS, xp=db.XP_DETAIL))
        kept_at = None
        if valuable:
            kept_at = st.selectbox(T("turned_in_at"), db.RETURN_SPOTS, format_func=db.spot_label,
                                   help=T("turned_in_help"))
        submitted = st.form_submit_button(T("submit"), type="primary")

    if submitted:
        photo_bytes = shrink_photo(photo) if photo else None
        item_id, ok = show_errors(db.save_item, nickname, category, description, location, found_on,
                                  photo_bytes, None, valuable, kept_at)
        if ok:
            xp = db.XP_REPORT + (db.XP_DETAIL if db.is_detailed(description) else 0) + \
                (db.XP_VALUABLE if valuable else 0)
            where = T("posted_desk", desk=db.spot_label(kept_at)) if valuable else \
                T("posted_left", place=location)
            st.success(T("posted", id=item_id, where=where, xp=xp))


def lost_screen():
    st.title(T("lost_title"))
    st.info(T("lost_intro"))
    with st.form("alert_form", clear_on_submit=True):
        c1, c2 = st.columns([2, 1])
        words = c1.text_input(T("lost_words"), placeholder=T("lost_words_ph"), help=T("lost_words_help"))
        category = c2.selectbox(T("type"), ["All"] + db.CATEGORIES,
                                format_func=lambda c: T("All") if c == "All" else cat(c))
        saved = st.form_submit_button(T("lost_save"), type="primary")

    if saved:
        matches, ok = show_errors(db.add_alert, nickname, words, category)
        if ok:
            st.success(T("lost_saved"))
            if matches:
                st.markdown(f"**{T('lost_already')}**")
                item_grid(matches, "alertnow")
            else:
                st.caption(T("lost_none_yet"))

    st.subheader(T("my_alerts"))
    alerts = db.my_alerts(nickname)
    if not alerts:
        st.caption(T("no_alerts"))
    for a in alerts:
        with st.container(border=True, key=f"card_alert_{a['alert_id']}"):
            c1, c2 = st.columns([4, 1])
            kind = T("All") if a["category"] == "All" else cat(a["category"])
            c1.markdown(f"🔔 **{html.escape(a['words'])}** · {kind}")
            if c2.button(T("delete"), key=f"del_alert_{a['alert_id']}"):
                db.delete_alert(a["alert_id"], nickname)
                st.rerun()
            found = db.alert_matches(a["words"], a["category"], nickname)
            if found:
                with st.expander(T("n_matching", n=len(found))):
                    item_grid(found, f"alert{a['alert_id']}")
            else:
                st.caption(T("no_matching"))


STATUS_COLOR = {"Found": "#E8833A", "Claimed": "#C9A227", "Returned": "#1F7A70", "Reuse": "#7A5CC2"}


def label_html(text, bg, fg="#FFFFFF"):
    """A small always-visible name tag for the map."""
    return (f'<div style="display:inline-block; white-space:nowrap; transform:translate(-50%,-130%); '
            f'background:{bg}; color:{fg}; padding:2px 8px; border-radius:8px; font:600 12px sans-serif; '
            f'box-shadow:0 1px 4px rgba(0,0,0,.4)">{text}</div>')


def school_map(items, setup_mode=False):
    """Real map of the school: satellite photo + building labels + Lost & Found desks + item pins."""
    m = folium.Map(location=db.MAP_CENTER, zoom_start=db.MAP_ZOOM, tiles=None, control_scale=True)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Imagery © Esri", name="Satellite", max_zoom=19).add_to(m)
    folium.TileLayer("OpenStreetMap", name="Street map").add_to(m)

    # Buildings / places where items are found (B1, B2, ...)
    for name, (no, lat, lon) in db.LOCATIONS.items():
        folium.Marker([lat, lon], tooltip=f"{no} {name}",
                      icon=folium.DivIcon(html=label_html(f"{no} {name}", "#16213E"))).add_to(m)

    # Lost & Found desks (R1, R2, ...)
    for name, (no, lat, lon) in db.RETURN_SPOT_INFO.items():
        folium.Marker([lat, lon], tooltip=T("desk_tooltip", no=no, name=name),
                      icon=folium.Icon(color="green", icon="inbox", prefix="fa")).add_to(m)
        folium.Marker([lat, lon], icon=folium.DivIcon(
            html=label_html(f"{no} {name}", "#1F7A70"))).add_to(m)

    # Item pins, colored by status
    for item in items:
        lat, lon = db.map_position(item)
        name = html.escape(f"#{item['item_id']} {cat(item['category'])}")
        folium.CircleMarker(
            [lat, lon], radius=8, weight=2, color="#FFFFFF", fill=True, fill_opacity=0.95,
            fill_color=STATUS_COLOR[item["status"]],
            tooltip=f"{name} · {status_label(item['status'])}",
            popup=folium.Popup(f"<b>{name}</b><br>{html.escape(item['description'])}"
                               f"<br>{html.escape(now_text(item))}", max_width=260),
        ).add_to(m)

    if setup_mode:
        folium.LatLngPopup().add_to(m)   # click anywhere to see its lat/lon
    folium.LayerControl(collapsed=False).add_to(m)
    return m


def map_screen():
    st.title(T("map_title"))
    st.caption(f"📍 {db.SCHOOL_NAME} · 201 Deep Wood Dr, Round Rock, TX")
    c1, c2 = st.columns(2)
    show_returned = c1.toggle(T("show_returned"), value=False)
    setup_mode = c2.toggle(T("map_setup"), value=False)

    active = ("Found", "Claimed")
    items = [i for i in db.search_items() if show_returned or i["status"] in active]
    components.html(school_map(items, setup_mode).get_root().render(), height=560)
    st.markdown(T("map_legend"))

    if setup_mode:
        st.info(T("map_setup_info"))
        st.dataframe(
            [{"No": no, "Name": n, "Type": "Building", "Lat": lat, "Lon": lon}
             for n, (no, lat, lon) in db.LOCATIONS.items()] +
            [{"No": no, "Name": n, "Type": "Lost & Found desk", "Lat": lat, "Lon": lon}
             for n, (no, lat, lon) in db.RETURN_SPOT_INFO.items()],
            hide_index=True)

    place = st.selectbox(T("items_found_at"), list(db.LOCATIONS), format_func=db.place_label)
    here = [i for i in db.search_items(location=place) if show_returned or i["status"] in active]
    item_grid(here, "map")


def search_screen():
    st.title(T("search_title"))
    keyword = st.text_input(T("keyword"), placeholder=T("keyword_ph"))
    c1, c2, c3, c4 = st.columns(4)
    category = c1.selectbox(T("type"), ["All"] + db.CATEGORIES,
                            format_func=lambda c: T("All") if c == "All" else cat(c))
    location = c2.selectbox(T("place"), ["All"] + list(db.LOCATIONS),
                            format_func=lambda p: T("All") if p == "All" else db.place_label(p))
    status = c3.selectbox(T("status"), ["All"] + db.STATUSES,
                          format_func=lambda s: T("All") if s == "All" else status_label(s))
    days = c4.selectbox(T("when"), [None, 7, 30],
                        format_func=lambda n: T("any_time") if n is None else T("last_n_days", n=n))

    results = db.search_items(keyword, category, location, status, days)
    st.caption(T("n_found", n=len(results)) + (" " + T("best_first") if keyword.strip() else ""))
    item_grid(results, "search")


def spot_check_box(item, is_finder):
    """Left-behind items: walkers-by say "still there" / "not there anymore"."""
    check = db.last_check(item["item_id"])
    if check is None:
        st.caption(T("no_check_yet"))
    elif check["still_there"]:
        st.caption(T("last_still", name=check["nickname"], when=when_text(check["created_at"])))
    else:
        st.warning(T("last_gone", name=check["nickname"], when=when_text(check["created_at"])))

    st.markdown(T("still_q"))
    c1, c2 = st.columns(2)
    if c1.button(T("btn_still"), key="still_there", width="stretch"):
        _, ok = show_errors(db.spot_check, item["item_id"], nickname, True)
        if ok:
            st.toast(T("thanks_check"))
            st.rerun()
    if c2.button(T("btn_gone"), key="not_there", width="stretch"):
        _, ok = show_errors(db.spot_check, item["item_id"], nickname, False)
        if ok:
            st.toast(T("thanks_check"))
            st.rerun()

    if db.needs_desk(item):
        st.info(T("needs_desk", n=db.days_waiting(item)))
        c1, c2 = st.columns([2, 1])
        desk = c1.selectbox(T("moved_to"), db.RETURN_SPOTS, format_func=db.spot_label, key="move_desk")
        if c2.button(T("btn_moved"), key="moved_btn", width="stretch"):
            _, ok = show_errors(db.move_to_desk, item["item_id"], nickname, desk)
            if ok:
                st.rerun()


def detail_screen(item_id):
    item = db.get_item(item_id)
    st.button(T("back"), on_click=close_item)
    if item is None:
        st.error(T("item_gone_db"))
        return

    st.title(f"{cat(item['category'])} #{item['item_id']}")
    left, right = st.columns([1, 1])
    with left:
        if item["photo"]:
            st.image(item["photo"], width="stretch")
        else:
            st.info(T("no_photo"))
    with right:
        st.markdown(f"### {status_label(item['status'])}")
        st.write(item["description"])
        st.write(T("d_found_at", place=item["location"]))
        st.write(T("d_date", d=item["date_found"]))
        st.write(T("d_by", name=item["found_by"]))

        is_finder = nickname == item["found_by"]
        is_owner = nickname == item["claimed_by"]

        if item["status"] in ("Found", "Claimed"):
            st.info(f"📍 **{where_text(item)}**")
        if item["valuable"]:
            st.caption(T("valuable_note"))

        # --- Status: Found -> the owner says "It's mine!"
        if item["status"] == "Found":
            if is_finder:
                st.caption(T("you_reported"))
            else:
                if item["valuable"]:
                    st.markdown(T("is_yours_desk"))
                    label = T("btn_mine")
                else:
                    st.markdown(T("is_yours_spot"))
                    label = T("btn_mine_picked")
                if st.button(label, type="primary"):
                    badges, ok = show_errors(db.claim_item, item_id, nickname)
                    if ok:
                        badge_toasts(item, badges)
                        st.rerun()
            if not item["kept_at"]:
                st.divider()
                spot_check_box(item, is_finder)
                if not item["valuable"]:
                    st.caption(T("reuse_rule", n=db.REUSE_AFTER_DAYS))

        # --- Status: Claimed -> valuable, the owner is on the way to the desk
        elif item["status"] == "Claimed":
            st.write(T("said_theirs", name=item["claimed_by"]))
            if is_owner:
                st.success(T("go_desk", desk=db.spot_label(item["kept_at"])))
                if st.button(T("btn_picked"), type="primary"):
                    badges, ok = show_errors(db.pick_up, item_id, nickname)
                    if ok:
                        badge_toasts(item, badges)
                        st.rerun()
            else:
                st.caption(T("waiting_desk", name=item["claimed_by"]))
            st.caption(T("expire_note", n=db.CLAIM_EXPIRE_DAYS))

        # --- Status: Returned / Reuse
        elif item["status"] == "Returned":
            st.success(T("went_home", name=item["claimed_by"], d=item["returned_at"][:10]))
        else:
            st.info(T("reuse_note", n=db.REUSE_AFTER_DAYS, d=(item["reused_at"] or "")[:10]))


def activity_screen():
    st.title(T("activity_title"))
    data = db.my_activity(nickname)
    messages = db.get_messages(nickname)
    unread = sum(1 for m in messages if not m["is_read"])
    tab0, tab1, tab2 = st.tabs([T("tab_messages", n=unread),
                                T("tab_reported", n=len(data["reported"])),
                                T("tab_mine", n=len(data["my_items"]))])

    with tab0:
        if not messages:
            st.info(T("no_messages"))
        for m in messages:
            key, details = db.message_parts(m)
            with st.container(border=True, key=f"card_msg_{m['message_id']}"):
                st.markdown(("🆕 " if not m["is_read"] else "") +
                            html.escape(lang.message_text(key, details, LANG())))
                c1, c2 = st.columns([3, 1])
                c1.caption(m["created_at"].replace("T", " ")[:16])
                if m["item_id"]:
                    c2.button(T("open_item"), key=f"msg_{m['message_id']}",
                              on_click=open_item, args=(m["item_id"],))
        db.mark_read(nickname)   # seen now; the "new" marks clear on the next visit

    with tab1:
        item_grid(data["reported"], "mine")

    with tab2:
        item_grid(data["my_items"], "mine2")


def level_ladder(xp):
    """Levels 1-5 with Findy: passed = color (small), current = color (big), next ones = gray."""
    now = db.level_number(xp)
    st.subheader(T("levels_title"))
    cells = ""
    for i, (need, name) in enumerate(db.LEVELS, start=1):
        if i == now:
            box = ("flex:1.6;border:5px solid #1B1B1B;background:#FFF3B0;box-shadow:6px 6px 0 #FF4FA3;"
                   "transform:translateY(-8px)")
            pic = findy_img(i, 150)
            tag = (f'<div style="display:inline-block;background:#1B1B1B;color:#FFD23F;font-weight:800;'
                   f'font-size:13px;padding:3px 10px;border-radius:8px;margin-bottom:4px">{T("you_are_here")}</div>')
            title = f'<div style="font-size:22px;font-weight:900">{name}</div>'
        else:
            box = "flex:1;border:3px solid #1B1B1B;background:#FFFFFF"
            pic = findy_img(i, 84, gray=i > now)
            tag = ""
            muted = "color:#999" if i > now else ""
            title = f'<div style="font-size:16px;font-weight:800;{muted}">{name}</div>'
        cells += (f'<div style="{box};border-radius:18px;padding:12px 8px;text-align:center;display:flex;'
                  f'flex-direction:column;align-items:center;justify-content:flex-end">'
                  f'{tag}{pic}{title}<div style="font-size:13px;color:#666">{T("lv_xp", xp=need)}</div></div>')
    st.markdown(f'<div style="display:flex;gap:12px;align-items:flex-end;margin:10px 0 18px">{cells}</div>',
                unsafe_allow_html=True)


def profile_screen():
    st.title(T("profile_title"))
    confirmed, pending = db.calc_xp(nickname)
    level, next_xp = db.calc_level(confirmed)

    st.markdown(f"## 🧑 {nickname} · **{level}**")
    level_ladder(confirmed)
    c1, c2 = st.columns(2)
    c1.metric(T("xp"), confirmed)
    c2.metric(T("pending_xp"), pending, help=T("pending_xp_help"))

    if next_xp:
        next_name, _ = db.calc_level(next_xp)
        st.progress(confirmed / next_xp, text=T("to_next", xp=confirmed, next=next_xp, name=next_name))
    else:
        st.progress(1.0, text=T("top_level"))

    st.subheader(T("badges"))
    mine = db.get_badges(nickname)
    icons = {"Water Bottle Hunter": "💧", "Book Finder": "📚", "Sports Finder": "🎾", "Return Hero": "🦸"}
    cards = ""
    for badge in db.BADGES:
        got = badge in mine
        look = "" if got else "filter:grayscale(1);opacity:.45;"
        cards += (f'<div style="flex:1;min-width:150px;text-align:center;padding:14px;border:3px solid #1B1B1B;'
                  f'border-radius:16px;background:#FFFFFF;{look}">'
                  f'<div style="font-size:44px;line-height:1.1">{icons.get(badge, "🏅")}</div>'
                  f'<div style="font-weight:800;margin-top:6px">{badge}</div>'
                  f'<div style="font-size:13px;color:#555">{T("b_" + badge)}</div></div>')
    st.markdown(f'<div style="display:flex;gap:14px;flex-wrap:wrap">{cards}</div>', unsafe_allow_html=True)
    st.write("")

    with st.expander(T("how_xp")):
        st.markdown(T("xp_rules", r=db.XP_REPORT, d=db.XP_DETAIL, v=db.XP_VALUABLE, b=db.XP_RETURN_BONUS,
                      levels=" → ".join(f"{name} ({xp})" for xp, name in db.LEVELS)))


def impact_screen():
    st.title(T("impact_title"))
    stats = db.get_stats()
    c = st.columns(4)
    c[0].metric(T("m_reported"), stats["reported"])
    c[1].metric(T("m_returned"), stats["returned"])
    c[2].metric(T("m_rate"), f"{stats['return_rate']}%")
    c[3].metric(T("m_this_week"), stats["this_week"])
    c = st.columns(4)
    c[0].metric(T("m_waiting"), stats["waiting"])
    c[1].metric(T("m_on_way"), stats["claimed"])
    c[2].metric(T("m_reused"), stats["reused"])

    left, right = st.columns([3, 2])
    with left:
        st.subheader(T("challenge"))
        st.progress(min(stats["returned"] / db.SCHOOL_GOAL, 1.0),
                    text=T("challenge_bar", n=stats["returned"], goal=db.SCHOOL_GOAL))
        st.subheader(T("per_week"))
        weekly = pd.DataFrame(stats["weekly"], columns=[T("week_of"), T("m_returned")])
        st.bar_chart(weekly, x=T("week_of"), y=T("m_returned"), color="#1F7A70")
    with right:
        top_finders_box()


# ---------------------------------------------------------------------------
# Router: decide which screen to show
# ---------------------------------------------------------------------------

if st.session_state.detail_item:
    detail_screen(st.session_state.detail_item)
else:
    {
        "Home": home_screen,
        "Report": report_screen,
        "Lost": lost_screen,
        "Map": map_screen,
        "Search": search_screen,
        "My Activity": activity_screen,
        "Profile": profile_screen,
        "Impact": impact_screen,
    }[st.session_state.page]()
