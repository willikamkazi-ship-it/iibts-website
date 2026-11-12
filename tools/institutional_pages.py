"""Public OBTS content for the restored IIBTS site sections."""

# Each page contains a title, introduction, and cards with internal destinations.
PAGES = {
    "en": {
        "research": ("Research", "Find study guides and learn how to investigate a biblical or theological question.", [
            ("Define your question", "Turn a broad topic into one question. Identify the biblical passages, people, place or period you want to examine.", "learn"),
            ("Find and assess sources", "Read the passage in context. Compare the biblical text with dictionaries, commentaries or other sources you can identify and verify.", "library"),
            ("Write and cite your work", "Explain how your sources support your conclusion. Give the author, title and page number or link where available. Identify direct quotations and credit borrowed ideas.", "standards"),
        ]),
        "campus": ("Online Campus", "Follow the steps from enrollment to studying and tracking your progress.", [
            ("Register and choose a language", "Start on WhatsApp and choose English, Kiswahili or French when prompted.", "join-obts"),
            ("Receive and study lessons", "Work through the reading, study guide and exercises. Where published, use visual or audio resources for review.", "how-to-learn"),
            ("Complete work and track progress", "Complete the assessments for your course and use your personal classroom link to see your next lesson and progress.", "portal"),
        ]),
        "news": ("News and events", "Find academic updates, new resources and announcements about training at OBTS.", [
            ("Sample lessons published", "Explore 35 sample lessons, five per course, in English, Kiswahili and French.", "learn"),
            ("Library catalogue", "Browse the catalogue for materials available in your chosen language.", "library"),
            ("Seminars and events", "Ask OBTS about upcoming seminars, training sessions and class schedules.", "contact"),
        ]),
        "scholarships": ("Scholarships and student assistance", "Find out how to ask about assistance with learning resources or access to study.", [
            ("Student assistance", "If you need help accessing course materials, tell the school what you need. The school can confirm which options, if any, are open.", "contact"),
            ("Sponsored access", "Ask the school about supporting access to learning materials or the Online Campus.", "support"),
        ]),
        "standards": ("Academic standards", "Study Scripture carefully, explain your reasoning and apply what you learn responsibly.", [
            ("Interpret in context", "Read the surrounding passage, identify its genre and explain how you reached your interpretation.", "research"),
            ("Submit honest work", "Write your own answers, mark quotations and cite borrowed ideas. Ask your lecturer when the assignment instructions are unclear.", "policies"),
            ("Put learning into practice", "Complete the exercises and use your lecturer’s feedback to improve your next assignment.", "how-to-learn"),
        ]),
        "support": ("Support and sponsorship", "Contact OBTS about helping learners or developing study resources.", [
            ("Support a learner", "Ask the school how to assist someone who needs study materials or access to online learning.", "scholarships"),
            ("Support the library", "Discuss contributing original or licensed books, study guides, audio or teaching visuals.", "library"),
            ("Contact the school", "Share what you would like to contribute, including translation, learning resources or technical support.", "contact"),
        ]),
        "policies": ("School policies", "Find guidance on student information, academic work, learning materials and help.", [
            ("Student and website information", "See how OBTS handles information you provide through its website and learning services.", "privacy"),
            ("Academic integrity", "Submit your own work and cite sources you quote or use.", "standards"),
            ("Copyright and access", "Use original, licensed, public-domain or otherwise authorized materials. Read the terms for the website and learning materials.", "terms"),
            ("Purchases and student support", "See how book orders and delivery work, or contact the school for academic or technical help.", "bookstore", "contact"),
        ]),
    },
    "sw": {
        "research": ("Utafiti", "Pata miongozo ya kusoma na ujifunze kuchunguza swali la Biblia au teolojia.", [
            ("Fafanua swali lako", "Chagua swali moja unalotaka kulijibu. Tambua vifungu vya Biblia, watu, mahali au kipindi unachotaka kuchunguza.", "learn"),
            ("Tafuta na pima vyanzo", "Soma kifungu katika muktadha wake. Linganisha maandishi ya Biblia na kamusi, vitabu vya ufafanuzi au vyanzo vingine unavyoweza kuvitambua na kuvihakiki.", "library"),
            ("Andika na taja vyanzo", "Eleza jinsi vyanzo vinavyounga mkono hitimisho lako. Taja mwandishi, kichwa na ukurasa au kiungo inapowezekana. Bainisha nukuu na taja chanzo cha mawazo uliyotumia.", "standards"),
        ]),
        "campus": ("Kampasi ya Mtandaoni", "Fuata hatua za kujiunga, kujifunza na kufuatilia maendeleo yako.", [
            ("Jisajili na uchague lugha", "Anza kwenye WhatsApp na uchague Kiswahili, Kiingereza au Kifaransa utakapoombwa.", "join-obts"),
            ("Pokea na usome masomo", "Fuata ratiba ya kusoma, pitia mwongozo na fanya mazoezi. Tumia nyenzo za picha au sauti pale zinapopatikana.", "how-to-learn"),
            ("Fanya kazi na fuatilia maendeleo", "Kamilisha tathmini za kozi yako. Tumia kiungo chako binafsi cha darasa kuona somo linalofuata na maendeleo yako.", "portal"),
        ]),
        "news": ("Habari na Matukio", "Pata taarifa za masomo, nyenzo mpya na matangazo ya mafunzo ya OBTS.", [
            ("Masomo ya mfano yamechapishwa", "Soma masomo 35 ya mfano, matano kwa kila kozi, kwa Kiswahili, Kiingereza na Kifaransa.", "learn"),
            ("Katalogi ya maktaba", "Vinjari katalogi kuona nyenzo zinazopatikana kwa lugha uliyochagua.", "library"),
            ("Semina na matukio", "Uliza OBTS kuhusu semina, vipindi vya mafunzo na ratiba za madarasa.", "contact"),
        ]),
        "scholarships": ("Ufadhili na Msaada kwa Wanafunzi", "Uliza kuhusu msaada wa kupata nyenzo au kushiriki katika masomo.", [
            ("Msaada kwa mwanafunzi", "Ukihitaji msaada wa kupata nyenzo za kozi, ieleze shule unachohitaji. Shule itakujulisha fursa yoyote iliyo wazi.", "contact"),
            ("Kusaidia mwanafunzi", "Uliza shule jinsi ya kusaidia upatikanaji wa nyenzo au ufikiaji wa Kampasi ya Mtandaoni.", "support"),
        ]),
        "standards": ("Viwango vya Masomo", "Soma Maandiko kwa makini, eleza hoja zako na tumia ulichojifunza kwa uwajibikaji.", [
            ("Fasiri kwa kuzingatia muktadha", "Soma vifungu vinavyozunguka andiko lako, tambua aina ya maandishi na eleza jinsi ulivyofikia tafsiri yako.", "research"),
            ("Wasilisha kazi kwa uaminifu", "Andika majibu yako mwenyewe. Bainisha nukuu na taja vyanzo vya mawazo uliyotumia. Uliza mhadhiri maelekezo ya kazi yasipoeleweka.", "policies"),
            ("Tumia ulichojifunza", "Fanya mazoezi na tumia mrejesho wa mhadhiri kuboresha kazi yako inayofuata.", "how-to-learn"),
        ]),
        "support": ("Usaidizi na Ufadhili", "Wasiliana na OBTS kuhusu kusaidia wanafunzi au kuandaa nyenzo za kujifunza.", [
            ("Msaidie mwanafunzi", "Uliza shule jinsi ya kumsaidia mwanafunzi anayehitaji nyenzo au ufikiaji wa masomo ya mtandaoni.", "scholarships"),
            ("Saidia maktaba", "Zungumza na shule kuhusu kuchangia vitabu vyenye ruhusa, miongozo asilia, sauti au vielelezo vya kufundishia.", "library"),
            ("Wasiliana na shule", "Eleza mchango unaotaka kutoa, kama tafsiri, nyenzo za masomo au msaada wa kiufundi.", "contact"),
        ]),
        "policies": ("Sera za Shule", "Pata maelekezo kuhusu taarifa za wanafunzi, kazi za masomo, matumizi ya nyenzo na msaada.", [
            ("Taarifa za mwanafunzi na tovuti", "Angalia jinsi OBTS inavyoshughulikia taarifa unazotoa kupitia tovuti na huduma zake za masomo.", "privacy"),
            ("Uaminifu wa kitaaluma", "Wasilisha kazi yako mwenyewe na taja vyanzo unavyonukuu au kutumia.", "standards"),
            ("Hakimiliki na ufikiaji", "Tumia nyenzo asilia, zilizoidhinishwa au zilizo katika milki ya umma. Soma masharti ya matumizi ya tovuti na nyenzo.", "terms"),
            ("Ununuzi na msaada", "Soma jinsi ya kuagiza na kupokea vitabu, au wasiliana na shule kwa msaada wa masomo na wa kiufundi.", "bookstore", "contact"),
        ]),
    },
    "fr": {
        "research": ("Recherche", "Trouvez des guides d’étude et apprenez à explorer une question biblique ou théologique.", [
            ("Préciser votre question", "Choisissez une question à laquelle vous souhaitez répondre. Repérez les passages bibliques, les personnes, les lieux ou la période à étudier.", "learn"),
            ("Trouver et évaluer vos sources", "Lisez le passage dans son contexte. Comparez le texte biblique avec des dictionnaires, des commentaires ou d’autres sources que vous pouvez identifier et vérifier.", "library"),
            ("Rédiger et citer", "Expliquez comment vos sources appuient votre conclusion. Indiquez l’auteur, le titre et, si possible, la page ou le lien. Signalez les citations et les idées empruntées.", "standards"),
        ]),
        "campus": ("Campus en ligne", "Suivez les étapes de l’inscription au suivi de vos progrès.", [
            ("S’inscrire et choisir une langue", "Commencez sur WhatsApp et choisissez le français, le kiswahili ou l’anglais lorsque le choix vous est proposé.", "join-obts"),
            ("Recevoir et étudier les leçons", "Suivez la lecture, le guide d’étude et les exercices. Utilisez les supports visuels ou audio lorsqu’ils sont disponibles.", "how-to-learn"),
            ("Faire les devoirs et suivre vos progrès", "Terminez les évaluations du cours et ouvrez votre lien personnel pour voir la prochaine leçon et vos progrès.", "portal"),
        ]),
        "news": ("Actualités et événements", "Retrouvez les nouvelles des cours, les ressources récentes et les annonces de formation d’OBTS.", [
            ("Leçons d’exemple publiées", "Découvrez 35 leçons d’exemple, cinq par cours, en français, en kiswahili et en anglais.", "learn"),
            ("Catalogue de la bibliothèque", "Parcourez le catalogue pour voir les ressources disponibles dans votre langue.", "library"),
            ("Séminaires et événements", "Renseignez-vous auprès d’OBTS sur les séminaires, les formations et les horaires des cours.", "contact"),
        ]),
        "scholarships": ("Bourses et aide aux étudiants", "Renseignez-vous sur l’aide à l’accès aux ressources et aux études.", [
            ("Aide aux étudiants", "Si vous avez besoin d’aide pour accéder aux documents d’un cours, expliquez vos besoins à l’école. Elle vous indiquera les possibilités ouvertes.", "contact"),
            ("Accès financé", "Demandez à l’école comment soutenir l’accès aux ressources d’étude ou au Campus en ligne.", "support"),
        ]),
        "standards": ("Normes académiques", "Étudiez les Écritures avec soin, expliquez votre raisonnement et appliquez vos apprentissages avec responsabilité.", [
            ("Interpréter en contexte", "Lisez les passages qui entourent le texte, identifiez son genre et expliquez comment vous êtes arrivé à votre interprétation.", "research"),
            ("Rendre un travail honnête", "Rédigez vos propres réponses, signalez les citations et indiquez les sources des idées empruntées. Demandez des précisions à votre enseignant si nécessaire.", "policies"),
            ("Mettre en pratique", "Faites les exercices et utilisez les retours de votre enseignant pour améliorer votre prochain travail.", "how-to-learn"),
        ]),
        "support": ("Soutien et parrainage", "Contactez OBTS pour aider des étudiants ou contribuer aux ressources d’étude.", [
            ("Soutenir un étudiant", "Demandez à l’école comment aider un étudiant qui a besoin de ressources ou d’un accès aux études en ligne.", "scholarships"),
            ("Soutenir la bibliothèque", "Proposez des livres autorisés, des guides originaux, des ressources audio ou des supports visuels.", "library"),
            ("Contacter l’école", "Décrivez votre contribution, par exemple une traduction, des ressources d’étude ou une aide technique.", "contact"),
        ]),
        "policies": ("Politiques de l’école", "Retrouvez les règles sur les données, les travaux, les ressources d’étude et l’assistance.", [
            ("Données des étudiants et du site", "Consultez les règles de traitement des informations que vous transmettez sur le site ou dans les services d’étude.", "privacy"),
            ("Intégrité académique", "Rendez votre propre travail et citez les sources que vous utilisez.", "standards"),
            ("Droit d’auteur et accès", "Utilisez des ressources originales, autorisées ou dans le domaine public. Lisez les conditions d’utilisation du site et des ressources.", "terms"),
            ("Achats et assistance", "Consultez les modalités de commande et de livraison des livres ou contactez l’école pour une aide pédagogique ou technique.", "bookstore", "contact"),
        ]),
    },
}

LIBRARY_LINKS = {
    "en": ("Choose a language", "Browse by resource type", ("Books and e-books", "Course notes and materials", "Articles and study guides", "Audio lessons", "Video and infographics", "Bookstore"), "The catalogue shows resources as they are published."),
    "sw": ("Chagua lugha", "Vinjari kwa aina ya nyenzo", ("Vitabu na vitabu pepe", "Noti na vifaa vya kozi", "Makala na miongozo ya kusoma", "Masomo ya sauti", "Video na infografiki", "Duka la vitabu"), "Katalogi inaonyesha nyenzo zinapochapishwa."),
    "fr": ("Choisir une langue", "Explorer par type de ressource", ("Livres et livres numériques", "Notes et documents de cours", "Articles et guides d’étude", "Leçons audio", "Vidéos et infographies", "Librairie"), "Le catalogue affiche les ressources au fur et à mesure de leur publication."),
}
