# Website ya OBTS: maandalizi ya uzinduzi

Tarehe: 31 Oktoba 2026.

## Chanzo kilichorejeshwa

GitHub main ilikuwa 47f6764 (website ya zamani). Bundle iliyohifadhiwa ndani ya odm-ai-asistant imethibitishwa na git bundle verify na kurejeshwa kwa commit 71f677d. Hii ina commits nane za kazi ya website, ikiwemo mtaala na marekebisho ya jina rasmi na lugha tatu. Hakuna kazi hiyo iliyoandikwa upya.

Tawi jipya la ukaguzi: codex/website-launch-20261031. Usibadilishe tawi la backend kwa kazi ya tovuti hii.

## Kilicho tayari

- Kurasa 14 katika kila lugha: EN, SW, FR; jumla 42. Mwanzo, kuhusu, kozi, jinsi ya kujifunza, usajili, mawasiliano, maswali, faragha, masharti, maktaba, duka, dashboard, msaidizi wa AI na mtaala.
- Nembo na utambulisho uliopo wa OBTS, bluu/ivory/dhahabu.
- Fomu ya kuandaa ujumbe wa WhatsApp: uthibitishaji wa taarifa, ridhaa, kuonyesha kosa na kuelekeza focus, kutokubali kozi iliyozimwa, kitufe cha kuendelea popup ikizuiwa, na njia ya mawasiliano JavaScript ikiwa imezimwa.
- Kuondoa ujumbe ulioandaliwa baada ya taarifa kuhaririwa; hakuna PII inayohifadhiwa na fomu kwenye browser storage.
- Menu inafungwa kwa Escape na focus inarudi kwenye kitufe.
- Canonical na hreflang za homepage zina URL zinazolingana.

## Ukaguzi uliofanyika

- python tools/build_site.py --check: PASS.
- python tools/check_static.py: kurasa 42 PASS (chanzo, links, assets, lugha, heading na metadata).
- node tools/check_registration.cjs: hali 6 PASS, pamoja na simu yenye nafasi nyingi, popup isiyorudi, kubadilisha taarifa, kozi iliyozimwa na ridhaa.
- node --check assets/js/site.js na git diff --check: PASS.
- Cloud browser: kurasa zote 42 zimefunguliwa; hakuna ukurasa uliokosa h1, picha iliyokosekana au horizontal overflow kwenye viewport ya desktop iliyotumika.
- Fomu tupu ya SW imekataliwa kwenye browser, kosa limeonekana na focus imerudi kwenye jina.
- Mwonekano wa homepage na admissions wa SW umetazamwa kwenye desktop. Browser ya simu/tablet na full existing Playwright suite hazijaendeshwa katika kikao hiki. Vipimo vya layout vya zamani vimehifadhiwa, si ushahidi mpya.
- Hakuna ujumbe wa WhatsApp uliotumwa. Hakuna full GitHub Actions run iliyoanzishwa: commit ya marekebisho ina [skip ci] kutokana na quota ambayo haijathibitishwa kurejea.

## Kabla ya kuchapisha

PREVIEW=True na noindex vimehifadhiwa. Dashboard, maktaba, duka na AI zinaeleza kuwa bado hazijafunguliwa. Hizi ni kurasa za taarifa; si uthibitisho kwamba backend au malipo yanafanya kazi. Agent wa mfumo akithibitisha endpoints za production, ziunganishwe na kutest login/ruhusa halisi kabla ya kusema huduma imefunguliwa.

Usajili wa website huandaa ujumbe wa WhatsApp; hauundi mwanafunzi kwenye database wenyewe. Utaratibu wa backend wa WhatsApp ndio wa kuendelea kuthibitisha. Ada na tarehe ya uzinduzi hazijatangazwa kama ukweli uliothibitishwa. Hakuna akaunti, nenosiri au rekodi ya mwanafunzi iliyoingizwa kwenye repo hii ya public.

Kuchapisha kunahitaji ruhusa ya kubadilisha preview/live kulingana na maelekezo yaliyopo. Hakuna merge ya main, deploy, DNS au domain iliyobadilishwa. Domain obts.co.tz ni thamani iliyokuwapo kwenye chanzo; umiliki na DNS hazijahakikiwa katika kikao hiki.
