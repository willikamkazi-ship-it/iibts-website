"""
Builds the OBTS public website (static HTML for GitHub Pages) from one
content source, in English (root), Kiswahili (sw/) and French (fr/).

    python3 tools/build_site.py            # writes the pages
    python3 tools/build_site.py --check    # exits 1 if a page is out of date

Rules kept by this file (see tools/check_site.cjs for the tests):
  * no fees, dates, working e-mail addresses, accreditation or partnership
    claims: fees and start dates are "to be announced" until the owner
    approves them, and WhatsApp (+255 704 686 885, already published on
    the earlier site) is the only contact channel;
  * no draft lessons, answer keys or lecturer guides: they live only in
    the private review area, never in this repository;
  * PREVIEW = True puts a "preview — not yet published" banner on every
    page; set it to False only with the launch instruction.
"""

import html
import json
import os
import re
import sys
from urllib.parse import urlsplit, urlencode

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREVIEW = False
WHATSAPP = "255704686885"
WHATSAPP_DISPLAY = "+255 704 686 885"
DOMAIN = "obts.co.tz"
# The school system's public address (odm-ai-asistant), e.g. "https://<service>.onrender.com". Empty until the
# library routes (/library, served by portal_routes.py) are deployed on PRODUCTION and checked there: while empty,
# no page links to the system and the library says "not yet open". The staging address must never be put here.
SERVICE_BASE = "https://odm-ai-asistant.onrender.com"
PAGES = ("index", "about", "courses", "how-to-learn", "admissions", "contact", "faq", "privacy", "terms",
         "library", "bookstore", "portal", "assistant", "syllabus")
NAV = ("index", "about", "courses", "admissions", "library", "portal", "contact", "faq")  # how-to-learn: home and footer
LANGS = {"en": "", "sw": "sw/", "fr": "fr/"}
LANG_LABEL = {"en": "EN", "sw": "SW", "fr": "FR"}
OG_LOCALE = {"en": "en_US", "sw": "sw_TZ", "fr": "fr_FR"}
LANG_NAME = {"en": "English", "sw": "Kiswahili", "fr": "Français"}


def e(text):
    return html.escape(text, quote=True)


# ------------------------------------------------------------
# Courses (names and module counts from curriculum.py of the OBTS system;
# descriptions summarise the module titles; nothing about fees or dates)
# ------------------------------------------------------------

COURSES = [
    {"code": "GB", "modules": 20, "open": True,
     "name": {"en": "General Bible Studies & Theology", "sw": "Mafunzo ya Jumla ya Biblia na Theolojia",
              "fr": "Études bibliques générales et théologie"},
     "text": {"en": "A broad, systematic study of Scripture and Christian doctrine: the Bible and its authority, God, "
                    "creation, humanity, sin, Christ, salvation, the Holy Spirit, the Church, worship and Christian life.",
              "sw": "Mafunzo mapana na ya mpangilio kuhusu Maandiko na mafundisho ya Kikristo: Biblia na mamlaka yake, "
                    "Mungu, uumbaji, mwanadamu, dhambi, Kristo, wokovu, Roho Mtakatifu, Kanisa, ibada na maisha ya Kikristo.",
              "fr": "Une étude large et ordonnée de l'Écriture et de la doctrine chrétienne : la Bible et son autorité, "
                    "Dieu, la création, l'être humain, le péché, le Christ, le salut, le Saint-Esprit, l'Église, le "
                    "culte et la vie chrétienne."}},
    {"code": "B66", "modules": 12, "open": True,
     "name": {"en": "66 Books of the Bible", "sw": "Vitabu 66 vya Biblia", "fr": "Les 66 livres de la Bible"},
     "text": {"en": "A guided reading of the whole Bible, book by book: the Law, the historical books, poetry and "
                    "wisdom, the prophets, the Gospels, Acts, the letters and Revelation.",
              "sw": "Usomaji wa Biblia nzima ukiongozwa, kitabu kwa kitabu: Torati, vitabu vya historia, mashairi na "
                    "hekima, manabii, Injili, Matendo, nyaraka na Ufunuo.",
              "fr": "Une lecture guidée de toute la Bible, livre par livre : la Loi, les livres historiques, la poésie "
                    "et la sagesse, les prophètes, les Évangiles, les Actes, les lettres et l'Apocalypse."}},
    {"code": "PE", "modules": 12, "open": True,
     "name": {"en": "Pastoral English", "sw": "Kiingereza cha Kichungaji", "fr": "Anglais pastoral"},
     "text": {"en": "English for ministry: reading and explaining the Bible, prayer, preaching and teaching, worship "
                    "services, pastoral conversations, evangelism and church administration.",
              "sw": "Kiingereza kwa huduma: kusoma na kueleza Biblia, maombi, kuhubiri na kufundisha, ibada, "
                    "mazungumzo ya kichungaji, uinjilisti na utawala wa kanisa.",
              "fr": "L'anglais pour le ministère : lire et expliquer la Bible, la prière, la prédication et "
                    "l'enseignement, le culte, les entretiens pastoraux, l'évangélisation et l'administration de l'Église."}},
    {"code": "ES", "modules": 12, "open": True,
     "name": {"en": "English Speaking", "sw": "Kuzungumza Kiingereza", "fr": "Anglais oral"},
     "text": {"en": "Everyday spoken English: grammar and tenses, vocabulary and conversation, pronunciation and "
                    "listening, fluency, reading and practical writing.",
              "sw": "Kiingereza cha kuzungumza kila siku: sarufi na nyakati, msamiati na mazungumzo, matamshi na "
                    "kusikiliza, ufasaha, kusoma na uandishi wa vitendo.",
              "fr": "L'anglais parlé au quotidien : grammaire et temps, vocabulaire et conversation, prononciation et "
                    "écoute, aisance, lecture et écriture pratique."}},
    {"code": "CL", "modules": 16, "open": True,
     "name": {"en": "Christian Leadership", "sw": "Uongozi wa Kikristo", "fr": "Leadership chrétien"},
     "text": {"en": "Biblical models of leadership, character and integrity, calling and vision, servant leadership, "
                    "teams, decisions, conflict, church governance, stewardship and accountability.",
              "sw": "Mifano ya uongozi katika Biblia, tabia na uadilifu, wito na maono, uongozi wa kitumishi, timu, "
                    "maamuzi, migogoro, utawala wa kanisa, uwakili na uwajibikaji.",
              "fr": "Modèles bibliques de leadership, caractère et intégrité, appel et vision, leadership de "
                    "serviteur, équipes, décisions, conflits, gouvernance de l'Église, gestion et responsabilité."}},
    {"code": "ENT", "modules": 20, "open": True,
     "name": {"en": "Entrepreneurship & Business Growth", "sw": "Ujasiriamali na Ukuaji wa Biashara",
              "fr": "Entrepreneuriat et croissance des entreprises"},
     "text": {"en": "From an idea to a working business: opportunities, business models, customers, planning, "
                    "marketing, money and pricing, operations and customer service, built step by step in a project.",
              "sw": "Kutoka wazo hadi biashara inayofanya kazi: fursa, mifumo ya biashara, wateja, mipango, masoko, "
                    "fedha na bei, uendeshaji na huduma kwa wateja, hatua kwa hatua katika mradi mmoja.",
              "fr": "De l'idée à l'entreprise qui fonctionne : opportunités, modèles d'affaires, clients, plan, "
                    "marketing, argent et prix, fonctionnement et service client, construits pas à pas dans un projet."}},
    {"code": "AI", "modules": 13, "open": False,
     "name": {"en": "Using AI for Work, Business and Life", "sw": "Matumizi ya AI kwa Kazi, Biashara na Maisha",
              "fr": "Utiliser l'IA pour le travail, les affaires et la vie"},
     "text": {"en": "A practical course: you make complete, usable work with free or low-cost tools on a phone — a checked "
                    "report, content and an advert; a video or an audio product; and a working website. You also learn "
                    "where AI goes wrong and how to check it. Taught in Kiswahili.",
              "sw": "Kozi ya vitendo: unatengeneza kazi kamili inayotumika kwa zana za bure au za gharama nafuu kwa simu — "
                    "ripoti, maudhui na tangazo lililohakikiwa; video au bidhaa ya sauti; na tovuti inayofanya kazi. "
                    "Unajifunza pia AI inakosea wapi na jinsi ya kuhakiki. Inafundishwa kwa Kiswahili.",
              "fr": "Un cours pratique : vous réalisez un travail complet et utilisable avec des outils gratuits ou peu "
                    "coûteux sur téléphone — un rapport vérifié, du contenu et une annonce ; une vidéo ou un produit audio ; "
                    "et un site web qui fonctionne. Vous apprenez aussi où l'IA se trompe et comment la vérifier. "
                    "Enseigné en kiswahili."}},
]

# ------------------------------------------------------------
# Words used on every page
# ------------------------------------------------------------

UI = {
    "en": {"nav": {"index": "Home", "about": "About", "courses": "Courses", "how-to-learn": "How to learn",
                   "admissions": "Admissions", "contact": "Contact", "faq": "FAQ", "privacy": "Privacy",
                   "terms": "Terms", "library": "Library", "bookstore": "Bookstore", "portal": "Dashboard",
                   "assistant": "AI assistant", "syllabus": "Syllabus"},
           "not_open": "Not yet open",
           "menu": "Menu", "skip": "Skip to content", "preview": "Preview — this website is not yet published.",
           "tagline": "Biblical Truth • Theological Depth • Ministry Formation",
           "foot_about": "An online school for Bible, theology and ministry skills, taught through WhatsApp and PDF lessons.",
           "foot_links": "Pages", "foot_contact": "Contact", "wa": "WhatsApp", "copy": "Online Bible & Theology School",
           "modules": "modules", "tba": "Fees and start date: to be announced", "soon": "Registration not yet open",
           "open": "Registration enquiries open", "ask": "Ask on WhatsApp", "lang_label": "Language"},
    "sw": {"nav": {"index": "Mwanzo", "about": "Kuhusu", "courses": "Kozi", "how-to-learn": "Jinsi ya kujifunza",
                   "admissions": "Usajili", "contact": "Mawasiliano", "faq": "Maswali", "privacy": "Faragha",
                   "terms": "Masharti", "library": "Maktaba", "bookstore": "Duka la vitabu", "portal": "Dashboard",
                   "assistant": "Msaidizi wa AI", "syllabus": "Mtaala"},
           "not_open": "Bado haijafunguliwa",
           "menu": "Menyu", "skip": "Ruka hadi maudhui", "preview": "Onyesho la awali — tovuti hii bado haijachapishwa.",
           "tagline": "Biblical Truth • Theological Depth • Ministry Formation",
           "foot_about": "Shule ya mtandaoni ya Biblia, theolojia na ujuzi wa huduma, inayofundisha kupitia WhatsApp na masomo ya PDF.",
           "foot_links": "Kurasa", "foot_contact": "Mawasiliano", "wa": "WhatsApp", "copy": "Online Bible & Theology School",
           "modules": "moduli", "tba": "Ada na tarehe ya kuanza: zitatangazwa", "soon": "Usajili bado haujafunguliwa",
           "open": "Maswali ya usajili yanapokelewa", "ask": "Uliza kwa WhatsApp", "lang_label": "Lugha"},
    "fr": {"nav": {"index": "Accueil", "about": "À propos", "courses": "Cours", "how-to-learn": "Comment apprendre",
                   "admissions": "Inscription", "contact": "Contact", "faq": "Questions", "privacy": "Confidentialité",
                   "terms": "Conditions", "library": "Bibliothèque", "bookstore": "Librairie", "portal": "Tableau de bord",
                   "assistant": "Assistant IA", "syllabus": "Programme"},
           "not_open": "Pas encore ouvert",
           "menu": "Menu", "skip": "Aller au contenu", "preview": "Aperçu — ce site n'est pas encore publié.",
           "tagline": "Biblical Truth • Theological Depth • Ministry Formation",
           "foot_about": "Une école en ligne de Bible, de théologie et de compétences pour le ministère, par WhatsApp et des leçons en PDF.",
           "foot_links": "Pages", "foot_contact": "Contact", "wa": "WhatsApp", "copy": "Online Bible & Theology School",
           "modules": "modules", "tba": "Frais et date de début : à annoncer", "soon": "Inscriptions pas encore ouvertes",
           "open": "Demandes d'inscription ouvertes", "ask": "Demander sur WhatsApp", "lang_label": "Langue"},
}


