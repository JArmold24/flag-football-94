# Building the iPhone app in the cloud (Codemagic) — no Mac needed

The repo already holds everything the build needs: the Xcode project (`native/ios/`), the shared `App` scheme,
the Game Center plugin, the icon and splash, the privacy manifest and `codemagic.yaml` at the root. What's
left is linking your accounts. It takes about 20 minutes, once.

**Before you start** you need: the Apple Developer Program membership active, and the Paid Apps agreement accepted
(only needed if you sell the app; the Free Apps agreement is automatic).

---

## 1. Create the App Store Connect API key (Apple)
1. Go to **appstoreconnect.apple.com → Users and Access → Integrations → App Store Connect API**.
2. If asked, click **Request Access** and accept; then **Team Keys → Generate API Key** (the **+**).
3. Name it `Codemagic`, set Access to **Admin**. Admin is needed because the build creates your distribution
   certificate and provisioning profile for you.
4. **Download the .p8 file** (Apple lets you download it only once — keep it safe). Note the **Issuer ID**
   (top of the page) and the **Key ID** (in the key's row).

## 2. Register the app's ID and create the app record (Apple)
1. **developer.apple.com → Account → Certificates, Identifiers & Profiles → Identifiers → +**
   → App IDs → App → Description `Flag Football 94`, Bundle ID **Explicit** `com.jarmold.flagfootball94`.
   Game Center is included for every app ID automatically; leave the other capabilities off. Register.
2. **appstoreconnect.apple.com → Apps → + → New App**: iOS, Name `Flag Football '94`, language English (U.S.),
   Bundle ID `com.jarmold.flagfootball94`, SKU `ff94-ios-001`, User Access Full Access. Create.

## 3. Make the signing key (on your PC, 1 minute)
The build uses this private key to create your App Store certificate. It stays in Codemagic as a secret.
1. Open **PowerShell** (Start → type PowerShell).
2. Run:
   ```powershell
   ssh-keygen -t rsa -b 2048 -m PEM -f "$env:USERPROFILE\Desktop\ios_distribution_private_key"
   ```
   Press **Enter twice** when it asks for a passphrase (no passphrase).
3. Two files appear on your Desktop. Open `ios_distribution_private_key` (the one **without** `.pub`) in Notepad.
   You'll paste its whole contents, from `-----BEGIN RSA PRIVATE KEY-----` to `-----END RSA PRIVATE KEY-----`, in step 4.4.
   Keep this file; if you lose it, a new key simply makes a new certificate.

## 4. Connect Codemagic
1. Go to **codemagic.io → Sign up with GitHub**. Choose a personal account. The free tier includes 500 build
   minutes a month on Mac mini M2 machines; one build of this game takes about 8–12 minutes.
2. **Add application** → GitHub → pick **JArmold24/flag-football-94** → project type **Other** (codemagic.yaml).
   Codemagic reads `codemagic.yaml` from the repo.
3. **Team settings → Team integrations → Developer Portal → Connect** (App Store Connect):
   - **API key name**: `ff94` ← must be exactly this; `codemagic.yaml` looks for this name
   - **Issuer ID** and **Key ID** from step 1
   - Upload the **.p8** file
4. Open the app in Codemagic → **Environment variables** tab → add:
   - Variable name `CERTIFICATE_PRIVATE_KEY`
   - Value: the whole key from step 3
   - Group: type `ios_signing` and create it
   - **Secure**: checked
   → Add.

## 5. Run the first build
1. In the app on Codemagic: **Start new build** → branch `main` → workflow **iOS → TestFlight** → Start.
2. What it does: installs the web layer and syncs it into the Xcode project, sets the build number,
   creates (first run) or reuses your App Store certificate and profile, builds and signs the `.ipa`, then uploads it
   to App Store Connect.
3. About 10–30 minutes after the build goes green, the build shows in **App Store Connect → your app → TestFlight**
   (Apple processes it first; you get an email).

Later builds: push your changes and click Start new build again, or push a git tag starting with `ios-`
(`git tag ios-1.0-b2 && git push --tags`) to start one automatically.

---

## If the first build fails
This is the first time this native code compiles anywhere (the Swift can't be compiled without a Mac), so a red
first build is possible. In Codemagic, open the failed step, download the log (`xcodebuild_logs` in Artifacts),
and send me the error lines — fixes are usually a line or two.

| Message | Cause → fix |
|---|---|
| `No matching profiles found` / `Cannot find bundle ID` | Step 2.1 not done, or a typo in the bundle ID |
| `Unauthorized` / `401` / `NOT_AUTHORIZED` | Integration not named `ff94`, wrong Issuer/Key ID, or the key isn't Admin |
| `CERTIFICATE_PRIVATE_KEY ... not found` | The variable isn't in a group named exactly `ios_signing` |
| `There is a problem with the request entity — maximum number of certificates` | You already have 3 distribution certificates; revoke an unused one in Certificates, Identifiers & Profiles |
| `Missing Compliance` in TestFlight | Shouldn't happen (the app declares no non-exempt encryption) — answer "None of the algorithms mentioned above" |
| `Invalid Pre-Release Train` / build number | Build number already used; start the build again (the number goes up each time) |

## TestFlight for friends
- **Internal testers** (up to 100 people you add to your App Store Connect team): available as soon as Apple
  finishes processing. They install the **TestFlight** app and accept the invite.
- **External testers** (anyone with a link): TestFlight → **Test Information** (beta description, feedback email),
  create an external group, add the build. The first build gets a short beta review (usually under a day). Then
  you can share a public link. To make future builds go to that review automatically, set
  `submit_to_testflight: true` in `codemagic.yaml`.
