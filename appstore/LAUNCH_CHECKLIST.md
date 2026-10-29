# Flag Football '94: road to the App Store

Done (in the repo): the native iOS project, Game Center plugin, haptics, native saves, privacy manifest, icon and splash,
store text and screenshots, Game Center artwork, privacy and support pages, the Codemagic cloud build.

In order:

1. **Enroll** in the Apple Developer Program ($99/yr), individual. Approval is usually 1–2 days.
2. **Agreements, Tax and Banking** in App Store Connect: accept the Paid Apps agreement, add the bank account
   and the tax forms (W-9 for a US individual). **Required**: the Full Game in-app purchase can't be sold (or tested in
   TestFlight) until this agreement is active.
3. **App Store Small Business Program**: apply (15% commission instead of 30%). Takes effect after approval.
4. **App Store Connect API key** (Admin): see `CODEMAGIC_SETUP.md` step 1.
5. **Register the bundle ID** `com.jarmold.flagfootball94` and **create the app record**: `CODEMAGIC_SETUP.md` step 2.
6. **Signing key + Codemagic**: `CODEMAGIC_SETUP.md` steps 3–4.
7. **First cloud build**: `CODEMAGIC_SETUP.md` step 5. This is the first compile of the Swift code; if it fails,
   send the log lines for a fix.
8. **Game Center**: app record → Services/Features → Game Center → turn it on, create the leaderboard and
   12 achievements with the exact IDs in `APP_STORE_LISTING.md` (artwork in `gamecenter/`), then add them to the
   version 1.0 page's Game Center section.
8b. **In-app purchase**: create the Full Game non-consumable (`com.jarmold.flagfootball94.fullgame`, $1.99) exactly as in
   `APP_STORE_LISTING.md`, with the review screenshot `iap_review.png`.
9. **TestFlight**: install the build on your own iPhone and play a full game, a Superstar season and a retire.
   Check: saves survive closing the app; haptics; Game Center sign-in banner; an achievement unlocks; the
   leaderboard opens from the Hall of Fame. Free version: finish one exhibition game, see the unlock screen, buy the
   Full Game (TestFlight purchases are free, sandbox), delete and reinstall, check it unlocks again (or via Restore
   Purchases). Add friends as testers.
10. **Fill the listing** from `APP_STORE_LISTING.md`: app information, pricing, App Privacy (Data Not Collected),
    age rating questionnaire, description, keywords, URLs, screenshots (iPhone 6.9" and iPad 13"), copyright,
    review notes. Price: Free; add the Full Game in-app purchase to the 1.0 version.
11. **Submit for review**: pick the TestFlight build on the 1.0 page → Add for Review → Submit. Review typically
    takes 1–3 days. Choose manual release so you control the launch day.
12. **Release** once approved.

Decided: **free download, one free exhibition game, $1.99 Full Game unlock** (built in v0.30).

Before launch: the GitHub Pages site and the claude.ai page still serve the whole game free in a browser. Decide whether
to take the playable web build down (keep only the privacy and support pages) before the App Store release.
