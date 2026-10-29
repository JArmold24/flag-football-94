# Flag Football '94: App Store submission sheet

Everything to paste into App Store Connect, in the order the screens ask for it. Character limits are checked.

## App information
| Field | Value |
|---|---|
| Name (30) | `Flag Football '94` |
| Subtitle (30) | `Retro 5-on-5 Flag Football` |
| Bundle ID | `com.jarmold.flagfootball94` (register this exact ID in Certificates, Identifiers & Profiles, or change it in `native/capacitor.config.json` and the Xcode project) |
| SKU | `ff94-ios-001` |
| Primary language | English (U.S.) |
| Category | Games → Sports (secondary: Games → Arcade) |
| Content rights | Does not contain, show or access third-party content |
| Age rating | Answer **None / No** to every question (no violence beyond none, no gambling, no contests, no user-generated content, no messaging, no web browsing, no ads). Expected result: **4+** |
| Copyright | `2026 <your name or company>` |

## Pricing
Pick one:
- **Paid**: set a price tier (for example $2.99). The build is ready as-is.
- **Free**: also ready as-is. A free download with a paid unlock needs extra in-app purchase code; see "Later" at the bottom.

## App Privacy
- Data collection: **"No, we do not collect data from this app"**. That gives the "Data Not Collected" label.
- The build also ships an Apple privacy manifest (`PrivacyInfo.xcprivacy`) saying the same thing: no tracking, no data collected. It declares only the UserDefaults API, which the save system uses.
- Privacy Policy URL: `https://jarmold24.github.io/flag-football-94/privacy.html`

## Version 1.0 page
- **Promotional text (170)**:
  `Call the play, tap your receiver and let it fly. A 16-bit football game built for your phone - with a full Superstar career from draft day to the Hall of Fame.`
- **Keywords (100)**:
  `football,flag,retro,16-bit,pixel,arcade,sports,career,franchise,playbook,touchdown,quarterback,coach`
- **Support URL**: `https://jarmold24.github.io/flag-football-94/support.html`
- **Marketing URL** (optional): `https://jarmold24.github.io/flag-football-94/`
- **What's New**: `First release!`

### Description
```
Five on five. No pads, no tackles - pull the flag.

Flag Football '94 is a fast, 16-bit style football game built for your phone. Pick a formation, call your play, snap it and tap the receiver you want - a tap throws a lob, a hold fires a bullet. Juke, spin and dive your way downfield, or pull flags and jump routes on defense.

SUPERSTAR CAREER
Create your player and live his whole career. Enter the draft or sign with the team you choose. Every snap earns a play grade - get open, run your route, win your matchup - and your grades build your coach's trust: rotation player, starter, featured, franchise. Earn XP, upgrade your ratings, sign in free agency, be voted captain, age, retire, and find out if your legacy makes the Hall of Fame.

A CPU THAT READS THE GAME
The computer runs a two-minute drill, burns the clock with a lead and goes for it on fourth down. On DYNAMIC difficulty it learns your habits - throw deep every play and it will notice - and it gets a little tougher with every win.

EVERYTHING ELSE
- Franchise mode: draft a team and coach it through seasons
- Three play styles: Classic, Retro Sideline and Retro Overhead
- A playbook editor to build your own routes and plays
- Broadcast-style play calls, instant replay, day and night games, rain and snow
- Game Center leaderboard and achievements
- No ads. No accounts. Plays offline.

An original game: all teams, players and logos are fictional.
```

## Screenshots
In `appstore/screenshots/`, all landscape, at Apple's exact sizes. Upload in this order:
1. `1_tap_receiver`: tap-the-receiver passing
2. `3_banner`: the touchdown banner
3. `2_playcall`: play calling
4. `4_superstar`: the Superstar hub
5. `5_draft`: draft day
6. `6_hall_of_fame`: the Hall of Fame
7. `7_overhead`: Retro Overhead style

- **iPhone 6.9"**: `iphone-6.9in/`, 2868 × 1320. App Store Connect scales these down for the smaller iPhones.
- **iPad 13"**: `ipad-13in/`, 2752 × 2064. Required, because the app runs on iPad.

## Game Center (Features → Game Center)
Turn Game Center on for the app, then create these with exactly these IDs. The game already posts to them.

**Leaderboard**: Classic, Single (best score).
| Reference name | Leaderboard ID | Score format | Sort | Display name | Image |
|---|---|---|---|---|---|
| Hall of Fame Legacy | `ff94.legacy` | Integer | High to low | `Hall of Fame Legacy` (suffix: `pts`) | `gamecenter/leaderboard_legacy.png` |

**Achievements**: 12 achievements, 1000 points in total. Images are in `appstore/gamecenter/`.
| Achievement ID | Title | Points | Before earning | After earning | Image |
|---|---|---|---|---|---|
| `ff94.first_td` | First Touchdown | 25 | Score your first touchdown in a Superstar career. | You found the end zone. | ach_first_td.png |
| `ff94.first_pick` | First Interception | 25 | Intercept your first pass. | Ball hawk. | ach_first_pick.png |
| `ff94.first_win` | First Win | 25 | Win your first Superstar game. | The first of many. | ach_first_win.png |
| `ff94.game100` | 100-Yard Game | 50 | Gain 100 yards in one game. | A hundred-yard day. | ach_game100.png |
| `ff94.hat_trick` | Hat Trick | 75 | Score three touchdowns in one game. | Three touchdowns in a game. | ach_hat_trick.png |
| `ff94.pulls8` | Flag Collector | 50 | Pull eight flags in one game. | Eight flags in a game. | ach_pulls8.png |
| `ff94.shutout` | Shutout | 75 | Win a game without allowing a point. | A shutout win. | ach_shutout.png |
| `ff94.playoff_win` | Playoff Win | 75 | Win a playoff game. | Playoff winner. | ach_playoff_win.png |
| `ff94.champion` | League Champion | 150 | Win the league championship. | Champions! | ach_champion.png |
| `ff94.td50` | 50 Career Touchdowns | 150 | Score 50 career touchdowns. | Fifty touchdowns. | ach_td50.png |
| `ff94.captain` | Team Captain | 100 | Be voted team captain. | The locker room is yours. | ach_captain.png |
| `ff94.hall_of_fame` | Hall of Famer | 200 | Retire with a legacy score of 200 or more. | Enshrined in the Hall of Fame. | ach_hall_of_fame.png |

## App Review Information
- **Sign-in required**: No.
- **Contact**: your name, phone and email (only Apple's reviewers see these).
- **Notes**:
```
Flag Football '94 is a single-player, offline football game. No account or sign-in is needed; Game Center is optional (leaderboard + achievements).

How to play: tap anywhere on the title screen, choose EXHIBITION, pick two teams and tap KICK OFF. On offense tap a formation, then a play; tap SNAP, then tap a receiver on the field to throw. SUPERSTAR MODE is the career mode (create a player, then enter the draft or sign with a team).

The game is landscape-only and supports iPhone and iPad. All teams, players, logos and names are original and fictional; the game is not affiliated with any league.
```

## Later (not needed for 1.0)
- A free download with a "Full Game" in-app purchase needs StoreKit code and a Restore Purchases button. That's a follow-up build if you choose that model.
- An app preview video (15–30 s of gameplay) is optional but very effective.
