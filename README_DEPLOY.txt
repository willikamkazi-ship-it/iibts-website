OBTS — Online Bible & Theology School: public website (static, GitHub Pages)

The pages are generated: edit tools/build_site.py, then run
    python3 tools/build_site.py
English pages are at the root, Kiswahili in sw/, French in fr/.
Shared files: assets/css/site.css, assets/js/site.js, assets/img/ (approved
OBTS logo and seal, resized without stretching).

Tests (also run by .github/workflows/site-check.yml):
    python3 tools/build_site.py --check
    python3 tools/check_static.py
    node tools/check_registration.cjs
    node tools/check_campus_link.cjs
    NODE_PATH=$(npm root -g) node tools/check_site.cjs [screenshot_dir]

PREVIEW = True in tools/build_site.py shows a "not yet published" banner,
adds noindex and a robots.txt that blocks indexing. Set it to False and
regenerate only with the launch instruction.

The old IIBTS pages (programs, policies, campus, library, news,
scholarships, standards, support) now redirect to their OBTS replacement.
Draft lessons, answer keys and lecturer guides are never stored here.

2026-10-31 recovery: the latest source was recovered from the OBTS system's
docs/launch/obts-website.bundle at 71f677d, retaining all eight saved commits.
See docs/WEBSITE_REVIEW_2026-10-31.md for validation and launch boundaries.