def wa_link(command=""):
    return f"https://wa.me/{WHATSAPP}" + ("?" + urlencode({"text": command}) if command else "")


def course_cards(lang, link_prefix=""):
    ui = UI[lang]
    cards = []
    for course in COURSES:
        status = (f'<span class="tag">{e(ui["open"])}</span><span class="tag wait">{e(ui["tba"])}</span>' if course["open"]
                  else f'<span class="tag wait">{e(ui["soon"])}</span>')
        cards.append(f'<article class="card{"" if course["open"] else " gold"}" id="{course["code"].lower()}">'
                     f'<h3>{e(course["name"][lang])}</h3><p>{status}<span class="tag">{course["modules"]} {e(ui["modules"])}'
                     f'</span></p><p>{e(course["text"][lang])}</p></article>')
    return '<div class="grid">' + "".join(cards) + "</div>"


# ------------------------------------------------------------
# Online services: library, bookstore, student dashboard, AI assistant.
# The library and student portal are verified on production. Bookstore
# and paid AI services remain closed. Lesson publication is separate.
# ------------------------------------------------------------

SERVICES = ("library", "bookstore", "portal", "assistant")

# Existing backend endpoints. No credentials or student links belong in source.
CAMPUS_ORIGIN = "https://odm-ai-asistant.onrender.com"
CAMPUS_TEXT = {
    "en": {"title": "Have your personal student link?", "label": "Your OBTS dashboard link",
           "help": "Paste the personal link sent to your WhatsApp. It opens your existing account; you do not need to register again. An expired link must be renewed through OBTS WhatsApp.",
           "button": "Open my dashboard", "library": "Open my library", "error": "Use the complete personal dashboard link sent by OBTS. Do not enter a password or a phone number.",
           "privacy": "Your link is checked on this device and is not saved by this website. Keep it private."},
    "sw": {"title": "Una kiungo chako cha mwanafunzi?", "label": "Kiungo chako cha dashboard ya OBTS",
           "help": "Bandika kiungo binafsi ulichotumiwa WhatsApp. Kitafungua akaunti yako iliyopo; huhitaji kujisajili upya. Kiungo kilichokwisha muda kinaombwa upya kupitia WhatsApp ya OBTS.",
           "button": "Fungua dashboard yangu", "library": "Fungua maktaba yangu", "error": "Tumia kiungo kamili cha dashboard ulichotumiwa na OBTS. Usiweke nenosiri wala namba ya simu.",
           "privacy": "Kiungo kinakaguliwa kwenye kifaa hiki na hakihifadhiwi na website. Kiweke kwa siri."},
    "fr": {"title": "Vous avez votre lien personnel étudiant ?", "label": "Votre lien du tableau de bord OBTS",
           "help": "Collez le lien personnel reçu sur WhatsApp. Il ouvre votre compte existant ; aucune nouvelle inscription n’est nécessaire. Demandez un nouveau lien sur WhatsApp OBTS si le vôtre a expiré.",
           "button": "Ouvrir mon tableau de bord", "library": "Ouvrir ma bibliothèque", "error": "Utilisez le lien personnel complet du tableau de bord envoyé par OBTS. Ne saisissez ni mot de passe ni numéro de téléphone.",
           "privacy": "Le lien est vérifié sur cet appareil et n'est pas enregistré par ce site. Gardez-le privé."},
}

CAMPUS_REQUEST = {
    'sw': ('Pata kiungo chako binafsi', 'Omba kiungo cha dashboard', 'Omba kiungo cha maktaba',
           'Bofya kitufe kisha tuma ujumbe uliowekwa kwenye WhatsApp ya shule. Tumia namba uliyojisajilia. Mfumo utakutumia kiungo binafsi kinachodumu saa 24.',
           'Dashboard inapatikana. Nyenzo za masomo huonekana baada ya kutolewa na shule.'),
    'en': ('Get your personal link', 'Request my dashboard link', 'Request my library link',
           'Select the button and send the prepared message to OBTS WhatsApp from your registered number. The system replies with a private link valid for 24 hours.',
           'The dashboard is available. Lesson materials appear after the school releases them.'),
    'fr': ('Recevoir votre lien personnel', 'Demander mon lien du tableau de bord', 'Demander mon lien de bibliothèque',
           'Sélectionnez le bouton et envoyez le message préparé sur WhatsApp OBTS depuis votre numéro inscrit. Le système répond avec un lien personnel valable 24 heures.',
           'Le tableau de bord est disponible. Les documents apparaissent après leur publication par l’école.'),
}


def campus_entry(lang, page):
    origin = service_origin()
    if not origin:
        return ""
    w = CAMPUS_TEXT[lang]
    target = "/library" if page == "library" else "/dashboard"
    label = w["library"] if page == "library" else w["button"]
    request = CAMPUS_REQUEST[lang]
    command = "MAKTABA" if page == "library" else "DASHBOARD"
    request_label = request[2] if page == "library" else request[1]
    return f'''<section class="note"><h2>{e(request[0])}</h2><p>{e(request[3])}</p>
<p><a class="btn navy" href="{e(wa_link(command))}">{e(request_label)}</a></p>
<details><summary>{e(w["title"])}</summary><p>{e(w["help"])}</p>
<form id="campus-entry" data-origin="{origin}" data-target="{target}" data-language="{lang}" data-error="{e(w["error"])}" novalidate>
<div class="field"><label for="campus-link">{e(w["label"])}</label><input type="url" id="campus-link" autocomplete="off" autocapitalize="off" spellcheck="false" aria-describedby="campus-privacy" required></div>
<p class="error" role="alert"></p><button class="btn navy" type="submit" disabled>{e(label)}</button>
<p class="hint" id="campus-privacy">{e(w["privacy"])}</p>
<noscript><p><a href="{e(wa_link(command))}">{e(request_label)}</a></p></noscript></form></details></section>'''

SERVICE_STATUS = {
    "en": "Not yet open. This service has been built and tested in a test environment; it opens only when the school approves the launch. Until then, ask on WhatsApp.",
    "sw": "Bado haijafunguliwa. Huduma hii imejengwa na kujaribiwa kwenye mazingira ya majaribio; itafunguliwa tu shule itakapoidhinisha uzinduzi. Hadi wakati huo, uliza kwa WhatsApp.",
    "fr": "Pas encore ouvert. Ce service a été construit et testé dans un environnement de test ; il ouvrira seulement lorsque l'école approuvera le lancement. D'ici là, demandez sur WhatsApp.",
}

