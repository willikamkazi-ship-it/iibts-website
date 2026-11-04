# Website ya OBTS: ukaguzi wa 2 Novemba 2026

Msingi: PR #1 `1720f21` (`codex/website-launch-20261031`). **Website haijakamilika kama huduma:** maktaba, dashboard, duka na msaidizi wa AI bado ni kurasa za taarifa ("Bado haijafunguliwa"). Hakuna merge, deploy, mabadiliko ya DNS, `PREVIEW=False` wala kuchapisha kulikofanywa.

## `kwa_mmiliki/` (haipo kwenye repo hii)
Folda ya ndani `kwa_mmiliki/` ilikuwa na faili 25: PDF na picha za ukaguzi wa GB-P001 v0.6, iliyogawanywa sehemu mbili. Ni rasimu za masomo ambazo bado hazijaidhinishwa, kwa hiyo **zote ni binafsi**. Hakuna faili ya website ndani yake.
- Zimehifadhiwa kwenye repo **private** `odm-ai-asistant`, tawi `faragha/kwa-mmiliki-website-2026-11-02`, pamoja na `SHA256SUMS_ZOTE` (faili 23 zimehakikiwa).
- Seti ya 2026-10-27 ni sawa, byte kwa byte, na `ukaguzi_mwonekano/2026-10-27_P001_sehemu/` ya tawi `vifaa-v4-uzalishaji`.
- Mmiliki amepewa nakala ya ZIP.
- Hakuna faili iliyofutwa. `.gitignore` sasa inazuia folda hiyo kuingia kwenye repo hii ya public.

## Kilichopimwa leo (kikao cha cloud, Chromium iliyosakinishwa)

| Kipimo | Matokeo |
|---|---|
| `python3 tools/build_site.py --check` | PASS (hakuna ukurasa uliopitwa na wakati) |
| `python3 tools/check_static.py` | Kurasa 42 PASS, pamoja na vipimo vipya vya `SERVICE_BASE` |
| `node tools/check_registration.cjs` | Hali 6 PASS, hakuna ujumbe uliotumwa |
| `node tools/check_site.cjs` | **Ukaguzi 5,828, makosa 0** kwa simu (360), tablet (820) na kompyuta (1366), EN/SW/FR. Unakagua: hakuna kosa la script, hakuna kusogea pembeni, kila kiungo na picha ya ndani inafunguka, menu na kubadili lugha vinafanya kazi, namba ya WhatsApp ni ya shule, fomu inakataa taarifa pungufu, na hakuna ada, mabaki ya IIBTS wala rasimu. Picha 27 zimehifadhiwa |

Kisichopimwa: simu halisi, Safari/iOS na Firefox, na anwani ya umma (website haijachapishwa).

## IIBTS → OBTS
Kila njia ya website ya zamani (`main` `47f6764`) bado ipo, na kurasa za zamani zinaelekeza kwenye kurasa za OBTS (`REDIRECTS` kwenye `tools/build_site.py`):

| Ukurasa wa zamani | Unaelekeza kwenye |
|---|---|
| programs | courses |
| policies | privacy |
| campus | how-to-learn |
| news | index |
| scholarships | admissions |
| standards | about |
| support | contact |

Kubadili lugha kunampeleka mtumiaji kwenye ukurasa uleule kwa lugha nyingine. Kwa mfano, `portal.html` → `sw/portal.html` → `fr/portal.html`.

## Njia ya mwanafunzi (kwa ukweli)
1. **Website, ukurasa wa usajili:** fomu **inaandaa ujumbe wa WhatsApp tu**. Haiandiki database wala kuhifadhi taarifa kwenye browser.
2. **WhatsApp, bot ya ODM (production `main`):** lugha → jina → nchi → usajili kukamilika na namba ya mwanafunzi → maelekezo ya malipo.
   - Ada iliyo kwenye code ni `WEEKLY_ACCESS_FEE` (siku 7), na code haina ada ya usajili tofauti.
   - Website haionyeshi bei: `check_site.cjs` inakataa "TZS" kwenye kurasa, kwa sababu ada haijatangazwa rasmi.
3. **Malipo:** msimamizi anathibitisha kupitia `/admin/verify-payment/<id>`, na hapo access ya siku 7 inafunguliwa. Website haina sehemu yoyote ya malipo.
4. **Somo:** `KSW GB-101`, `PDF GB-101` na `DONE GB-101` kwenye WhatsApp. Kwa production, DONE inahitaji migration ya `progress` (ODM PR #2 `95eaea3`, `docs/audit/ROLLOUT_2026-11-01.md`).
5. **Dashboard:** kiungo binafsi `/dashboard?t=…` kinatoka backend kupitia WhatsApp. Route hiyo iko kwenye ODM `ci-review`/PR #2 (staging) pekee, **si kwenye production `main`**.

## Kuunganisha maktaba na dashboard: hali na kizuizi

| Huduma | Route ya backend | Production (`main`) | Kwenye website |
|---|---|---|---|
| Maktaba | `GET /library?lang=en\|sw\|fr` (`portal_routes.py`) | **Haipo** | `SERVICE_BASE` (mpya, tupu). Ikiwekwa kwa anwani ya production iliyothibitishwa, kitufe "Fungua maktaba" kitafungua `/library?lang=<lugha ya ukurasa>`. `check_static.py` inakataa anwani ya staging |
| Katalogi ya umma | `GET /api/library/catalogue` | **Haipo** | Haijatumika |
| Dashboard ya mwanafunzi | `GET /dashboard?t=` | **Haipo** | Inabaki kiungo binafsi cha WhatsApp; website haiwezi kuingia kwa niaba ya mwanafunzi |
| Wafanyakazi | `GET /staff/portal` | **Haipo** (main ina API za `/staff/*` tu) | Haitangazwi kwenye website ya umma |

**Kizuizi mahsusi:** route hizi hazijawa deployed kwenye production, na kikao hiki hakifiki Render, kwa hiyo hakuna endpoint iliyothibitishwa. Hakuna data ya mfano iliyowekwa, na hakuna nyenzo za mhadhiri zilizofunguliwa.

## Mwanafunzi wa majaribio
OBTS-SW-000005 (mmiliki). Tawi la ODM `claude/production-operator-0005-20261031` (`4861549`) linamfanya operator kwenye production, baada ya ruhusa ya merge na deploy.

## Ruhusa zinazohitajika
1. **Merge ya PR #1 kwenye `main`:** GitHub Pages inajenga kutoka `main`, kwa hiyo merge = kuchapisha preview ya umma (bado ina `noindex` na bango la preview).
2. **`PREVIEW = False`:** kuondoa bango na `noindex`, yaani uzinduzi wa umma.
3. **`SERVICE_BASE`:** anwani ya production, baada ya `/library` kuwa deployed na kujaribiwa huko.
4. **DNS ya `obts.co.tz`:** haijahakikiwa.
