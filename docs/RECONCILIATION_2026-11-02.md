# Kuunganisha kazi mbili za website

Msingi wa PR #1 uliothibitishwa: ccaaa87. Bundle ya agent imechukuliwa kutoka repo private odm-ai-asistant, tawi faragha/kwa-mmiliki-website-2026-11-02, faili website-2d51812.bundle. git bundle verify imefaulu; commit ya agent ni 2d518127a654ce892107f414134909d58ae21a57, juu ya 1720f21.

Kazi imeunganishwa bila kurudisha PR nyuma: .gitignore, ripoti ya agent na SERVICE_BASE vimeongezwa juu ya campus-link validation/referrer safeguards za ccaaa87. Ripoti ya agent inabaki rekodi ya kikao chake; vipimo vyake 5,828 havijatangazwa kuwa vipimo vipya vya kazi iliyounganishwa.

SERVICE_BASE inabaki tupu. Hii sasa inazima kiungo cha maktaba ya umma na form zote za personal campus link mpaka production ithibitishwe. Maandalizi ya form na vipimo vyake hayajafutwa; yanawashwa na usanidi huo mmoja baada ya endpoints kuhakikiwa. Kuwasha maktaba hakufungui dashboard bila token; backend inaendelea kuthibitisha token na ruhusa.

Anwani inayokubaliwa ni HTTPS origin halisi ya production pekee. Staging, http, host inayofanana, credentials, path, query na fragment zinakataliwa. Domain ya huduma ikibadilika, badilisha CAMPUS_ORIGIN na ihakiki kabla ya SERVICE_BASE.

Nyenzo za kwa_mmiliki/ hazijachukuliwa wala kupakiwa kwenye repo hii ya public. .gitignore inazuia kwa_mmiliki/ na __pycache__/. Bundle imehakikiwa kuwa na marekebisho manne ya website tu. Repo ya faragha ina orodha ya nyenzo; checksum za PDF/picha hazijarudiwa hapa.

Vipimo vya kazi iliyounganishwa: build consistency na static checks za kurasa 42; registration cases 6; campus-link cases 8; production-origin checks 6 na lugha tatu za gate. Hakuna merge, deploy, DNS, backend write, student message au live authentication iliyofanywa. PREVIEW=True inabaki.
