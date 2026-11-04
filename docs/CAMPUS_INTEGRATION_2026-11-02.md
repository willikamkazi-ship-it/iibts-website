# OBTS website → maktaba na dashboard zilizopo

Msingi wa website: PR #1, 1720f21. Mkataba wa endpoints umehakikiwa kutoka portal_routes.py ya backend PR #2, 95eaea3. Hakuna backend iliyobadilishwa katika kazi hii.

## Kilichotekelezwa

Kurasa portal.html na library.html kwa EN/SW/FR sasa zina sehemu ya kufungua kiungo binafsi kilichotolewa na OBTS. Hakuna login mpya, student ID mpya, nenosiri jipya au database mpya iliyotengenezwa.

Kiungo kinachokubalika kina origin iliyosanidiwa CAMPUS_ORIGIN na path /dashboard pamoja na token t moja. Script inajenga destination iliyowekwa (/dashboard au /library) na lang=en/sw/fr kutoka ukurasa wa website. Haihamishi query parameters zisizohitajika, haitoi access bila token na haibadili muda wa token. Token halisi inathibitishwa na backend pekee. Hakuna token halisi iliyoingizwa kwenye source, logs au majaribio.

Origin ya sasa ni production iliyotambuliwa katika ukaguzi wa Render: https://odm-ai-asistant.onrender.com. Scheme nyingine, origin nyingine, userinfo, hash, token tupu/zinazorudiwa na path za staff zinakataliwa. Website haina fetch ya data binafsi wala CORS mpya. Inapeleka mwanafunzi kwenye huduma iliyopo baada ya yeye kubonyeza kitufe. Kiungo hakihifadhiwi katika localStorage/sessionStorage.

Kurasa zote zimeongezewa referrer policy no-referrer. Backend nayo inapaswa kuthibitisha sera ya referrer/no-store kwenye kurasa zake zenye token; sera ya website pekee si sera ya response ya backend.

## Ukaguzi

- Build source consistency na static checks za kurasa 42: PASS.
- Registration checks 6: PASS.
- Campus-link checks 8: PASS, ikiwemo chaguo la lugha tatu na destination ya maktaba, origin potofu, credentials, http, token tupu/zinazorudiwa na data isiyofaa.
- Browser: kurasa sita za maktaba/dashboard zimefunguliwa; form inaonekana, button inawashwa na hakuna horizontal overflow kwenye desktop.
- Browser: submit bila kiungo imekataliwa, kosa limeonekana na focus imerudi kwenye input.
- Hakuna valid student session iliyofunguliwa, hakuna DB read kupitia session, hakuna WhatsApp send, deploy au merge. Hakuna end-to-end authentication iliyodaiwa.

## Mapungufu yanayohitaji backend kabla ya kufungua huduma

1. Kutoa kiungo binafsi halisi kwa OBTS-SW-000005 kupitia utaratibu uliopo; njia ya kuomba/kutuma kiungo haijathibitishwa kufanya kazi.
2. Dashboard ya backend bado ina headings, labels na makosa mengi yaliyogongomewa Kiswahili. Query lang huchagua maudhui lakini si tafsiri kamili ya UI; EN/FR bado zinahitaji kukamilishwa. Maktaba ina LIBRARY_WORDS ya lugha tatu.
3. Jaribu token halali, iliyokwisha muda na iliyobadilishwa; mwanafunzi aone data zake tu, nyenzo alizoruhusiwa tu na asione nyenzo za mhadhiri.
4. Thibitisha migrations, database na huduma live. Mabadiliko haya ya website hayaweki huduma ambayo haijachapishwa kuwa live.
5. Endelea kuhifadhi PREVIEW=True/noindex na taarifa za huduma ambazo hazijafunguliwa mpaka uzinduzi uidhinishwe.

Hii ni hatua ya kuunganisha njia ya akaunti iliyopo, si kukamilika kwa mfumo mzima. Muundo uliorejeshwa kutoka IIBTS unaendelea chini ya jina OBTS.