SERVICE_TEXT = {
    "en": {
        "heading": "Online services",
        "cards": {"library": "Books, study guides and course materials by language, course and module.",
                  "bookstore": "Approved OBTS books with a description, an allowed sample and an approved price.",
                  "portal": "Your courses, next lesson, progress, tasks, feedback and purchased books.",
                  "assistant": "Help to understand a lesson, practise an exercise and build your AI course project."},
        "library": ("Library", "Books, study guides and course materials, organised by language, course and module.",
                    """<h2>What you will find</h2><div class="grid">
<div class="card"><h3>Free for everyone</h3><p>Published materials that anyone may read.</p></div>
<div class="card"><h3>Approved lessons</h3><p>Lessons that a lecturer has approved, open to students registered in that course.</p></div>
<div class="card gold"><h3>Books for sale</h3><p>OBTS books listed in the <a href="bookstore.html">bookstore</a>.</p></div>
<div class="card"><h3>Lecturer materials</h3><p>Guides for lecturers. They are not shown to the public.</p></div></div>
<p>Materials that have not yet been approved are never shown in the library.</p>
<h2>How you will search</h2><ul><li>By title or word.</li><li>By language: English, Kiswahili or French.</li><li>By course and module.</li><li>Each item shows its access: free, registered students, for sale, or lecturers only.</li></ul>"""),
        "bookstore": ("Bookstore", "How OBTS books will be sold.",
                      """<div class="note">No book is on sale yet.</div>
<h2>Before a book is sold</h2><ol class="steps"><li>The book goes through idea, outline, chapters, sources, review, cover and PDF, and is approved.</li>
<li>The school approves the sample you may read before buying.</li><li>The school approves the price.</li></ol>
<h2>How you will buy</h2><ol class="steps"><li>Read the book's page: description, sample and approved price.</li>
<li>Order with your WhatsApp number; you receive an order number and the amount.</li>
<li>Pay with the payment method announced by OBTS and send the transaction number.</li>
<li>A member of the finance staff verifies the payment; then the book is sent to you and the delivery is recorded.</li></ol>"""),
        "portal": ("Student dashboard", "One page for your studies.",
                   """<h2>What it shows</h2><div class="grid">
<div class="card"><h3>Courses and progress</h3><p>The courses you may open and where you are in each.</p></div>
<div class="card"><h3>Next lesson</h3><p>The lesson to study next.</p></div>
<div class="card"><h3>Tasks and feedback</h3><p>The tasks you sent and your lecturer's feedback. A mark is shown only when a lecturer gave it.</p></div>
<div class="card gold"><h3>Library and books</h3><p>Materials for your courses and the books you bought.</p></div></div>
<h2>How you will open it</h2><p>A personal link is sent to your own WhatsApp number. The link works for a limited time; ask for a new one when it expires.</p>
<h2>Lecturers and administrators</h2><p>Staff sign in separately. Each role sees only what it is allowed to: drafts, reviews, approvals, translations, students and deliveries.</p>"""),
        "assistant": ("AI study assistant", "An assistant for your studies that uses only the school's materials.",
                      """<h2>What it does</h2><ul><li>Explains a lesson you have access to.</li><li>Guides you through an exercise with hints, without giving the answers.</li>
<li>Helps with your AI course project: report, content, video, audio or website.</li><li>Helps lecturers draft a book outline.</li></ul>
<h2>Its rules</h2><ul><li>It answers only from materials the school allows, and names its source.</li><li>When the materials do not answer your question, it says so.</li>
<li>It never invents marks, payments, approvals or progress: those come from the school's records.</li></ul>
<h2>Cost and limits</h2><p>Each question is one request to an AI model, and there is a daily limit of requests. The cost for students and the number of requests per day will be announced before the service opens.</p>"""),
    },
    "sw": {
        "heading": "Huduma za mtandaoni",
        "cards": {"library": "Vitabu, miongozo na vifaa vya kozi kwa lugha, kozi na moduli.",
                  "bookstore": "Vitabu vya OBTS vilivyoidhinishwa, vyenye maelezo, sampuli iliyoruhusiwa na bei iliyopitishwa.",
                  "portal": "Kozi zako, somo linalofuata, maendeleo, kazi, mrejesho na vitabu ulivyonunua.",
                  "assistant": "Msaada wa kuelewa somo, kufanya zoezi na kujenga mradi wa kozi ya AI."},
        "library": ("Maktaba", "Vitabu, miongozo na vifaa vya kozi, vimepangwa kwa lugha, kozi na moduli.",
                    """<h2>Utakachokipata</h2><div class="grid">
<div class="card"><h3>Bure kwa wote</h3><p>Nyenzo zilizochapishwa ambazo kila mtu anaweza kusoma.</p></div>
<div class="card"><h3>Masomo yaliyoidhinishwa</h3><p>Masomo yaliyoidhinishwa na mhadhiri, kwa wanafunzi waliosajiliwa kwenye kozi husika.</p></div>
<div class="card gold"><h3>Vitabu vya kuuza</h3><p>Vitabu vya OBTS vilivyo kwenye <a href="bookstore.html">duka la vitabu</a>.</p></div>
<div class="card"><h3>Vifaa vya wahadhiri</h3><p>Miongozo ya wahadhiri. Haionyeshwi kwa umma.</p></div></div>
<p>Nyenzo ambazo bado hazijaidhinishwa hazionyeshwi kwenye maktaba kamwe.</p>
<h2>Utakavyotafuta</h2><ul><li>Kwa kichwa au neno.</li><li>Kwa lugha: Kiingereza, Kiswahili au Kifaransa.</li><li>Kwa kozi na moduli.</li><li>Kila nyenzo inaonyesha hali ya ufikiaji: bure, wanafunzi waliosajiliwa, inauzwa, au wahadhiri tu.</li></ul>"""),
        "bookstore": ("Duka la vitabu", "Jinsi vitabu vya OBTS vitakavyouzwa.",
                      """<div class="note">Hakuna kitabu kinachouzwa kwa sasa.</div>
<h2>Kabla kitabu hakijauzwa</h2><ol class="steps"><li>Kitabu kinapita wazo, outline, sura, vyanzo, ukaguzi, jalada na PDF, kisha kinaidhinishwa.</li>
<li>Shule inaidhinisha sampuli utakayoweza kusoma kabla ya kununua.</li><li>Shule inapitisha bei.</li></ol>
<h2>Utakavyonunua</h2><ol class="steps"><li>Soma ukurasa wa kitabu: maelezo, sampuli na bei iliyopitishwa.</li>
<li>Agiza kwa namba yako ya WhatsApp; unapokea namba ya oda na kiasi.</li>
<li>Lipa kwa njia ya malipo iliyotangazwa na OBTS na utume namba ya muamala.</li>
<li>Mfanyakazi wa fedha anathibitisha malipo; kisha kitabu kinatumwa kwako na utoaji unarekodiwa.</li></ol>"""),
        "portal": ("Dashboard ya mwanafunzi", "Ukurasa mmoja wa masomo yako.",
                   """<h2>Inachoonyesha</h2><div class="grid">
<div class="card"><h3>Kozi na maendeleo</h3><p>Kozi unazoweza kufungua na ulipofikia katika kila moja.</p></div>
<div class="card"><h3>Somo linalofuata</h3><p>Somo la kusoma baadaye.</p></div>
<div class="card"><h3>Kazi na mrejesho</h3><p>Kazi ulizotuma na mrejesho wa mhadhiri wako. Alama inaonyeshwa tu mhadhiri akiitoa.</p></div>
<div class="card gold"><h3>Maktaba na vitabu</h3><p>Nyenzo za kozi zako na vitabu ulivyonunua.</p></div></div>
<h2>Utakavyoifungua</h2><p>Kiungo binafsi kinatumwa kwenye namba yako ya WhatsApp. Kiungo kinafanya kazi kwa muda maalum; omba kipya kikiisha muda.</p>
<h2>Wahadhiri na wasimamizi</h2><p>Wafanyakazi wanaingia kwa njia yao. Kila nafasi inaona tu inachoruhusiwa: rasimu, mapitio, idhini, tafsiri, wanafunzi na utoaji.</p>"""),
        "assistant": ("Msaidizi wa AI wa masomo", "Msaidizi wa masomo yako anayetumia nyenzo za shule tu.",
                      """<h2>Anachofanya</h2><ul><li>Anaeleza somo ambalo una ufikiaji wake.</li><li>Anakuongoza kwenye zoezi kwa vidokezo, bila kukupa majibu.</li>
<li>Anasaidia mradi wako wa kozi ya AI: ripoti, maudhui, video, audio au tovuti.</li><li>Anawasaidia wahadhiri kuandaa outline ya kitabu.</li></ul>
<h2>Kanuni zake</h2><ul><li>Anajibu kutoka kwenye nyenzo zinazoruhusiwa na shule tu, na anataja chanzo.</li><li>Nyenzo zisipojibu swali lako, anasema hivyo.</li>
<li>Habuni alama, malipo, idhini wala maendeleo: hayo yanatoka kwenye rekodi za shule.</li></ul>
<h2>Gharama na mipaka</h2><p>Kila swali ni ombi moja kwa modeli ya AI, na kuna kikomo cha maombi kwa siku. Gharama kwa mwanafunzi na idadi ya maombi kwa siku zitatangazwa kabla huduma haijafunguliwa.</p>"""),
    },
    "fr": {
        "heading": "Services en ligne",
        "cards": {"library": "Livres, guides d'étude et documents de cours par langue, cours et module.",
                  "bookstore": "Des livres d'OBTS approuvés, avec une description, un extrait autorisé et un prix approuvé.",
                  "portal": "Vos cours, la prochaine leçon, vos progrès, vos tâches, les retours et vos livres achetés.",
                  "assistant": "De l'aide pour comprendre une leçon, faire un exercice et construire votre projet du cours d'IA."},
        "library": ("Bibliothèque", "Livres, guides d'étude et documents de cours, classés par langue, cours et module.",
                    """<h2>Ce que vous trouverez</h2><div class="grid">
<div class="card"><h3>Gratuit pour tous</h3><p>Des documents publiés que chacun peut lire.</p></div>
<div class="card"><h3>Leçons approuvées</h3><p>Des leçons approuvées par un enseignant, ouvertes aux étudiants inscrits au cours.</p></div>
<div class="card gold"><h3>Livres en vente</h3><p>Les livres d'OBTS présentés dans la <a href="bookstore.html">librairie</a>.</p></div>
<div class="card"><h3>Documents des enseignants</h3><p>Des guides pour les enseignants, non visibles du public.</p></div></div>
<p>Les documents qui ne sont pas encore approuvés ne sont jamais affichés dans la bibliothèque.</p>
<h2>Comment chercher</h2><ul><li>Par titre ou par mot.</li><li>Par langue : anglais, kiswahili ou français.</li><li>Par cours et par module.</li><li>Chaque document indique son accès : gratuit, étudiants inscrits, en vente ou enseignants seulement.</li></ul>"""),
        "bookstore": ("Librairie", "Comment les livres d'OBTS seront vendus.",
                      """<div class="note">Aucun livre n'est encore en vente.</div>
<h2>Avant qu'un livre soit vendu</h2><ol class="steps"><li>Le livre passe par l'idée, le plan, les chapitres, les sources, la révision, la couverture et le PDF, puis il est approuvé.</li>
<li>L'école approuve l'extrait que vous pourrez lire avant d'acheter.</li><li>L'école approuve le prix.</li></ol>
<h2>Comment acheter</h2><ol class="steps"><li>Lisez la page du livre : description, extrait et prix approuvé.</li>
<li>Commandez avec votre numéro WhatsApp ; vous recevez un numéro de commande et le montant.</li>
<li>Payez par le moyen de paiement annoncé par OBTS et envoyez le numéro de transaction.</li>
<li>Un membre du service financier vérifie le paiement ; le livre vous est alors envoyé et la livraison est enregistrée.</li></ol>"""),
        "portal": ("Tableau de bord de l'étudiant", "Une seule page pour vos études.",
                   """<h2>Ce qu'il affiche</h2><div class="grid">
<div class="card"><h3>Cours et progrès</h3><p>Les cours que vous pouvez ouvrir et où vous en êtes dans chacun.</p></div>
<div class="card"><h3>Prochaine leçon</h3><p>La leçon à étudier ensuite.</p></div>
<div class="card"><h3>Tâches et retours</h3><p>Les tâches envoyées et les retours de votre enseignant. Une note n'apparaît que si un enseignant l'a donnée.</p></div>
<div class="card gold"><h3>Bibliothèque et livres</h3><p>Les documents de vos cours et les livres achetés.</p></div></div>
<h2>Comment l'ouvrir</h2><p>Un lien personnel est envoyé à votre propre numéro WhatsApp. Il fonctionne pendant une durée limitée ; demandez-en un nouveau lorsqu'il expire.</p>
<h2>Enseignants et administrateurs</h2><p>Le personnel se connecte séparément. Chaque rôle ne voit que ce qui lui est permis : brouillons, révisions, approbations, traductions, étudiants et livraisons.</p>"""),
        "assistant": ("Assistant d'étude IA", "Un assistant pour vos études qui n'utilise que les documents de l'école.",
                      """<h2>Ce qu'il fait</h2><ul><li>Il explique une leçon à laquelle vous avez accès.</li><li>Il vous guide dans un exercice par des indices, sans donner les réponses.</li>
<li>Il aide votre projet du cours d'IA : rapport, contenu, vidéo, audio ou site web.</li><li>Il aide les enseignants à préparer le plan d'un livre.</li></ul>
<h2>Ses règles</h2><ul><li>Il répond seulement à partir des documents autorisés par l'école et cite sa source.</li><li>Quand les documents ne répondent pas à votre question, il le dit.</li>
<li>Il n'invente jamais de notes, de paiements, d'approbations ni de progrès : ils viennent des registres de l'école.</li></ul>
<h2>Coût et limites</h2><p>Chaque question est une requête à un modèle d'IA, avec une limite quotidienne de requêtes. Le coût pour les étudiants et le nombre de requêtes par jour seront annoncés avant l'ouverture du service.</p>"""),
    },
}


OPEN_LIBRARY = {"en": "Open the library", "sw": "Fungua maktaba", "fr": "Ouvrir la bibliothèque"}


def service_origin():
    """Fail closed unless the enabled address is the exact known HTTPS production origin."""
    if not SERVICE_BASE:
        return ""
    url = urlsplit(SERVICE_BASE)
    if (url.scheme != "https" or url.netloc != urlsplit(CAMPUS_ORIGIN).netloc
            or url.username or url.password or url.path not in ("", "/") or url.query or url.fragment):
        raise ValueError("SERVICE_BASE must be the verified production origin; staging and other origins are refused")
    return CAMPUS_ORIGIN


def library_url(lang):
    """The system's own library page in the same language (portal_routes.library_page reads ?lang=en|sw|fr)."""
    origin = service_origin()
    return f"{origin}/library?lang={lang}" if origin else ""


def is_open(page):
    return page in ("library", "portal") and bool(service_origin())


