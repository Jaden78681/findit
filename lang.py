"""
FindIt - words on the screen in English and Spanish.

t("key", lang, name=...) returns the text for that key in the chosen language.
To add a language: add a new column (dictionary) with the same keys.
Place names (Tennis Courts, Library Desk…) and nicknames stay as they are.
"""

LANGS = {"en": "English", "es": "Español"}

TEXT = {
    # --- sidebar / welcome
    "tagline": ("Find it. Return it. Reuse it.", "Encuéntralo. Devuélvelo. Reúsalo."),
    "language": ("🌐 Language", "🌐 Idioma"),
    "nickname": ("Your nickname", "Tu apodo"),
    "nickname_help": ("Use a nickname, not your real name.", "Usa un apodo, no tu nombre real."),
    "go_to": ("Go to", "Ir a"),
    "page_Home": ("🏠 Home", "🏠 Inicio"),
    "page_Report": ("🙋 I found something", "🙋 Encontré algo"),
    "page_Lost": ("😢 I lost something", "😢 Perdí algo"),
    "page_Map": ("🗺️ School map", "🗺️ Mapa de la escuela"),
    "page_Search": ("🔎 Browse found items", "🔎 Ver objetos encontrados"),
    "page_My Activity": ("📬 My messages", "📬 Mis mensajes"),
    "page_Profile": ("🏅 My Findy level", "🏅 Mi nivel Findy"),
    "page_Impact": ("🌍 Our school's impact", "🌍 Impacto escolar"),
    "new_messages": ("📬 {n} new message(s). Open 📬 My messages.",
                     "📬 {n} mensaje(s) nuevo(s). Abre 📬 Mis mensajes."),
    "welcome": ("Welcome to FindIt 👋", "Bienvenido a FindIt 👋"),
    "welcome_sub": ("A game-powered Lost & Found for our school.",
                    "Objetos perdidos con juego para nuestra escuela."),
    "welcome_info": ("Log in or sign up with a nickname. Please don't use your real name.",
                     "Entra o crea una cuenta con un apodo. No uses tu nombre real."),

    # --- log in / sign up
    "tab_login": ("🔑 Log in", "🔑 Iniciar sesión"),
    "tab_signup": ("✨ Sign up", "✨ Crear cuenta"),
    "password": ("Password", "Contraseña"),
    "password_confirm": ("Password (again)", "Contraseña (otra vez)"),
    "email": ("School email", "Correo escolar"),
    "email_help": ("Only used if you forget your password.", "Solo se usa si olvidas tu contraseña."),
    "btn_login": ("Log in", "Entrar"),
    "btn_signup": ("Create account", "Crear cuenta"),
    "signup_done": ("Account created! Now log in as **{name}**.",
                    "¡Cuenta creada! Ahora entra como **{name}**."),
    "forgot": ("Forgot your password?", "¿Olvidaste tu contraseña?"),
    "forgot_info": ("Type your school email and we'll send you a reset link.",
                    "Escribe tu correo escolar y te enviaremos un enlace para cambiarla."),
    "btn_send_reset": ("📧 Send reset link", "📧 Enviar enlace"),
    "reset_soon": ("📧 Coming soon: password reset by email isn't connected yet. Ask a teacher for help for now.",
                   "📧 Próximamente: el cambio de contraseña por correo aún no está conectado. Por ahora pide ayuda a un maestro."),
    "logged_in_as": ("👤 {name}", "👤 {name}"),
    "btn_logout": ("🚪 Log out", "🚪 Salir"),
    "logged_out": ("You logged out. See you soon!", "Cerraste sesión. ¡Hasta pronto!"),
    "err_login_empty": ("Type your nickname and password.", "Escribe tu apodo y contraseña."),
    "err_no_account": ("No account with that nickname. Sign up first.", "No hay una cuenta con ese apodo. Primero crea una."),
    "err_wrong_password": ("Wrong password. Try again.", "Contraseña incorrecta. Inténtalo de nuevo."),
    "err_bad_nickname": ("Nickname: 3–20 letters, numbers or _. Not your real name.",
                         "Apodo: 3–20 letras, números o _. No uses tu nombre real."),
    "err_nickname_taken": ("That nickname is taken. Try another one.", "Ese apodo ya existe. Prueba otro."),
    "err_bad_email": ("Please type a valid email.", "Escribe un correo válido."),
    "err_password_match": ("The two passwords don't match.", "Las dos contraseñas no coinciden."),

    # --- status, categories
    "status_Found": ("🟠 Waiting for owner", "🟠 Esperando al dueño"),
    "status_Claimed": ("🟡 Owner on the way", "🟡 El dueño va en camino"),
    "status_Returned": ("🟢 Returned", "🟢 Devuelto"),
    "status_Reuse": ("♻️ Reuse box", "♻️ Caja de reúso"),
    "All": ("All", "Todos"),
    "cat_Water Bottle": ("Water Bottle", "Botella de agua"),
    "cat_Clothing": ("Clothing", "Ropa"),
    "cat_Book": ("Book", "Libro"),
    "cat_Sports Gear": ("Sports Gear", "Equipo deportivo"),
    "cat_School Supplies": ("School Supplies", "Útiles escolares"),
    "cat_Bag": ("Bag", "Bolsa"),
    "cat_Electronics": ("Electronics", "Electrónicos"),
    "cat_Other": ("Other", "Otro"),

    # --- cards
    "view_details": ("View details", "Ver detalles"),
    "no_items": ("No items here yet.", "Todavía no hay objetos aquí."),
    "maybe_gone": ("⚠️ may be gone", "⚠️ puede que ya no esté"),

    "card_found": ("📍 Found: {place} · {d}", "📍 Encontrado: {place} · {d}"),
    "now_spot": ("🧭 Now: still at {place}", "🧭 Ahora: sigue en {place}"),
    "now_desk": ("🧭 Now: {desk}", "🧭 Ahora: {desk}"),
    "now_home": ("🧭 Now: back with the owner", "🧭 Ahora: con su dueño"),
    "now_reuse": ("🧭 Now: school reuse box", "🧭 Ahora: caja de reúso"),

    # --- home
    "hi": ("Hi, {name}! 👋", "¡Hola, {name}! 👋"),
    "my_level": ("My level", "Mi nivel"),
    "my_xp": ("My XP", "Mis XP"),
    "my_xp_help": ("Confirmed XP from items that went home", "XP confirmados de objetos devueltos"),
    "pending_xp": ("Pending XP", "XP pendientes"),
    "pending_xp_help": ("Becomes real XP when your items go home",
                        "Se vuelven XP reales cuando tus objetos vuelven a casa"),
    "challenge": ("🎯 School Return Challenge", "🎯 Reto escolar de devoluciones"),
    "challenge_bar": ("{n} / {goal} items returned", "{n} / {goal} objetos devueltos"),
    "top_finders": ("🏆 This week's Top Finders", "🏆 Mejores buscadores de la semana"),
    "top_finders_cap": ("XP from items that went home in the last 7 days. Nicknames only.",
                        "XP de objetos devueltos en los últimos 7 días. Solo apodos."),
    "top_row": ("**{name}** · {xp} XP · {n} item(s) home", "**{name}** · {xp} XP · {n} objeto(s) devuelto(s)"),
    "top_empty": ("No items went home this week yet. Be the first!",
                  "Esta semana todavía no se devolvió nada. ¡Sé el primero!"),
    "recently_found": ("Recently found", "Encontrados recientemente"),
    "i_found": ("➕ I found something", "➕ Encontré algo"),

    # --- report
    "report_title": ("I Found Something", "Encontré algo"),
    "reports_today": ("Reports today: {n} / {limit}", "Reportes hoy: {n} / {limit}"),
    "rule_leave_it": ("👉 **Don't carry it around.** Leave it right where you found it and post it here. "
                      "The owner will see it and come get it.",
                      "👉 **No lo cargues contigo.** Déjalo donde lo encontraste y publícalo aquí. "
                      "El dueño lo verá y vendrá por él."),
    "valuable_toggle": ("💎 It's a valuable (phone, wallet, keys, earbuds, ID…)",
                        "💎 Es algo de valor (celular, cartera, llaves, audífonos, ID…)"),
    "valuable_warn": ("Valuables shouldn't be left behind. Take it to a **Lost & Found desk**, "
                      "then tell us which one below.",
                      "Los objetos de valor no se deben dejar. Llévalo a un **mostrador de objetos perdidos** "
                      "y dinos a cuál abajo."),
    "photo": ("Photo", "Foto"),
    "photo_tip": ("📸 Photo tip: don't show names, faces, ID cards or phone screens.",
                  "📸 Consejo: que no se vean nombres, caras, credenciales ni pantallas de celular."),
    "type": ("Type", "Tipo"),
    "found_at": ("Found at", "Encontrado en"),
    "date_found": ("Date found", "Fecha"),
    "description": ("Description", "Descripción"),
    "desc_placeholder": ("Blue water bottle with a tennis ball sticker",
                         "Botella azul con una calcomanía de pelota de tenis"),
    "desc_help": ("Write at least {n} characters for the detail bonus (+{xp} XP).",
                  "Escribe al menos {n} caracteres para el bono de detalle (+{xp} XP)."),
    "turned_in_at": ("📍 I turned it in at", "📍 Lo entregué en"),
    "turned_in_help": ("See the green pins on the Map.", "Mira los puntos verdes en el Mapa."),
    "submit": ("Submit", "Enviar"),
    "posted": ("Item #{id} posted ({where})! +{xp} pending XP. It becomes real XP when the owner picks it up.",
               "¡Objeto #{id} publicado ({where})! +{xp} XP pendientes. Se vuelven reales cuando el dueño lo recoja."),
    "posted_left": ("left at {place}", "dejado en {place}"),
    "posted_desk": ("turned in at {desk}", "entregado en {desk}"),

    # --- lost alerts
    "lost_title": ("I Lost Something", "Perdí algo"),
    "lost_intro": ("Tell us what you lost. When someone posts a matching item, you get a message.",
                   "Dinos qué perdiste. Cuando alguien publique algo parecido, te llegará un mensaje."),
    "lost_words": ("What does it look like? (a few words)", "¿Cómo es? (pocas palabras)"),
    "lost_words_ph": ("blue bottle", "botella azul"),
    "lost_words_help": ("Use English words, like the posts: blue bottle, black hoodie, earbuds…",
                        "Usa palabras en inglés, como las publicaciones: blue bottle, black hoodie, earbuds…"),
    "lost_save": ("🔔 Turn on alert", "🔔 Activar alerta"),
    "lost_saved": ("Alert on! We'll message you when a match is posted.",
                   "¡Alerta activada! Te avisaremos cuando aparezca algo parecido."),
    "lost_already": ("Already posted and matching:", "Ya publicado y parecido:"),
    "lost_none_yet": ("Nothing matches yet. We'll keep looking.", "Nada coincide todavía. Seguiremos buscando."),
    "n_matching": ("🔎 {n} matching item(s) now", "🔎 {n} objeto(s) parecido(s) ahora"),
    "no_matching": ("No matching items yet.", "Todavía no hay objetos parecidos."),
    "my_alerts": ("My alerts", "Mis alertas"),
    "no_alerts": ("No alerts yet.", "Todavía no tienes alertas."),
    "delete": ("Delete", "Borrar"),

    # --- map
    "map_title": ("School Map", "Mapa de la escuela"),
    "show_returned": ("Show returned items too", "Mostrar también los devueltos"),
    "map_setup": ("📐 Map setup (click to read lat/lon)", "📐 Ajustar mapa (clic para ver lat/lon)"),
    "map_legend": ("🟠 Waiting for owner · 🟡 Owner on the way (valuables) · 🟢 Returned · "
                   "**B** = building or place where items are found · "
                   "**R** (green) = Lost & Found desk",
                   "🟠 Esperando al dueño · 🟡 El dueño va en camino (objetos de valor) · 🟢 Devuelto · "
                   "**B** = edificio o lugar donde se encuentran objetos · "
                   "**R** (verde) = mostrador de objetos perdidos"),
    "map_setup_info": ("Click any building on the satellite map to see its exact latitude and longitude. "
                       "Then update LOCATIONS or RETURN_SPOT_INFO at the top of db.py.",
                       "Haz clic en un edificio para ver su latitud y longitud. "
                       "Luego cambia LOCATIONS o RETURN_SPOT_INFO en db.py."),
    "desk_tooltip": ("Lost & Found desk {no}: {name}", "Mostrador de objetos perdidos {no}: {name}"),
    "items_found_at": ("Items found at", "Objetos encontrados en"),

    # --- search
    "search_title": ("Browse Found Items", "Ver objetos encontrados"),
    "keyword": ("Keyword", "Palabra clave"),
    "keyword_ph": ("bottle, jacket, blue…", "bottle, jacket, blue…"),
    "place": ("Place", "Lugar"),
    "status": ("Status", "Estado"),
    "when": ("Found when", "Cuándo"),
    "any_time": ("Any time", "Cualquier fecha"),
    "last_n_days": ("Last {n} days", "Últimos {n} días"),
    "best_first": ("Best matches first.", "Primero los más parecidos."),
    "n_found": ("{n} item(s) found", "{n} objeto(s) encontrado(s)"),

    # --- detail
    "back": ("← Back", "← Volver"),
    "item_gone_db": ("This item no longer exists.", "Este objeto ya no existe."),
    "no_photo": ("No photo", "Sin foto"),
    "d_found_at": ("📍 **Found at:** {place}", "📍 **Encontrado en:** {place}"),
    "d_date": ("📅 **Date found:** {d}", "📅 **Fecha:** {d}"),
    "d_by": ("🙋 **Found by:** {name}", "🙋 **Encontrado por:** {name}"),
    "where_left": ("Left where it was found: {place}", "Se dejó donde se encontró: {place}"),
    "where_desk": ("Kept at the Lost & Found desk: {desk}", "Guardado en el mostrador de objetos perdidos: {desk}"),
    "valuable_note": ("💎 Valuable item: kept safe at a Lost & Found desk.",
                      "💎 Objeto de valor: guardado en un mostrador de objetos perdidos."),
    "you_reported": ("You reported this item. Waiting for the owner to find it.",
                     "Tú reportaste este objeto. Esperando a que el dueño lo encuentre."),
    "is_yours_desk": ("**Is this yours?** Tap the button, then go to the desk above to get it.",
                      "**¿Es tuyo?** Toca el botón y ve al mostrador de arriba para recogerlo."),
    "is_yours_spot": ("**Is this yours?** Grab it at the spot above, then tap the button.",
                      "**¿Es tuyo?** Recógelo en el lugar de arriba y luego toca el botón."),
    "btn_mine": ("🙋 It's mine!", "🙋 ¡Es mío!"),
    "btn_mine_picked": ("🙋 It's mine! I picked it up", "🙋 ¡Es mío! Ya lo recogí"),
    "badge_toast": ("🏅 {name} earned a badge: {badge}", "🏅 {name} ganó una insignia: {badge}"),
    "said_theirs": ("🙋 **{name}** said it's theirs.", "🙋 **{name}** dijo que es suyo."),
    "go_desk": ("Go to the **{desk}**. The staff there will hand it to you.",
                "Ve al **{desk}**. El personal te lo entregará."),
    "btn_picked": ("🙌 I picked it up", "🙌 Ya lo recogí"),
    "waiting_desk": ("Waiting for {name} to pick it up at the desk.",
                     "Esperando a que {name} lo recoja en el mostrador."),
    "expire_note": ("If it is not picked up within {n} days, it goes back to Found.",
                    "Si no lo recogen en {n} días, vuelve a «Esperando al dueño»."),
    "went_home": ("🎉 This item went home with {name} on {d}.", "🎉 Este objeto volvió a casa con {name} el {d}."),
    "reuse_note": ("♻️ Nobody picked this up in {n} days, so it went to the school reuse box on {d}.",
                   "♻️ Nadie lo recogió en {n} días, así que pasó a la caja de reúso de la escuela el {d}."),
    "reuse_rule": ("♻️ Not picked up in {n} days → goes to the school reuse box "
                   "(rule to be confirmed with the school).",
                   "♻️ Si nadie lo recoge en {n} días → pasa a la caja de reúso de la escuela "
                   "(regla por confirmar con la escuela)."),
    "still_q": ("**Walking by?** Is it still there?", "**¿Pasas por ahí?** ¿Sigue ahí?"),
    "btn_still": ("👍 Still there", "👍 Sigue ahí"),
    "btn_gone": ("❌ Not there anymore", "❌ Ya no está"),
    "thanks_check": ("Thanks! Everyone can see your update.", "¡Gracias! Todos pueden ver tu actualización."),
    "last_still": ("👍 Still there · checked by {name}, {when}", "👍 Sigue ahí · revisado por {name}, {when}"),
    "last_gone": ("⚠️ Not there anymore · reported by {name}, {when}",
                  "⚠️ Ya no está · reportado por {name}, {when}"),
    "no_check_yet": ("No one has checked on it yet.", "Nadie lo ha revisado todavía."),
    "needs_desk": ("📦 It's been here {n} days. If you walk by, please take it to a Lost & Found desk.",
                   "📦 Lleva {n} días aquí. Si pasas, llévalo a un mostrador de objetos perdidos."),
    "moved_to": ("I took it to", "Lo llevé a"),
    "btn_moved": ("📦 I took it to the desk", "📦 Lo llevé al mostrador"),
    "today": ("today", "hoy"),
    "days_ago": ("{n} day(s) ago", "hace {n} día(s)"),

    # --- activity
    "activity_title": ("My Messages", "Mis mensajes"),
    "tab_messages": ("📬 Messages ({n} new)", "📬 Mensajes ({n} nuevos)"),
    "tab_reported": ("Items I reported ({n})", "Objetos que reporté ({n})"),
    "tab_mine": ("My items ({n})", "Mis objetos ({n})"),
    "no_messages": ("No messages yet.", "Todavía no hay mensajes."),
    "open_item": ("Open item", "Abrir objeto"),

    # --- profile
    "profile_title": ("My Findy Level", "Mi nivel Findy"),
    "xp": ("XP", "XP"),
    "to_next": ("{xp} / {next} XP to {name}", "{xp} / {next} XP para {name}"),
    "top_level": ("Top level reached! 🏆", "¡Nivel máximo! 🏆"),
    "badges": ("Special badges", "Insignias especiales"),
    "levels_title": ("Findy levels", "Niveles Findy"),
    "you_are_here": ("YOU ARE HERE", "ESTÁS AQUÍ"),
    "lv_xp": ("{xp}+ XP", "{xp}+ XP"),
    "next_goal": ("Next: {name} at {xp} XP", "Siguiente: {name} con {xp} XP"),
    "locked": ("(locked)", "(bloqueada)"),
    "b_Water Bottle Hunter": ("Helped 5 water bottles go home", "Ayudó a devolver 5 botellas"),
    "b_Book Finder": ("Helped a book go home", "Ayudó a devolver un libro"),
    "b_Sports Finder": ("Helped sports gear or a tennis court item go home",
                        "Ayudó a devolver equipo deportivo o algo de las canchas de tenis"),
    "b_Return Hero": ("Helped 5 items go home", "Ayudó a devolver 5 objetos"),
    "b_Super Finder": ("Reached the Super Finder level", "Llegó al nivel Super Finder"),
    "how_xp": ("How XP works", "Cómo funcionan los XP"),
    "xp_rules": ("- Report an item: **+{r}** (pending)\n"
                 "- Detailed description: **+{d}** (pending)\n"
                 "- Valuable turned in at a Lost & Found desk: **+{v}** (pending)\n"
                 "- Item goes home: **+{b}**, and all pending XP for that item becomes real XP\n"
                 "- Item goes to the reuse box: the pending XP becomes real (no return bonus)\n"
                 "- Fair play: you can take home only 1 item per day from the same finder\n"
                 "- Levels: {levels}",
                 "- Reportar un objeto: **+{r}** (pendiente)\n"
                 "- Descripción detallada: **+{d}** (pendiente)\n"
                 "- Objeto de valor entregado en un mostrador: **+{v}** (pendiente)\n"
                 "- El objeto vuelve a casa: **+{b}**, y todos sus XP pendientes se vuelven reales\n"
                 "- El objeto pasa a la caja de reúso: sus XP pendientes se vuelven reales (sin bono)\n"
                 "- Juego limpio: solo puedes llevarte 1 objeto al día del mismo buscador\n"
                 "- Niveles: {levels}"),

    # --- impact
    "impact_title": ("Our School's Impact", "Impacto escolar"),
    "m_reported": ("Reported", "Reportados"),
    "m_on_way": ("On the way", "En camino"),
    "m_returned": ("Returned", "Devueltos"),
    "m_this_week": ("Returned this week", "Devueltos esta semana"),
    "m_rate": ("Return rate", "Tasa de devolución"),
    "m_waiting": ("Still waiting", "Esperando"),
    "m_reused": ("Reuse box", "Caja de reúso"),
    "per_week": ("Items returned per week", "Objetos devueltos por semana"),
    "week_of": ("Week of", "Semana del"),

    # --- rule errors (from db.py)
    "err_no_description": ("Please add a short description.", "Agrega una descripción corta."),
    "err_no_location": ("Please pick a location on the school map.", "Elige un lugar del mapa escolar."),
    "err_no_desk": ("Valuables can't be left behind. Pick the Lost & Found desk you turned it in at.",
                    "Los objetos de valor no se dejan. Elige el mostrador donde lo entregaste."),
    "err_daily_limit": ("Daily limit reached: you can report {limit} items per day.",
                        "Límite diario: puedes reportar {limit} objetos por día."),
    "err_no_item": ("Item not found.", "Objeto no encontrado."),
    "err_own_item": ("You reported this item, so you can't claim it.",
                     "Tú reportaste este objeto, así que no puedes reclamarlo."),
    "err_already_home": ("This item already went home.", "Este objeto ya volvió a casa."),
    "err_already_yours": ("You already said it's yours. Go to the desk and pick it up.",
                          "Ya dijiste que es tuyo. Ve al mostrador a recogerlo."),
    "err_someone_else": ("Someone else already said this is theirs. Check with the Lost & Found desk.",
                         "Otra persona ya dijo que es suyo. Pregunta en el mostrador de objetos perdidos."),
    "err_tap_mine_first": ("Tap \"It's mine!\" first.", "Primero toca «¡Es mío!»."),
    "err_pair_limit": ("Fair play: you already took home an item from {finder} today. Try again tomorrow.",
                       "Juego limpio: ya te llevaste un objeto de {finder} hoy. Intenta mañana."),
    "err_no_check_needed": ("This item isn't waiting at its spot anymore.",
                            "Este objeto ya no está esperando en su lugar."),
    "err_alert_words": ("Type a few words about what you lost.", "Escribe unas palabras sobre lo que perdiste."),

    # --- messages (from db.py)
    "msg_picked_up": ("{owner} picked up {item}. It went home! Your XP for this item is now confirmed.",
                      "{owner} recogió {item}. ¡Volvió a casa! Tus XP por este objeto ya están confirmados."),
    "msg_go_to_desk": ("Go to the {desk} to get {item}. The staff there will hand it to you. "
                       "Then tap 'I picked it up'.",
                       "Ve al {desk} por {item}. El personal te lo entregará. Luego toca «Ya lo recogí»."),
    "msg_owner_coming": ("{owner} says {item} is theirs and is going to the {desk}.",
                         "{owner} dice que {item} es suyo y va al {desk}."),
    "msg_alert_match": ("🔔 A new item matches your alert “{words}”: {item} at {place}.",
                        "🔔 Un objeto nuevo coincide con tu alerta «{words}»: {item} en {place}."),
    "msg_gone": ("{who} says {item} is not at {place} anymore.", "{who} dice que {item} ya no está en {place}."),
    "msg_moved": ("{who} took {item} to the {desk}.", "{who} llevó {item} al {desk}."),
    "msg_reuse": ("{item} wasn't picked up in {days} days, so it went to the school reuse box. "
                  "Thanks for helping!",
                  "Nadie recogió {item} en {days} días, así que pasó a la caja de reúso. ¡Gracias por ayudar!"),
}


def t(key, lang="en", **values):
    """Text for `key` in `lang`, with {values} filled in. Unknown keys are shown as they are."""
    pair = TEXT.get(key)
    if pair is None:
        return key.format(**values) if values else key
    text = pair[1] if lang == "es" else pair[0]
    return text.format(**values) if values else text


def cat(category, lang="en"):
    return t(f"cat_{category}", lang)


def item_label(category, item_id, lang="en"):
    return f"{cat(category, lang)} #{item_id}"


def message_text(key, details, lang="en"):
    """Turn a saved message (key + details) into a sentence."""
    if key == "raw":
        return details.get("text", "")
    values = dict(details)
    if "cat" in values and "id" in values:
        values["item"] = item_label(values.pop("cat"), values.pop("id"), lang)
    return t(key, lang, **values)
