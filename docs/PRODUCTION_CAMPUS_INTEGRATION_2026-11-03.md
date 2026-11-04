# Production campus integration — 2026-11-03

The school system's production /library and personal /dashboard routes have now been deployed and checked in SW/EN/FR. SERVICE_BASE therefore names the verified production origin. The public library can be opened in the website's selected language; private study materials still depend on school publication and account permissions.

The main entry on library and student-dashboard pages now requests a personal link through the school WhatsApp: MAKTABA or DASHBOARD. The student sends the prepared message from their registered number, and the backend issues its own 24-hour signed link. Pasting an existing link remains an optional details section. This website never mints tokens, stores personal links, creates an account or grants course access.

The existing school contact number was compared with the live WhatsApp API's business phone number and matched. Transport acceptance is not proof of delivery: a controlled backend test was accepted by Meta but its later delivery callback reported failure, so a real sender-initiated WhatsApp test remains pending. No public launch claim follows from this source update.

Validation: 42 static pages passed generation/link/language checks; six registration checks and eight personal-link validation checks passed. The browser-check script parses successfully, but its full browser suite was not rerun for this change. The previous 5,828-check result does not apply as fresh evidence to this revision.

PREVIEW remains True. Website publication, DNS changes, bookstore opening and paid AI activation have not been performed. No lesson files, lecturer materials, credentials or personal student links are included in this repository update.