def services_grid(lang):
    ui, text = UI[lang], SERVICE_TEXT[lang]
    cards = "".join(f'<article class="card"><h3><a href="{p}.html">{e(ui["nav"][p])}</a></h3>'
                    + ("" if is_open(p) else f'<p><span class="tag wait">{e(ui["not_open"])}</span></p>')
                    + f'<p>{e(text["cards"][p])}</p></article>'
                    for p in SERVICES)
    return f'<section class="section"><h2>{e(text["heading"])}</h2><div class="grid">{cards}</div></section>'


def service_page(lang, page):
    title, intro, html_body = SERVICE_TEXT[lang][page]
    if is_open(page):
        browse = (f'<p><a class="btn navy" href="{e(library_url(lang))}">{e(OPEN_LIBRARY[lang])}</a></p>'
                  if page == 'library' else '')
        return title, intro, (f'<p class="note">{e(CAMPUS_REQUEST[lang][4])}</p>' + browse
                              + campus_entry(lang, page) + html_body + f'<p><a class="btn navy" href="{wa_link()}">{e(UI[lang]["ask"])}</a></p>')
    status = (f'<div class="note gold"><strong>{e(UI[lang]["not_open"])}.</strong> {e(SERVICE_STATUS[lang].split(". ", 1)[1])}'
              f' <a href="{wa_link()}">{e(UI[lang]["ask"])}</a></div>')
    entry = campus_entry(lang, page) if page in ("portal", "library") else ""
    return title, intro, status + entry + html_body + f'<p><a class="btn navy" href="{wa_link()}">{e(UI[lang]["ask"])}</a></p>'


# ------------------------------------------------------------
# Page bodies
# ------------------------------------------------------------

def body(lang, page):
    ui = UI[lang]
    wa = wa_link()
    if lang == "en":
        content = {
            "index": ("Online Bible & Theology School",
                      f'''<section class="hero"><div class="wrap"><div><div class="kicker">{e(ui["tagline"])}</div>
<h1>Study the Bible, theology and ministry skills from your phone</h1>
<p class="lead">OBTS is an online school. Lessons come to you as PDF files on WhatsApp, each with clear objectives, a timed study plan, exercises and a task your tutor reviews.</p>
<div class="actions"><a class="btn" href="admissions.html">Register your interest</a><a class="btn secondary" href="courses.html">See the courses</a></div></div>
<img class="seal" src="{{assets}}img/obts-seal-192.png" width="192" height="192" alt="OBTS seal"></div></section>
<div class="wrap"><section class="section"><h2>What you can study</h2>{course_cards(lang)}</section>
<section class="section"><h2>How a lesson works</h2><ol class="steps">
<li>You receive the lesson as a PDF on WhatsApp.</li><li>You follow the study plan: reading, Scripture or examples, and exercises.</li>
<li>You send your task to your tutor on WhatsApp (text, or a voice message for the English courses).</li>
<li>After sending your task, you open the answer key and receive feedback.</li></ol>
<p><a href="how-to-learn.html">More about how to learn</a></p></section>
<div class="note gold">Fees and start dates have not yet been announced. Ask on <a href="{wa}">WhatsApp</a> and admissions will reply when they are confirmed.</div></div>'''),
            "about": ("About OBTS", "OBTS is an online school for Bible, theology and practical ministry skills.",
                      f'''<p>The Online Bible &amp; Theology School (OBTS) teaches through lessons that a student can follow on an ordinary phone. The motto in its logo — <em>Biblical Truth • Theological Depth • Ministry Formation</em> — describes what the school aims at: understanding Scripture well, thinking carefully about Christian doctrine, and growing in the skills of ministry and service.</p>
<h2>How OBTS teaches</h2><div class="grid">
<div class="card"><h3>Structured lessons</h3><p>Every lesson states its objectives, gives a study plan in minutes, and ends with a task that shows what you learned.</p></div>
<div class="card"><h3>Reviewed content</h3><p>Lessons are written, checked against their sources and reviewed by a lecturer before they are sent to students. Draft lessons are never sent.</p></div>
<div class="card"><h3>Three languages</h3><p>The website is in English, Kiswahili and French. The first 25 lessons of General Bible Studies &amp; Theology (modules 1–3) have been written in all three languages and are being reviewed by lecturers; once approved, you receive them in the language you choose when you register. The other courses are written first in English (the AI course in Kiswahili); their Kiswahili and French versions are being prepared and reviewed.</p></div></div>
<h2>Courses</h2><p>OBTS offers six courses, and a seventh on practical AI is being prepared. See <a href="courses.html">Courses</a>.</p>'''),
            "courses": ("Courses", "Seven courses, each divided into modules and taught lesson by lesson.",
                        f'''{course_cards(lang)}
<div class="note"><strong>Language of the lessons.</strong> General Bible Studies &amp; Theology (GB): lessons 1–25 (modules 1–3) have been written in English, Kiswahili and French and are being reviewed by lecturers. A lesson is sent only after a lecturer has approved it in that language; the student then receives it in the language chosen at registration, as a PDF lesson and summary pages on WhatsApp. B66, PE, ES, CL and ENT are written first in English and the AI course in Kiswahili; their Kiswahili and French versions are being prepared and checked, so ask admissions which language is available. Pastoral English and English Speaking teach English, so their exercises stay in English.</div>
<div class="note gold">Fees, start dates and the number of courses you may take at the same time will be announced by admissions. <a href="{wa}">Ask on WhatsApp</a>.</div>'''),
            "how-to-learn": ("How to learn with OBTS", "What you need, what a lesson contains and how you send your work.",
                             '''<h2>What you need</h2><ul><li>A phone with WhatsApp and a PDF reader.</li><li>A Bible for the Bible and theology courses.</li><li>A quiet time for each lesson: most lessons are planned for 40 to 90 minutes.</li></ul>
<h2>What a lesson contains</h2><div class="grid">
<div class="card"><h3>Objectives</h3><p>What you will be able to do at the end of the lesson.</p></div>
<div class="card"><h3>Study plan</h3><p>Steps with the minutes for each, so you know how to use your time.</p></div>
<div class="card"><h3>Teaching and exercises</h3><p>Explanations, Scripture references or examples, and practice with answers you check later.</p></div>
<div class="card gold"><h3>Task</h3><p>Short written answers, or voice messages in the English courses, that you send to your tutor.</p></div></div>
<h2>Step by step</h2><ol class="steps">
<li>Read the objectives and follow the study plan.</li>
<li>Do the exercises without looking at the answers.</li>
<li>Send your task to your tutor on WhatsApp.</li>
<li>Only then open the answer key and compare your answers.</li>
<li>Read your tutor's feedback before the next lesson.</li></ol>
<h2>English courses</h2><p>Pastoral English and English Speaking begin with a short placement recording: you speak for about one minute before the first lesson, so your tutor knows where you start. It is not an examination.</p>'''),
            "admissions": ("Admissions", "Tell us who you are and which course interests you. The form opens WhatsApp with your message ready to send.",
                           None),
            "contact": ("Contact", "WhatsApp is the official way to reach OBTS.",
                        f'''<div class="grid"><div class="card gold"><h3>WhatsApp</h3><p><strong>{WHATSAPP_DISPLAY}</strong></p><p>For admissions, questions about courses and support for students.</p><p><a class="btn navy" href="{wa}">Open WhatsApp</a></p></div>
<div class="card"><h3>Website</h3><p>{DOMAIN}</p><p>Other contact channels will be added here only when they are confirmed.</p></div></div>'''),
            "faq": ("Frequently asked questions", "Short answers to common questions.", None),
            "privacy": ("Privacy policy", "How OBTS uses the information you send.", None),
            "terms": ("Terms of use", "The conditions for using this website and OBTS materials.", None),
        }
    elif lang == "sw":
        content = {
            "index": ("Online Bible & Theology School",
                      f'''<section class="hero"><div class="wrap"><div><div class="kicker">{e(ui["tagline"])}</div>
<h1>Jifunze Biblia, theolojia na ujuzi wa huduma kwa simu yako</h1>
<p class="lead">OBTS ni shule ya mtandaoni. Masomo yanakufikia kama faili za PDF kwenye WhatsApp, kila moja likiwa na malengo yaliyo wazi, mpango wa kujifunza wenye dakika, mazoezi na kazi inayopitiwa na mkufunzi wako.</p>
<div class="actions"><a class="btn" href="admissions.html">Onyesha nia ya kujiunga</a><a class="btn secondary" href="courses.html">Tazama kozi</a></div></div>
<img class="seal" src="{{assets}}img/obts-seal-192.png" width="192" height="192" alt="Nembo ya OBTS"></div></section>
<div class="wrap"><section class="section"><h2>Unachoweza kujifunza</h2>{course_cards(lang)}</section>
<section class="section"><h2>Somo linavyofanya kazi</h2><ol class="steps">
<li>Unapokea somo kama PDF kwenye WhatsApp.</li><li>Unafuata mpango wa kujifunza: kusoma, Maandiko au mifano, na mazoezi.</li>
<li>Unamtumia mkufunzi wako kazi kwa WhatsApp (maandishi, au ujumbe wa sauti kwa kozi za Kiingereza).</li>
<li>Baada ya kutuma kazi, unafungua majibu na kupokea mrejesho.</li></ol>
<p><a href="how-to-learn.html">Zaidi kuhusu jinsi ya kujifunza</a></p></section>
<div class="note gold">Ada na tarehe za kuanza bado hazijatangazwa. Uliza kwa <a href="{wa}">WhatsApp</a> na ofisi ya usajili itakujibu zikithibitishwa.</div></div>'''),
            "about": ("Kuhusu OBTS", "OBTS ni shule ya mtandaoni ya Biblia, theolojia na ujuzi wa vitendo wa huduma.",
                      f'''<p>Online Bible &amp; Theology School (OBTS) inafundisha kupitia masomo ambayo mwanafunzi anaweza kuyafuata kwa simu ya kawaida. Kauli mbiu iliyo kwenye nembo yake — <em>Biblical Truth • Theological Depth • Ministry Formation</em> (Ukweli wa Biblia • Kina cha Theolojia • Malezi ya Huduma) — inaeleza lengo la shule: kuyaelewa Maandiko vizuri, kufikiri kwa makini kuhusu mafundisho ya Kikristo, na kukua katika ujuzi wa huduma.</p>
<h2>OBTS inavyofundisha</h2><div class="grid">
<div class="card"><h3>Masomo yenye mpangilio</h3><p>Kila somo linataja malengo yake, linatoa mpango wa kujifunza kwa dakika, na linamalizika kwa kazi inayoonyesha ulichojifunza.</p></div>
<div class="card"><h3>Maudhui yaliyokaguliwa</h3><p>Masomo yanaandikwa, yanalinganishwa na vyanzo vyake na kukaguliwa na mhadhiri kabla ya kutumwa kwa wanafunzi. Rasimu hazitumwi kamwe.</p></div>
<div class="card"><h3>Lugha tatu</h3><p>Tovuti iko kwa Kiingereza, Kiswahili na Kifaransa. Masomo 25 ya kwanza ya Mafunzo ya Jumla ya Biblia na Theolojia (moduli 1–3) yameandikwa kwa lugha zote tatu na yanakaguliwa na wahadhiri; yakishaidhinishwa, unayapokea kwa lugha utakayochagua wakati wa kujisajili. Kozi nyingine zinaandikwa kwanza kwa Kiingereza (kozi ya AI kwa Kiswahili); matoleo yake ya Kiswahili na Kifaransa yanaandaliwa na kukaguliwa.</p></div></div>
<h2>Kozi</h2><p>OBTS inatoa kozi sita, na ya saba kuhusu matumizi ya AI inaandaliwa. Tazama <a href="courses.html">Kozi</a>.</p>'''),
            "courses": ("Kozi", "Kozi saba, kila moja imegawanywa katika moduli na kufundishwa somo kwa somo.",
                        f'''{course_cards(lang)}
<div class="note"><strong>Lugha ya masomo.</strong> Mafunzo ya Jumla ya Biblia na Theolojia (GB): masomo 1–25 (moduli 1–3) yameandikwa kwa Kiingereza, Kiswahili na Kifaransa na yanakaguliwa na wahadhiri. Somo linatumwa tu baada ya mhadhiri kuliidhinisha kwa lugha hiyo; kisha mwanafunzi analipokea kwa lugha aliyoichagua wakati wa kujisajili, kama somo la PDF pamoja na kurasa za muhtasari kwenye WhatsApp. B66, PE, ES, CL na ENT zinaandikwa kwanza kwa Kiingereza na kozi ya AI kwa Kiswahili; matoleo yake ya Kiswahili na Kifaransa yanaandaliwa na kukaguliwa, hivyo uliza ofisi ya usajili lugha inayopatikana. Kiingereza cha Kichungaji na Kuzungumza Kiingereza vinafundisha Kiingereza, hivyo mazoezi yake yanabaki kwa Kiingereza.</div>
<div class="note gold">Ada, tarehe za kuanza na idadi ya kozi unazoweza kusoma kwa wakati mmoja zitatangazwa na ofisi ya usajili. <a href="{wa}">Uliza kwa WhatsApp</a>.</div>'''),
            "how-to-learn": ("Jinsi ya kujifunza na OBTS", "Unachohitaji, kilichomo kwenye somo na jinsi ya kutuma kazi yako.",
                             '''<h2>Unachohitaji</h2><ul><li>Simu yenye WhatsApp na programu ya kusoma PDF.</li><li>Biblia kwa kozi za Biblia na theolojia.</li><li>Muda wa utulivu kwa kila somo: masomo mengi yamepangwa kwa dakika 40 hadi 90.</li></ul>
<h2>Kilichomo kwenye somo</h2><div class="grid">
<div class="card"><h3>Malengo</h3><p>Utakachoweza kufanya mwisho wa somo.</p></div>
<div class="card"><h3>Mpango wa kujifunza</h3><p>Hatua pamoja na dakika za kila moja, ili ujue jinsi ya kutumia muda wako.</p></div>
<div class="card"><h3>Mafundisho na mazoezi</h3><p>Maelezo, marejeo ya Maandiko au mifano, na mazoezi ambayo majibu yake unayakagua baadaye.</p></div>
<div class="card gold"><h3>Kazi</h3><p>Majibu mafupi ya maandishi, au jumbe za sauti kwa kozi za Kiingereza, unazomtumia mkufunzi wako.</p></div></div>
<h2>Hatua kwa hatua</h2><ol class="steps">
<li>Soma malengo na ufuate mpango wa kujifunza.</li>
<li>Fanya mazoezi bila kuangalia majibu.</li>
<li>Mtumie mkufunzi wako kazi kwa WhatsApp.</li>
<li>Hapo ndipo ufungue majibu na kulinganisha majibu yako.</li>
<li>Soma mrejesho wa mkufunzi wako kabla ya somo linalofuata.</li></ol>
<h2>Kozi za Kiingereza</h2><p>Kiingereza cha Kichungaji na Kuzungumza Kiingereza zinaanza kwa kurekodi sauti fupi ya upimaji: unazungumza kwa takriban dakika moja kabla ya somo la kwanza, ili mkufunzi wako ajue unapoanzia. Si mtihani.</p>'''),
            "admissions": ("Usajili", "Tueleze wewe ni nani na kozi gani inakuvutia. Fomu inafungua WhatsApp ukiwa na ujumbe tayari kutuma.", None),
            "contact": ("Mawasiliano", "WhatsApp ndiyo njia rasmi ya kuwasiliana na OBTS.",
                        f'''<div class="grid"><div class="card gold"><h3>WhatsApp</h3><p><strong>{WHATSAPP_DISPLAY}</strong></p><p>Kwa usajili, maswali kuhusu kozi na msaada kwa wanafunzi.</p><p><a class="btn navy" href="{wa}">Fungua WhatsApp</a></p></div>
<div class="card"><h3>Tovuti</h3><p>{DOMAIN}</p><p>Njia nyingine za mawasiliano zitaongezwa hapa tu zitakapothibitishwa.</p></div></div>'''),
            "faq": ("Maswali yanayoulizwa mara kwa mara", "Majibu mafupi kwa maswali ya kawaida.", None),
            "privacy": ("Sera ya faragha", "OBTS inavyotumia taarifa unazotuma.", None),
            "terms": ("Masharti ya matumizi", "Masharti ya kutumia tovuti hii na vifaa vya OBTS.", None),
        }
    else:
        content = {
            "index": ("Online Bible & Theology School",
                      f'''<section class="hero"><div class="wrap"><div><div class="kicker">{e(ui["tagline"])}</div>
<h1>Étudiez la Bible, la théologie et le ministère depuis votre téléphone</h1>
<p class="lead">OBTS est une école en ligne. Les leçons vous parviennent en PDF sur WhatsApp, chacune avec des objectifs clairs, un plan d'étude minuté, des exercices et une tâche que votre tuteur examine.</p>
<div class="actions"><a class="btn" href="admissions.html">Manifester votre intérêt</a><a class="btn secondary" href="courses.html">Voir les cours</a></div></div>
<img class="seal" src="{{assets}}img/obts-seal-192.png" width="192" height="192" alt="Sceau d'OBTS"></div></section>
<div class="wrap"><section class="section"><h2>Ce que vous pouvez étudier</h2>{course_cards(lang)}</section>
<section class="section"><h2>Comment se déroule une leçon</h2><ol class="steps">
<li>Vous recevez la leçon en PDF sur WhatsApp.</li><li>Vous suivez le plan d'étude : lecture, Écriture ou exemples, et exercices.</li>
<li>Vous envoyez votre tâche à votre tuteur sur WhatsApp (texte, ou message vocal pour les cours d'anglais).</li>
<li>Après l'envoi, vous ouvrez le corrigé et recevez un retour.</li></ol>
<p><a href="how-to-learn.html">En savoir plus sur la manière d'apprendre</a></p></section>
<div class="note gold">Les frais et les dates de début n'ont pas encore été annoncés. Demandez sur <a href="{wa}">WhatsApp</a> : le service des inscriptions répondra dès qu'ils seront confirmés.</div></div>'''),
            "about": ("À propos d'OBTS", "OBTS est une école en ligne de Bible, de théologie et de compétences pratiques pour le ministère.",
                      f'''<p>L'Online Bible &amp; Theology School (OBTS) enseigne au moyen de leçons qu'un étudiant peut suivre sur un téléphone ordinaire. La devise de son logo — <em>Biblical Truth • Theological Depth • Ministry Formation</em> (Vérité biblique • Profondeur théologique • Formation au ministère) — décrit son but : bien comprendre l'Écriture, réfléchir avec soin à la doctrine chrétienne et grandir dans les compétences du ministère.</p>
<h2>Comment OBTS enseigne</h2><div class="grid">
<div class="card"><h3>Des leçons structurées</h3><p>Chaque leçon indique ses objectifs, donne un plan d'étude en minutes et se termine par une tâche qui montre ce que vous avez appris.</p></div>
<div class="card"><h3>Un contenu révisé</h3><p>Les leçons sont écrites, vérifiées par rapport à leurs sources et révisées par un enseignant avant d'être envoyées aux étudiants. Les brouillons ne sont jamais envoyés.</p></div>
<div class="card"><h3>Trois langues</h3><p>Le site est en anglais, en kiswahili et en français. Les 25 premières leçons des Études bibliques générales et théologie (modules 1 à 3) ont été rédigées dans les trois langues et sont en cours de vérification par des enseignants ; une fois approuvées, vous les recevez dans la langue choisie lors de votre inscription. Les autres cours sont d'abord écrits en anglais (le cours d'IA en kiswahili) ; leurs versions en kiswahili et en français sont en préparation et en vérification.</p></div></div>
<h2>Cours</h2><p>OBTS propose six cours, et un septième sur l'usage pratique de l'IA est en préparation. Voir <a href="courses.html">Cours</a>.</p>'''),
            "courses": ("Cours", "Sept cours, chacun divisé en modules et enseigné leçon par leçon.",
                        f'''{course_cards(lang)}
<div class="note"><strong>Langue des leçons.</strong> Études bibliques générales et théologie (GB) : les leçons 1 à 25 (modules 1 à 3) ont été rédigées en anglais, en kiswahili et en français et sont en cours de vérification par des enseignants. Une leçon n'est envoyée qu'après son approbation par un enseignant dans cette langue ; l'étudiant la reçoit alors dans la langue choisie lors de l'inscription, sous forme de leçon PDF et de pages de résumé sur WhatsApp. B66, PE, ES, CL et ENT sont d'abord écrits en anglais et le cours d'IA en kiswahili ; leurs versions en kiswahili et en français sont en préparation et en vérification : demandez au service des inscriptions quelle langue est disponible. L'anglais pastoral et l'anglais oral enseignent l'anglais : leurs exercices restent en anglais.</div>
<div class="note gold">Les frais, les dates de début et le nombre de cours que vous pouvez suivre en même temps seront annoncés par le service des inscriptions. <a href="{wa}">Demandez sur WhatsApp</a>.</div>'''),
            "how-to-learn": ("Comment apprendre avec OBTS", "Ce dont vous avez besoin, le contenu d'une leçon et l'envoi de votre travail.",
                             '''<h2>Ce dont vous avez besoin</h2><ul><li>Un téléphone avec WhatsApp et un lecteur de PDF.</li><li>Une Bible pour les cours de Bible et de théologie.</li><li>Un moment calme pour chaque leçon : la plupart des leçons sont prévues pour 40 à 90 minutes.</li></ul>
<h2>Le contenu d'une leçon</h2><div class="grid">
<div class="card"><h3>Objectifs</h3><p>Ce que vous saurez faire à la fin de la leçon.</p></div>
<div class="card"><h3>Plan d'étude</h3><p>Des étapes avec leur durée, pour savoir comment utiliser votre temps.</p></div>
<div class="card"><h3>Enseignement et exercices</h3><p>Des explications, des références bibliques ou des exemples, et des exercices dont vous vérifiez les réponses ensuite.</p></div>
<div class="card gold"><h3>Tâche</h3><p>De courtes réponses écrites, ou des messages vocaux dans les cours d'anglais, que vous envoyez à votre tuteur.</p></div></div>
<h2>Étape par étape</h2><ol class="steps">
<li>Lisez les objectifs et suivez le plan d'étude.</li>
<li>Faites les exercices sans regarder les réponses.</li>
<li>Envoyez votre tâche à votre tuteur sur WhatsApp.</li>
<li>Ensuite seulement, ouvrez le corrigé et comparez vos réponses.</li>
<li>Lisez le retour de votre tuteur avant la leçon suivante.</li></ol>
<h2>Cours d'anglais</h2><p>L'anglais pastoral et l'anglais oral commencent par un court enregistrement de placement : vous parlez environ une minute avant la première leçon, pour que votre tuteur sache d'où vous partez. Ce n'est pas un examen.</p>'''),
            "admissions": ("Inscription", "Dites-nous qui vous êtes et quel cours vous intéresse. Le formulaire ouvre WhatsApp avec votre message prêt à envoyer.", None),
            "contact": ("Contact", "WhatsApp est le moyen officiel de joindre OBTS.",
                        f'''<div class="grid"><div class="card gold"><h3>WhatsApp</h3><p><strong>{WHATSAPP_DISPLAY}</strong></p><p>Pour les inscriptions, les questions sur les cours et le soutien aux étudiants.</p><p><a class="btn navy" href="{wa}">Ouvrir WhatsApp</a></p></div>
<div class="card"><h3>Site web</h3><p>{DOMAIN}</p><p>D'autres moyens de contact seront ajoutés ici seulement lorsqu'ils seront confirmés.</p></div></div>'''),
            "faq": ("Questions fréquentes", "De courtes réponses aux questions courantes.", None),
            "privacy": ("Politique de confidentialité", "Comment OBTS utilise les informations que vous envoyez.", None),
            "terms": ("Conditions d'utilisation", "Les conditions d'utilisation de ce site et des documents d'OBTS.", None),
        }
    if page in SERVICES:
        content[page] = service_page(lang, page)
    if page == "syllabus":
        content[page] = (SYLLABUS_TEXT[lang]["title"], SYLLABUS_TEXT[lang]["intro"], None)
    if page == "courses":
        title, intro, html_body = content[page]
        content[page] = (title, intro, html_body + f'<p><a class="btn navy" href="syllabus.html">'
                                                    f'{e(SYLLABUS_TEXT[lang]["see"])}</a></p>')
    item = content[page]
    if page == "index":
        home = item[1]
        cut = home.rindex('<div class="note gold">')
        return item[0], home[:cut] + services_grid(lang) + home[cut:], True
    title, intro, html_body = item
    if html_body is None:
        html_body = {"admissions": admissions, "faq": faq, "privacy": privacy, "terms": terms,
                     "syllabus": syllabus}[page](lang)
    head = f'<section class="page-head"><div class="wrap"><h1>{e(title)}</h1><p>{e(intro)}</p></div></section>'
    return title, head + f'<div class="wrap section">{html_body}</div>', False


FORM = {
    "en": {"steps": ["Fill in the form and press the button: WhatsApp opens with your message.",
                     "Send the message. Admissions replies and confirms the course, the language, the fees and the start date.",
                     "For Pastoral English or English Speaking, you first make a one-minute placement recording.",
                     "You receive your first lesson on WhatsApp."],
           "name": "Full name", "phone": "WhatsApp number", "place": "Town and country", "language": "Preferred language",
           "courses": "Course(s)", "message": "Message (optional)",
           "consent": "I agree that OBTS uses these details to reply to me, as described in the privacy policy.",
           "submit": "Open WhatsApp with my message", "missing": "Please complete:",
           "intro": "Hello OBTS, I would like to register.", "hint": "Nothing is saved on this website: your details go only into the WhatsApp message you choose to send.",
           "continue": "Continue to WhatsApp", "prepared": "Your message is ready. If WhatsApp did not open, use the button below. Review your details and press Send in WhatsApp to complete your enquiry.", "no_js": "To register without this form, contact OBTS on WhatsApp.",
           "privacy": "privacy policy", "phone_hint": "With country code, for example +255 …"},
    "sw": {"steps": ["Jaza fomu na ubonyeze kitufe: WhatsApp inafunguka na ujumbe wako.",
                     "Tuma ujumbe. Ofisi ya usajili inajibu na kuthibitisha kozi, lugha, ada na tarehe ya kuanza.",
                     "Kwa Kiingereza cha Kichungaji au Kuzungumza Kiingereza, kwanza unarekodi sauti ya upimaji ya dakika moja.",
                     "Unapokea somo lako la kwanza kwenye WhatsApp."],
           "name": "Jina kamili", "phone": "Namba ya WhatsApp", "place": "Mji na nchi", "language": "Lugha unayopendelea",
           "courses": "Kozi", "message": "Ujumbe (si lazima)",
           "consent": "Nakubali OBTS itumie taarifa hizi kunijibu, kama ilivyoelezwa kwenye sera ya faragha.",
           "submit": "Fungua WhatsApp na ujumbe wangu", "missing": "Tafadhali jaza:",
           "intro": "Habari OBTS, ningependa kujisajili.", "hint": "Hakuna kinachohifadhiwa kwenye tovuti hii: taarifa zako zinaingia tu kwenye ujumbe wa WhatsApp utakaoamua kuutuma.",
           "continue": "Endelea WhatsApp", "prepared": "Ujumbe wako uko tayari. WhatsApp isipofunguka, tumia kitufe hapa chini. Hakiki taarifa zako na ubonyeze Tuma kwenye WhatsApp ili kukamilisha ombi lako.", "no_js": "Kujisajili bila fomu hii, wasiliana na OBTS kupitia WhatsApp.",
           "privacy": "sera ya faragha", "phone_hint": "Pamoja na msimbo wa nchi, kwa mfano +255 …"},
    "fr": {"steps": ["Remplissez le formulaire et appuyez sur le bouton : WhatsApp s'ouvre avec votre message.",
                     "Envoyez le message. Le service des inscriptions répond et confirme le cours, la langue, les frais et la date de début.",
                     "Pour l'anglais pastoral ou l'anglais oral, vous faites d'abord un enregistrement de placement d'une minute.",
                     "Vous recevez votre première leçon sur WhatsApp."],
           "name": "Nom complet", "phone": "Numéro WhatsApp", "place": "Ville et pays", "language": "Langue préférée",
           "courses": "Cours", "message": "Message (facultatif)",
           "consent": "J'accepte qu'OBTS utilise ces informations pour me répondre, comme décrit dans la politique de confidentialité.",
           "submit": "Ouvrir WhatsApp avec mon message", "missing": "Veuillez compléter :",
           "intro": "Bonjour OBTS, je souhaite m'inscrire.", "hint": "Rien n'est enregistré sur ce site : vos informations vont seulement dans le message WhatsApp que vous choisissez d'envoyer.",
           "continue": "Continuer sur WhatsApp", "prepared": "Votre message est prêt. Si WhatsApp ne s’ouvre pas, utilisez le bouton ci-dessous. Vérifiez vos informations et appuyez sur Envoyer dans WhatsApp pour terminer votre demande.", "no_js": "Pour vous inscrire sans ce formulaire, contactez OBTS sur WhatsApp.",
           "privacy": "politique de confidentialité", "phone_hint": "Avec l'indicatif du pays, par exemple +255 …"},
}


def admissions(lang):
    f, ui = FORM[lang], UI[lang]
    steps = "".join(f"<li>{e(s)}</li>" for s in f["steps"])
    boxes = "".join(
        f'<label><input type="checkbox" name="course" value="{e(c["name"][lang])}"{"" if c["open"] else " disabled"}> '
        f'{e(c["name"][lang])}{"" if c["open"] else " — " + e(ui["soon"])}</label>' for c in COURSES)
    options = "".join(f'<option value="{e(LANG_NAME[code])}"{" selected" if code == lang else ""}>{e(LANG_NAME[code])}</option>'
                      for code in LANGS)
    text = json.dumps({k: f[k] for k in ("name", "phone", "place", "language", "courses", "message", "consent",
                                          "missing", "intro")}, ensure_ascii=False)
    return f'''<div class="grid" style="align-items:start"><div><h2 style="margin-top:0">{e(ui["nav"]["admissions"])}</h2><ol class="steps">{steps}</ol>
<div class="note gold">{e(ui["tba"])}.</div></div>
<form class="reg" id="registration" novalidate data-wa="{WHATSAPP}" data-text="{e(text)}">
<div class="field"><label for="f-name">{e(f["name"])}</label><input type="text" id="f-name" name="name" autocomplete="name" required></div>
<div class="field"><label for="f-phone">{e(f["phone"])}</label><input type="tel" id="f-phone" name="phone" autocomplete="tel" inputmode="tel" required placeholder="+255" aria-describedby="f-phone-hint"><div class="hint" id="f-phone-hint">{e(f["phone_hint"])}</div></div>
<div class="field"><label for="f-place">{e(f["place"])}</label><input type="text" id="f-place" name="place" required></div>
<div class="field"><label for="f-language">{e(f["language"])}</label><select id="f-language" name="language">{options}</select></div>
<fieldset class="field"><legend>{e(f["courses"])}</legend><div class="checks">{boxes}</div></fieldset>
<div class="field"><label for="f-message">{e(f["message"])}</label><textarea id="f-message" name="message"></textarea></div>
<div class="field consent"><input type="checkbox" id="f-consent" name="consent" required><label for="f-consent" style="font-weight:500;color:inherit">{e(f["consent"])} (<a href="privacy.html">{e(f["privacy"])}</a>)</label></div>
<p class="error" role="alert" aria-live="polite"></p>
<button class="btn" type="submit">{e(f["submit"])}</button>
<div class="note registration-prepared" id="registration-prepared" role="status" hidden><p>{e(f["prepared"])}</p><a class="btn navy" id="registration-continue" target="_blank" rel="noopener noreferrer">{e(f["continue"])}</a></div>
<noscript><p class="note"><a href="{wa_link()}">{e(f["no_js"])}</a></p></noscript>
<p class="hint" style="margin-top:12px">{e(f["hint"])}</p></form></div>'''


FAQ = {
    "en": [("Who can study at OBTS?", "Anyone who wants to learn and can follow lessons on a phone. Pastoral English starts from a basic level of English (A2); English Speaking starts with a placement recording."),
           ("Do I need a computer?", "No. A phone with WhatsApp and a PDF reader is enough."),
           ("How much are the fees, and when do courses start?", "Fees and start dates have not yet been announced. Ask on WhatsApp and admissions will tell you when they are confirmed."),
           ("Can I take more than one course?", "Admissions will confirm how many courses you can take at the same time."),
           ("In which language are the lessons?", "General Bible Studies & Theology: the first 25 lessons have been written in English, Kiswahili and French and are being reviewed by lecturers; once approved, you receive them in the language you choose when you register. The other courses are written first in English, and the AI course in Kiswahili; their Kiswahili and French versions are being prepared and reviewed, and admissions will tell you what is available."),
           ("Will I receive a certificate?", "Information about certificates will be given only when it has been approved. Please do not rely on any promise that is not on this website or from OBTS admissions."),
           ("How are my details used?", "See the privacy policy. The registration form on this website stores nothing; it only prepares a WhatsApp message.")],
    "sw": [("Nani anaweza kusoma OBTS?", "Yeyote anayetaka kujifunza na anayeweza kufuata masomo kwa simu. Kiingereza cha Kichungaji kinaanza kiwango cha msingi cha Kiingereza (A2); Kuzungumza Kiingereza kinaanza kwa kurekodi sauti ya upimaji."),
           ("Je, ninahitaji kompyuta?", "Hapana. Simu yenye WhatsApp na programu ya kusoma PDF inatosha."),
           ("Ada ni kiasi gani, na kozi zinaanza lini?", "Ada na tarehe za kuanza bado hazijatangazwa. Uliza kwa WhatsApp na ofisi ya usajili itakueleza zikithibitishwa."),
           ("Je, ninaweza kusoma zaidi ya kozi moja?", "Ofisi ya usajili itathibitisha idadi ya kozi unazoweza kusoma kwa wakati mmoja."),
           ("Masomo yako kwa lugha gani?", "Mafunzo ya Jumla ya Biblia na Theolojia: masomo 25 ya kwanza yameandikwa kwa Kiingereza, Kiswahili na Kifaransa na yanakaguliwa na wahadhiri; yakishaidhinishwa, unayapokea kwa lugha utakayochagua wakati wa kujisajili. Kozi nyingine zinaandikwa kwanza kwa Kiingereza, na kozi ya AI kwa Kiswahili; matoleo yake ya Kiswahili na Kifaransa yanaandaliwa na kukaguliwa, na ofisi ya usajili itakueleza kinachopatikana."),
           ("Je, nitapata cheti?", "Taarifa kuhusu vyeti zitatolewa tu zitakapoidhinishwa. Tafadhali usitegemee ahadi yoyote isiyo kwenye tovuti hii au kutoka ofisi ya usajili ya OBTS."),
           ("Taarifa zangu zinatumikaje?", "Tazama sera ya faragha. Fomu ya usajili kwenye tovuti hii haihifadhi chochote; inaandaa ujumbe wa WhatsApp tu.")],
    "fr": [("Qui peut étudier à OBTS ?", "Toute personne qui veut apprendre et peut suivre des leçons sur un téléphone. L'anglais pastoral commence à un niveau d'anglais de base (A2) ; l'anglais oral commence par un enregistrement de placement."),
           ("Ai-je besoin d'un ordinateur ?", "Non. Un téléphone avec WhatsApp et un lecteur de PDF suffit."),
           ("Quels sont les frais, et quand les cours commencent-ils ?", "Les frais et les dates de début n'ont pas encore été annoncés. Demandez sur WhatsApp : le service des inscriptions vous informera dès qu'ils seront confirmés."),
           ("Puis-je suivre plus d'un cours ?", "Le service des inscriptions confirmera combien de cours vous pouvez suivre en même temps."),
           ("Dans quelle langue sont les leçons ?", "Études bibliques générales et théologie : les 25 premières leçons ont été rédigées en anglais, en kiswahili et en français et sont en cours de vérification par des enseignants ; une fois approuvées, vous les recevez dans la langue choisie lors de votre inscription. Les autres cours sont d'abord écrits en anglais, et le cours d'IA en kiswahili ; leurs versions en kiswahili et en français sont en préparation et en révision, et le service des inscriptions vous dira ce qui est disponible."),
           ("Recevrai-je un certificat ?", "Les informations sur les certificats seront données seulement lorsqu'elles auront été approuvées. Ne vous fiez à aucune promesse qui ne figure pas sur ce site ou ne vient pas du service des inscriptions d'OBTS."),
           ("Comment mes informations sont-elles utilisées ?", "Voir la politique de confidentialité. Le formulaire d'inscription de ce site n'enregistre rien ; il prépare seulement un message WhatsApp.")],
}


def faq(lang):
    return "".join(f"<details><summary>{e(q)}</summary><div><p>{e(a)}</p></div></details>" for q, a in FAQ[lang])


# The first four paragraphs are the policy already served by the OBTS system (app.py, /privacy).
PRIVACY = {
    "en": (["Information received through WhatsApp may be used for registration, learning support, student progress, Online Campus access management, pastoral assistance and automated responses.",
            "We do not sell users' personal information to third parties.",
            "Users may request deletion of their information by contacting OBTS & ODM administration.",
            "This service may use Meta WhatsApp Business Platform, cloud hosting, database services and artificial intelligence services to process and respond to messages."],
           "This website", ["The registration form on this website does not store or send your details anywhere. It only prepares a WhatsApp message, which you can read, change or decide not to send.",
                            "This website remembers your language choice in your own browser. It uses no advertising or tracking cookies."],
           "Last updated: October 2026."),
    "sw": (["Taarifa zinazopokelewa kupitia WhatsApp zinaweza kutumika kwa ajili ya usajili, msaada wa kimasomo, maendeleo ya mwanafunzi, usimamizi wa ufikiaji wa Online Campus, msaada wa kichungaji na majibu ya kiotomatiki.",
            "Hatuuzi taarifa binafsi za watumiaji kwa wahusika wengine.",
            "Watumiaji wanaweza kuomba kufutwa kwa taarifa zao kwa kuwasiliana na uongozi wa OBTS na ODM.",
            "Huduma hii inaweza kutumia Meta WhatsApp Business Platform, huduma za hifadhi ya wingu (cloud), huduma za database, na huduma za akili bandia (AI) kuchakata na kujibu ujumbe."],
           "Tovuti hii", ["Fomu ya usajili kwenye tovuti hii haihifadhi wala haitumi taarifa zako popote. Inaandaa ujumbe wa WhatsApp tu, ambao unaweza kuusoma, kuubadilisha au kuamua kutoutuma.",
                          "Tovuti hii inakumbuka lugha uliyochagua ndani ya kivinjari chako tu. Haitumii vidakuzi (cookies) vya matangazo wala vya kufuatilia."],
           "Ilisasishwa mara ya mwisho: Oktoba 2026."),
    "fr": (["Les informations reçues via WhatsApp peuvent être utilisées pour l'inscription, le soutien pédagogique, le suivi de la progression de l'étudiant, la gestion de l'accès au Campus en ligne, l'assistance pastorale et les réponses automatisées.",
            "Nous ne vendons pas les informations personnelles des utilisateurs à des tiers.",
            "Les utilisateurs peuvent demander la suppression de leurs informations en contactant l'administration d'OBTS et d'ODM.",
            "Ce service peut utiliser la plateforme Meta WhatsApp Business, l'hébergement cloud, des services de base de données et des services d'intelligence artificielle pour traiter et répondre aux messages."],
           "Ce site web", ["Le formulaire d'inscription de ce site n'enregistre ni n'envoie vos informations nulle part. Il prépare seulement un message WhatsApp, que vous pouvez lire, modifier ou décider de ne pas envoyer.",
                           "Ce site retient votre choix de langue dans votre propre navigateur. Il n'utilise aucun cookie publicitaire ni de suivi."],
           "Dernière mise à jour : octobre 2026."),
}


def privacy(lang):
    system, heading, site, updated = PRIVACY[lang]
    who = {"en": "Online Bible & Theology School (OBTS) and Online Deliverance Ministry (ODM)",
           "sw": "Online Bible & Theology School (OBTS) na Online Deliverance Ministry (ODM)",
           "fr": "Online Bible & Theology School (OBTS) et Online Deliverance Ministry (ODM)"}[lang]
    return (f"<h2 style='margin-top:0'>{e(who)}</h2>" + "".join(f"<p>{e(p)}</p>" for p in system)
            + f"<h2>{e(heading)}</h2>" + "".join(f"<p>{e(p)}</p>" for p in site)
            + f'<p>WhatsApp: <a href="{wa_link()}">{WHATSAPP_DISPLAY}</a></p><p class="hint">{e(updated)}</p>')


TERMS = {
    "en": [("Purpose", "This website gives information about the Online Bible & Theology School (OBTS) and lets you contact admissions."),
           ("Course materials", "Lessons and other materials sent to students are for the student's personal study. Please do not publish or sell them without written permission from OBTS."),
           ("Information on this website", "OBTS works to keep this information correct. Fees, dates, certificates and other details are valid only when OBTS announces them; anything not yet announced is shown as \"to be announced\"."),
           ("Draft materials", "Draft lessons, answer keys and lecturer guides are not published on this website and are not sent to students before they are approved."),
           ("Respect in learning groups", "Students are asked to communicate respectfully with tutors and other students, and to protect other people's personal information."),
           ("Changes", "These terms may be updated. The date below shows the latest version.")],
    "sw": [("Lengo", "Tovuti hii inatoa taarifa kuhusu Online Bible & Theology School (OBTS) na inakuwezesha kuwasiliana na ofisi ya usajili."),
           ("Vifaa vya kozi", "Masomo na vifaa vingine vinavyotumwa kwa wanafunzi ni kwa ajili ya kujifunza binafsi kwa mwanafunzi. Tafadhali usivichapishe wala kuviuza bila ruhusa ya maandishi kutoka OBTS."),
           ("Taarifa kwenye tovuti hii", "OBTS inajitahidi kuweka taarifa hizi sahihi. Ada, tarehe, vyeti na mambo mengine ni halali tu OBTS inapoyatangaza; chochote kisichotangazwa bado kinaonyeshwa kama \"kitatangazwa\"."),
           ("Rasimu", "Rasimu za masomo, majibu na miongozo ya wahadhiri hazichapishwi kwenye tovuti hii na hazitumwi kwa wanafunzi kabla ya kuidhinishwa."),
           ("Heshima katika vikundi vya kujifunza", "Wanafunzi wanaombwa kuwasiliana kwa heshima na wakufunzi na wanafunzi wengine, na kulinda taarifa binafsi za watu wengine."),
           ("Mabadiliko", "Masharti haya yanaweza kusasishwa. Tarehe iliyo hapa chini inaonyesha toleo la karibuni.")],
    "fr": [("Objet", "Ce site donne des informations sur l'Online Bible & Theology School (OBTS) et vous permet de contacter le service des inscriptions."),
           ("Documents de cours", "Les leçons et autres documents envoyés aux étudiants sont destinés à l'étude personnelle de l'étudiant. Merci de ne pas les publier ni les vendre sans l'autorisation écrite d'OBTS."),
           ("Informations de ce site", "OBTS s'efforce de garder ces informations exactes. Les frais, dates, certificats et autres détails ne sont valables que lorsqu'OBTS les annonce ; ce qui n'est pas encore annoncé est indiqué « à annoncer »."),
           ("Brouillons", "Les brouillons de leçons, les corrigés et les guides de l'enseignant ne sont pas publiés sur ce site et ne sont pas envoyés aux étudiants avant leur approbation."),
           ("Respect dans les groupes d'apprentissage", "Les étudiants sont priés de communiquer avec respect avec les tuteurs et les autres étudiants, et de protéger les informations personnelles d'autrui."),
           ("Modifications", "Ces conditions peuvent être mises à jour. La date ci-dessous indique la dernière version.")],
}


def terms(lang):
    updated = {"en": "Last updated: October 2026.", "sw": "Ilisasishwa mara ya mwisho: Oktoba 2026.",
               "fr": "Dernière mise à jour : octobre 2026."}[lang]
    return "".join(f"<h2>{e(h)}</h2><p>{e(p)}</p>" for h, p in TERMS[lang]) + f'<p class="hint">{e(updated)}</p>'


# ------------------------------------------------------------
# Layout
# ------------------------------------------------------------

CURRENT_PAGE = ' aria-current="page"'
CURRENT_LANG = ' aria-current="true"'


# ------------------------------------------------------------
# Syllabus: the modules of every course, from the school system's
# curriculum (tools/syllabus.json, exported from odm-ai-asistant).
# Module titles are shown in the language the course is written in; the
# AI course structure is a proposal until the school approves it.
# ------------------------------------------------------------

SYLLABUS_TEXT = {
    "en": {"title": "Syllabus", "intro": "The modules of each course, in order.",
           "see": "See the syllabus (modules of every course)",
           "lang_note": "Module titles are shown in English, the language of the curriculum; Kiswahili and French titles will be added when they are approved. The first 25 GB lessons (modules 1–3) have been written in English, Kiswahili and French and are being reviewed; each is sent in the student's language only after a lecturer approves it. The AI course titles are given in all three languages.",
           "code": "Code", "module": "Module", "details": "Grade · track · lessons · days", "lessons": "Lessons", "days": "Days", "grade": "Grade", "track": "Track",
           "modules": "modules", "proposed": "Proposed structure — awaiting the school's approval. It has 16 modules and 56 lessons; each student takes 13 modules (47 lessons, 120 days), choosing the video or the audio track in Grade III. Fees and start dates are not yet announced.",
           "no_promise": "The course does not promise employment or income.",
           "tracks": {"maandishi": "writing", "video": "video", "audio": "audio", "tovuti": "website", "mradi": "final project"}},
    "sw": {"title": "Mtaala", "intro": "Moduli za kila kozi, kwa mpangilio.",
           "see": "Tazama mtaala (moduli za kila kozi)",
           "lang_note": "Majina ya moduli yanaonyeshwa kwa Kiingereza, lugha ya mtaala; majina ya Kiswahili na Kifaransa yataongezwa yatakapoidhinishwa. Masomo 25 ya kwanza ya GB (moduli 1–3) yameandikwa kwa Kiingereza, Kiswahili na Kifaransa na yanakaguliwa; kila somo linatumwa kwa lugha ya mwanafunzi tu baada ya mhadhiri kuliidhinisha. Majina ya kozi ya AI yapo kwa lugha zote tatu.",
           "code": "Namba", "module": "Moduli", "details": "Daraja · njia · masomo · siku", "lessons": "Masomo", "days": "Siku", "grade": "Daraja", "track": "Njia",
           "modules": "moduli", "proposed": "Muundo unaopendekezwa — unasubiri idhini ya shule. Una moduli 16 na masomo 56; kila mwanafunzi anachukua moduli 13 (masomo 47, siku 120), akichagua njia ya video au ya audio katika Daraja III. Ada na tarehe za kuanza bado hazijatangazwa.",
           "no_promise": "Kozi haiahidi ajira wala mapato.",
           "tracks": {"maandishi": "maandishi", "video": "video", "audio": "audio", "tovuti": "tovuti", "mradi": "mradi wa mwisho"}},
    "fr": {"title": "Programme", "intro": "Les modules de chaque cours, dans l'ordre.",
           "see": "Voir le programme (modules de chaque cours)",
           "lang_note": "Les titres des modules sont donnés en anglais, la langue du programme ; les titres en kiswahili et en français seront ajoutés lorsqu'ils seront approuvés. Les 25 premières leçons de GB (modules 1 à 3) ont été rédigées en anglais, en kiswahili et en français et sont en cours de vérification ; chacune n'est envoyée dans la langue de l'étudiant qu'après son approbation par un enseignant. Les titres du cours d'IA sont donnés dans les trois langues.",
           "code": "Code", "module": "Module", "details": "Niveau · parcours · leçons · jours", "lessons": "Leçons", "days": "Jours", "grade": "Niveau", "track": "Parcours",
           "modules": "modules", "proposed": "Structure proposée — en attente de l'approbation de l'école. Elle compte 16 modules et 56 leçons ; chaque étudiant suit 13 modules (47 leçons, 120 jours), en choisissant le parcours vidéo ou audio au niveau III. Les frais et les dates de début ne sont pas encore annoncés.",
           "no_promise": "Le cours ne promet ni emploi ni revenu.",
           "tracks": {"maandishi": "écrit", "video": "vidéo", "audio": "audio", "tovuti": "site web", "mradi": "projet final"}},
}


def syllabus_data():
    with open(os.path.join(ROOT, "tools", "syllabus.json"), encoding="utf-8") as source:
        return json.load(source)["courses"]


def syllabus(lang):
    text, data = SYLLABUS_TEXT[lang], syllabus_data()
    parts = [f'<div class="note">{e(text["lang_note"])}</div>',
             '<p>' + " ".join(f'<a class="tag" href="#syl-{c["code"].lower()}">{e(c["name"][lang])}</a>'
                              for c in COURSES) + '</p>']
    for course in COURSES:
        info = data[course["code"]]
        modules = info["modules"]
        is_ai = course["code"] == "AI"
        head = [text["code"], text["module"]] + ([text["details"]] if is_ai
                                                 else [text["lessons"]] if any(m.get("lessons") for m in modules) else [])
        rows = []
        for m in modules:
            title = m["title"].get(lang) or m["title"].get(info["master"])
            cells = [m["code"], title]
            if is_ai:
                cells.append(f'{text["grade"]} {m["grade"]} · {text["tracks"].get(m["track"], m["track"])} · '
                             f'{text["lessons"].lower()} {m["lessons"]} · {text["days"].lower()} {m["days"]}')
            elif len(head) == 3:
                cells.append(m.get("lessons") or "")
            rows.append("<tr>" + "".join(('<td class="nowrap">' if i == 0 else "<td>") + e(str(c)) + "</td>"
                                         for i, c in enumerate(cells)) + "</tr>")
        note = (f'<div class="note gold">{e(text["proposed"])} {e(text["no_promise"])}</div>' if is_ai else "")
        parts.append(f'<section class="section" id="syl-{course["code"].lower()}"><h2>{e(course["name"][lang])}</h2>'
                     f'<p><span class="tag">{len(modules)} {e(text["modules"])}</span></p>{note}'
                     f'<div class="table-scroll"><table class="simple"><thead><tr>'
                     + "".join(f"<th>{e(h)}</th>" for h in head) + "</tr></thead><tbody>" + "".join(rows)
                     + "</tbody></table></div></section>")
    return "".join(parts)


def page_html(lang, page):
    ui = UI[lang]
    title, main, is_home = body(lang, page)
    prefix = "../" if LANGS[lang] else ""
    assets = prefix + "assets/"
    nav = "".join(f'<a href="{p}.html"{CURRENT_PAGE if p == page else ""}>{e(ui["nav"][p])}</a>' for p in NAV)
    switch = "".join(
        f'<a href="{prefix}{LANGS[code]}{page}.html" hreflang="{code}" lang="{code}" title="{LANG_NAME[code]}"'
        f'{CURRENT_LANG if code == lang else ""}>{LANG_LABEL[code]}</a>' for code in LANGS)
    alternates = "".join(f'<link rel="alternate" hreflang="{code}" href="https://{DOMAIN}/{LANGS[code]}{"" if page == "index" else page + ".html"}">'
                         for code in LANGS)
    footer_links = "".join(f'<li><a href="{p}.html">{e(ui["nav"][p])}</a></li>' for p in ("courses", "syllabus", "how-to-learn",
                                                                                            "admissions", "library",
                                                                                            "bookstore", "portal",
                                                                                            "assistant", "faq",
                                                                                            "privacy", "terms"))
    full_title = title if is_home else f"{title} | OBTS"
    preview = f'<div class="preview">{e(ui["preview"])}</div>' if PREVIEW else ""
    # the page's own lead sentence describes it in search results and link previews; the home page uses the school's
    lead = re.search(r'<section class="page-head">.*?<p>(.*?)</p>', main, re.S)
    description = html.unescape(lead.group(1)) if lead and not is_home else ui["foot_about"]
    url = f"https://{DOMAIN}/{LANGS[lang]}{'' if page == 'index' else page + '.html'}"
    share = (f'<link rel="canonical" href="{url}">\n'
             f'<meta property="og:site_name" content="OBTS — Online Bible &amp; Theology School">\n'
             f'<meta property="og:type" content="website">\n'
             f'<meta property="og:title" content="{e(full_title)}">\n'
             f'<meta property="og:description" content="{e(description)}">\n'
             f'<meta property="og:url" content="{url}">\n'
             f'<meta property="og:locale" content="{OG_LOCALE[lang]}">\n'
             + "".join(f'<meta property="og:locale:alternate" content="{OG_LOCALE[code]}">\n' for code in LANGS if code != lang)
             + f'<meta property="og:image" content="https://{DOMAIN}/assets/img/obts-logo-600.png">\n'
             f'<meta property="og:image:width" content="600"><meta property="og:image:height" content="400">\n'
             f'<meta property="og:image:alt" content="OBTS — Online Bible &amp; Theology School">\n'
             f'<meta name="twitter:card" content="summary">')
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="no-referrer">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
{share}
{'<meta name="robots" content="noindex">' if PREVIEW else ''}
{alternates}
<link rel="icon" type="image/png" href="{assets}img/favicon-64.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Libre+Baskerville:wght@400;700&display=swap">
<link rel="stylesheet" href="{assets}css/site.css">
</head>
<body>
<a class="skip" href="#main">{e(ui["skip"])}</a>
{preview}
<header class="site-header"><div class="wrap bar">
<a class="brand" href="index.html"><img src="{assets}img/obts-logo-600.png" width="600" height="400" alt="OBTS — Online Bible &amp; Theology School"><span>Online Bible &amp; Theology School</span></a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">{e(ui["menu"])}</button>
<nav class="nav" id="site-nav" aria-label="{e(ui["menu"])}">{nav}<div class="lang" role="group" aria-label="{e(ui["lang_label"])}">{switch}</div></nav>
</div></header>
<main id="main">{main.replace("{assets}", assets)}</main>
<footer class="site-footer"><div class="wrap"><div class="foot">
<div><img src="{assets}img/obts-seal-192.png" width="72" height="72" alt=""><p>{e(ui["foot_about"])}</p><p>{e(ui["tagline"])}</p></div>
<div><h3>{e(ui["foot_links"])}</h3><ul>{footer_links}</ul></div>
<div><h3>{e(ui["foot_contact"])}</h3><ul><li>{e(ui["wa"])}: <a href="{wa_link()}">{WHATSAPP_DISPLAY}</a></li><li>{DOMAIN}</li></ul></div>
</div><div class="copy">© 2026 {e(ui["copy"])}</div></div></footer>
<a class="wa-float" href="{wa_link()}" aria-label="WhatsApp {WHATSAPP_DISPLAY}">WhatsApp</a>
<script src="{assets}js/campus-link.js"></script>
<script src="{assets}js/site.js"></script>
</body>
</html>
'''


# Pages of the earlier IIBTS site: each now points to the OBTS page that replaces it.
REDIRECTS = {"programs": "courses", "policies": "privacy", "campus": "how-to-learn",
             "news": "index", "scholarships": "admissions", "standards": "about", "support": "contact"}


def redirect_html(target):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex">'
            f'<meta http-equiv="refresh" content="0; url={target}.html"><link rel="canonical" href="{target}.html">'
            f'<title>OBTS</title></head><body><p><a href="{target}.html">Online Bible &amp; Theology School</a></p>'
            f'</body></html>\n')


def outputs():
    files = {}
    for lang, folder in LANGS.items():
        for page in PAGES:
            files[os.path.join(ROOT, folder, f"{page}.html")] = page_html(lang, page)
    for old, new in REDIRECTS.items():
        files[os.path.join(ROOT, f"{old}.html")] = redirect_html(new)
    files[os.path.join(ROOT, "robots.txt")] = "User-agent: *\nDisallow: /\n" if PREVIEW else "User-agent: *\nAllow: /\n"
    return files


def main():
    check = "--check" in sys.argv
    stale = []
    for path, text in outputs().items():
        current = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if current != text:
            stale.append(os.path.relpath(path, ROOT))
            if not check:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as out:
                    out.write(text)
    print(("out of date: " if check else "written: ") + (", ".join(stale) or "none"))
    return 1 if check and stale else 0


if __name__ == "__main__":
    sys.exit(main())
