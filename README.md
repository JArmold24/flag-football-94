# Flag Football '94 — PC & phone build (v0.24)

A 16-bit style 5-on-5 flag football game built from the design document, with the
Madden '94 play-calling grid, passing windows, and camera, plus a **Superstar** career mode.

## Play it

Open **`FlagFootball94.html`** in Chrome or Edge (double-click it). That single file is the whole
game — no install, no internet needed. The source lives in `src/` (open `index.html` for the
multi-file dev version; `python build.py` rebuilds the single file).

Saves (settings, Superstar career, Franchise, roster edits, playbook) are stored in the browser's local storage for that file.

**On a phone or tablet** — host the `pwa/` folder on any static HTTPS site (GitHub Pages, Netlify, Cloudflare
Pages, a Dropbox/S3 public bucket...), open the link on the phone in landscape, then *Add to Home Screen*
(iOS Safari: Share → Add to Home Screen; Android Chrome: menu → Install app). It then launches like an app:
full screen, no browser bars, its own icon, and it works offline after the first load. The single
`FlagFootball94.html` file also plays in a phone browser (tap the FULL button for full screen on Android);
only the home-screen install needs the hosted folder.

**Touch controls** appear the moment a finger touches the screen: a floating stick under the left thumb,
buttons under the right thumb whose labels follow the moment (SNAP, JUKE / SPIN, PULL / SWAT, DIVE, RUN /
WINDOWS, SPRINT, SWITCH, AUD), tap a receiver window to throw (tap = lob, hold = bullet), tap a tile to call a
play (the FLIP / NO HUDDLE / RESET buttons on the play-call screen are tappable), swipe to move through menus
and tap to pick, MENU for the pause menu, REPLAY on the result screen, KEYBOARD when a name is asked for.

## Controls

Keyboard-native: every prompt on screen names the real key.

| Key | Does |
| --- | --- |
| Arrow keys or WASD | Move / navigate menus / move the play-grid cursor |
| **Space** | Snap the ball; juke (ball carrier); pull the flag or lunge (defense); dive for a pass; confirm |
| **1 2 3 4** | Throw to that receiver — the number is on his window. Tap = lob, hold = bullet |
| **E** | Spin (carrier); swat a pass (defense); hold E + Left/Right for pre-snap motion |
| Shift (hold) | Sprint |
| Tab | Switch defender |
| Enter | Pick / start |
| **Esc** | Pause menu (resume, hints on/off, quit to menu) — from anywhere in a game |
| Q | Audible at the line (then 1 / 2 / 3) |
| F / N / T | Flip play / No huddle / Timeout (play-call screen) |
| **V** | Show the called play's art before the snap (toggle) |
| **R** | Instant replay of the last play (on the result screen). In the replay: Space pause, Left/Right scrub, Up/Down camera, R speed, Enter done |
| P / M | Pause / mute |

**Play calling** — arrows move the cursor, Enter picks (or press 1–3 for a tile inside the striped
window). Formation first, then one of its 8 plays. Run plays are locked out in the no-run zones.

**Offense** — Space snaps. The passing windows open by themselves a beat after the snap; press the
number on a window to throw to that receiver (tap = lob, hold = bullet; hold an arrow to lead him).
A window flashes red when the receiver is covered. Arrows move the QB — cross the line to run with
it (by default the QB can always run; Options → QB Can Run), except in a no-run zone (hatched turf)
where it is pass only. Handoffs and pitches happen by themselves on run plays. Ball in the air:
Space dives. Ball carrier: Space jukes, E spins, Shift sprints. 7-second pass clock.

**Defense** — Pre-snap: Tab switches your defender, Q audibles. Don't cross the line before the
snap. Space pulls the flag in reach (Space away from the runner lunges), E swats a pass. Reach the
QB in the pocket and pull for a sack. Your controlled defender pulls on the button; the other four
are CPU-run and pull automatically. On Rookie (or with Auto Flag Pull on) your pulls are automatic
too. A controls card shows on the first snap of every game; Esc opens the pause menu at any time.

**Look** — players are 20×32 pixel sprites (up from 16×26): broad shoulders, a real cap with a
brim, defined thighs/calves/socks/cleats, a six-frame run cycle with knee lift and arm pump, and
every pose (throw, catch, carry, pull, hold, stumble, swat, dive, celebrate). Stands have tiers of
fans that bob, a walkway, a wall at the apron, and each sideline has a bench with the subs sitting
on it in team colors.

**Flag pulling** — the FLAG PULL rating is the dominant term in every pull: it sets the defender's
reach (0.85 yd at a 10, 1.5 yd at a 99) and his base odds (about 1 in 5 for a 10, 4 in 5 for a 90
on a square-up), before the carrier's Agility, the angle (side is best, head-on worst), a juke or
spin window, sprinting, and the catch-and-pull bonus. A miss on a runner going by at speed is a
whiff: the defender stumbles for 0.4–0.65 s (better pullers recover faster) and the runner is
gone. A miss on a slow or head-on carrier (a QB in the pocket, a runner squaring up) is a swipe: a
0.15–0.3 s recovery and one more grab. In a test with a whole defense forced to one rating, a
defense of 10s gave up 14 yards a play and a touchdown on 40% of snaps; a defense of 90s gave up 6
yards and 3.5%.

**Clock** — the game clock runs between plays like Madden: a play that ends in bounds burns a
15-second run-off through the whistle, banner and camera swing, then the play-call screen ticks
in real time (Options → Clock Run-Off: none / 10 / 15 / 20 / 25). Incompletions, out of bounds,
scores, turnovers and timeouts stop it; no-huddle (N) cuts the run-off to 4 seconds. A 6-minute
half is about 13 plays a side.

**Feel** — players carry momentum (turning at full speed takes longer, a juke is a burst that
doesn't). A juke is lateral to the direction you're running: hold left/right to pick the side, or
tap A alone to cut away from the nearest defender. Defenders close to you "bite" on the fake for a
beat. CPU pursuit works in roles: the two nearest attack, the rest take contain lanes ahead of the
runner, and a defender meeting the runner head-on breaks down and mirrors instead of flying past.

## Player graphics (v0.10–v0.11)

Players are now **pre-rendered sprites**: a jointed low-poly football player is animated in 3D
(`tools/prerender/rig.js`, `clips.js`), rendered from the game's camera angle in 8 directions,
and baked down to 16-bit style pixel cells (`tools/prerender/render.js` -> `src/sheetdata.js`).
The sheet stores part ids + shade bands, not colors, so every frame is recolored at runtime for the
team, skin tone, hair and style options (caps, headbands, sleeves, gloves, tights, cleats) — a true
palette swap. Clips: idle, QB stance, center over the ball, defender crouch, run / run with ball,
walk, backpedal (defenders) and QB drop-back, carry, throw (3), catch (2), over-the-shoulder catch (2),
flag pull (reach-grab-rip, 4) + hold, stumble (3), swat, juke L/R (2), spin, dive + landing (2),
two celebrations, two dejections, and a striped official who signals touchdown, incomplete, first
down and safety from the sideline. Players are drawn smaller relative to the field than v0.10 and the
receiver windows are ~25% shorter so more of the field stays visible.
A flag pull is now a timed two-body moment: the defender reaches, the runner is stopped as the hand
lands, the flag comes off and goes up — or the hand slips and the defender stumbles.
Rebuild the sheet with `cd tools/prerender && npm install && node render.js` (needs Playwright's Chromium);
`node preview.js --clips run,pull --zoom 8` writes a contact sheet to check the frames.

## Stadium & presentation (v0.12)

- The crowd is drawn in true perspective, scanline by scanline from a synthesized crowd texture
  (`src/stadium.js`): tiers, aisles, a concourse, the home side wearing more home colors, sections
  that bounce, camera flashes. Walls with fictional ad boards line both sidelines and the far end.
- Time of day — **day / dusk / night** (Options → TIME OF DAY, default varies per game): turf,
  stands, haze and the players' palette all shift; night games fall off into the dark at the edges.
- Field: Madden-style flat turf bands, the home team's emblem at midfield, chain crew (down box
  and line-to-gain stick) on the near sideline, bench players in uniform, a referee who signals.
- Score strip with team emblems and a possession arrow; receiver windows centered; dust on cuts,
  spins and dives; the pulled flag tumbles away; screen shake on a sack; scene fades; play-call
  diagrams no longer spill out of their tiles; menus sit over a dusk stadium.

## v0.24 — full-width phones, glass buttons, a QB who leads his man

- **Full-width on phones.** In landscape the game now fills the whole screen. The field and backdrops extend past the old 320-wide box, and menus stay centered. The touch buttons have an iPhone-style frosted glass look and respect the notch/home-bar safe areas.
- **Field size audit, no change.** The 30 x 70 yd field (50 yd goal to goal plus two 10 yd end zones) matches the tournament 5v5 spec. Players are drawn about 1/19 of the field width, close to Madden '94's chunky look. True-to-life proportions would shrink them to roughly 1/60, too small to read on a phone. The wide phone view now shows more sideline instead.
- **Classic auto-lead fixed.** The pass lead now walks the receiver's actual route ahead in time and re-solves for flight time, instead of extrapolating his current velocity. In tests, bullets landed within reach 98% of the time (was 69%) and lobs 100% (was 56%). CPU QBs lead slightly less on lower difficulty.
- **Sideline routes.** Route points are clamped 1.2 yd inside the sideline. A receiver who reaches the boundary holds for half a second, then freelances back inside to get open. In tests, 0 of 100 pass plays had a receiver step out.
- **Training Camp.** The CPU picks the defense for you. Camp ends as soon as you hit the XP cap, so you don't play reps for nothing.
- **Defaults.** Halves are now 4 minutes and run-off between plays is 10 s. Existing saves are migrated once. Season goals already scale with half length, and the safety's picks/pulls goal now scales too.
- **READ AIDS (Classic).** Turn off the colored open/tight rings and tags. With aids off, the receiver you're targeting gets a plain white ring at his feet.
- **Options show only what applies** to your Play Style (Classic-only rows hide in Retro and vice versa).
- **Back to formations.** From the play list, tap **< BACK** (or press ESC) to return to the formation screen.
- **Control Hints off** now also skips the first-snap controls card.

## v0.23 — rush rules, tap-the-receiver passing, a phone-first pass

- **Rush eligibility**: only a defender lined up on or behind the dashed rush line (7 yards off the ball) at the
  snap may cross the line of scrimmage before the ball is handed off, pitched or thrown. Your defender crossing
  early from inside the line draws **ILLEGAL RUSH** (5 yards, replay the down) — called the moment he crosses,
  and automatically declined when the offense gains more than 5 on the play. With PENALTIES off he simply can't
  cross. (The old check only looked at the snap instant and how fast you were moving, which is why it fired
  once and you couldn't recreate it.) The pre-snap hint tells you whether your defender is a rusher.
- **PASSING (Options, Classic style)**: '94 WINDOWS keeps the receiver cameras; **TAP RECEIVER** leaves the
  field clear — each receiver gets a ring at his feet and a badge over his head with the read (OPEN / LOB IT /
  BULLET / COVERED) and, on a keyboard, his number. Tap him on the field (or press his number): tap = lob,
  hold = bullet.
- **Options screen**: full-size rows with − / + buttons on each side, like the Superstar screens, scrolling 11
  at a time.
- **Phone-first text**: every footer and hint is rewritten for touch (OK / BACK / the button names instead of
  ENTER / ESC / SPACE / letter keys), the How to Play pages have touch versions, name entry points to the
  KEYBOARD button, and the playbook editor is fully touch-capable (tap a formation, a slot, a player on the
  field; buttons for every action; tap the field to drop route points). On wide phones the top-right buttons
  (PLAY ART, replay controls) stack down the side bar instead of covering the scoreboard.

## v0.22 — hi-res sprites

- **The players are rendered at twice the detail.** The sprite sheet is pre-rendered at 2 sprite pixels per
  game pixel (a standing player is 46 sprite pixels tall instead of 23) and the canvas draws at two device
  pixels per game pixel, so every sprite pixel lands on its own device pixel while the field, lines, fonts and
  HUD keep their 16-bit pixel size. Rounded torso, shoulders and shorts replaced the boxes in the rig; the
  stripe shading, outlines, eyes and jersey digits were rebuilt for the finer grid. Sprites move in
  half-pixel steps. Throw (6 frames), catch (4) and flag pull (7) got in-between frames.
- The single-file build is bigger (about 6 MB) because of the sheet; it still loads offline once cached.

## v0.21 — sprint tank, Madden-style defensive art, a passing game you can read

- **Sprint is a per-play tank.** Holding SHIFT (or SPRINT) drains a bar that now shows under the player you
  control: a full tank is ~2.3 s of sprint for a low STAMINA rating, ~3.3 s for a high one; it refills slowly
  while he jogs, and once he is gassed (red) he cannot sprint again until it is back to a quarter. Every player
  starts each play with a full tank.
- **Defensive play art reads like modern Madden** — on the play-call tiles, the audible tiles and the field:
  red arrows for rushers / blitzers, a line and ring to the receiver for man coverage, zone bubbles colored by
  type (light blue flat, yellow hook, dark blue deep, purple QB spy), with a color key on the play-call screen.
- **Passing is decided by the read, not the dice.** Each window now tags the coverage: OPEN, LOB IT (the
  defender is underneath — a lob sails over him), BULLET (he is trailing / over the top — a bullet beats him
  to the spot) or COVERED (he is draped on the receiver). A contested catch is resolved from the geometry at
  arrival — who is nearer the ball, where the defender sits along the flight line, the throw type against that
  position, hands vs. coverage, a swat or a dive — with only a small random band on top; the human QB's
  scatter was tightened (the read is the skill test, not the dice), and the CPU quarterback now picks lob or
  bullet by the same read and stops throwing into draped coverage. Throwing a bullet into a man underneath,
  or lobbing to a man over the top, is how you throw picks now. A lob caught over a trailing defender uses
  the high-point catch animation. Tap = lob, hold (0.2 s) = bullet, hold an arrow while throwing to lead the
  receiver (on top of the automatic lead for his speed).
- Groundwork for the hi-res sprite pass: the canvas now renders at two device pixels per game pixel (the
  16-bit look is unchanged), sprites are placed on the finer grid, and the animation clips can carry more
  frames.

## v0.20 — drawn sprites, smoother motion, play art on the turf, bigger Superstar screens

- **Sprites are shaded like pixel art now, not lit like a render.** The pre-render no longer quantizes
  per-pixel lighting (which left every limb a dither of three tones); each body part is shaded by where a
  pixel sits inside its own silhouette — a highlight band down the lit edge, a shadow band (two on wide
  parts) down the far edge, a shadow row along the underside, and a contact shadow where a nearer part
  (an arm across the chest) meets a farther one. The stripes stay put from frame to frame, arms separate
  from torsos, and jersey numbers sit on a clean base tone. Palette ramps shift hue the way an artist's do
  (shadows cooler, highlights warmer), with a four-tone ramp per material.
- **Smoother motion**: the run cycle has 12 frames (was 8), backpedal and walk 8 (were 6); the stride is
  tracked as a phase so switching between run, walk and backpedal never makes the legs skip; sprite facing
  has hysteresis so a player running near a 45° boundary no longer flickers between two facings; the
  camera's dead zone blends smoothly instead of switching gains; and the main loop snaps frame timing to
  whole sim steps so 60 Hz display jitter never doubles or drops a step (the stutter you could see on a
  long run). The quarterback's throw follow-through was toned down.
- **Play art on the field**: V / PLAY ART no longer opens a panel. The offense's routes are drawn on the
  turf with each receiver's throw key beside him; the defense's assignments are drawn too — a line and ring
  to the receiver in man coverage (tagged PRESS or SOFT when the defender is playing that technique), the
  zone's ellipse, a rush arrow to the quarterback, a dotted line for a spy. The retro styles show the art by
  default before the snap; the button hides it.
- **Superstar edit screens** (Create, Look & Style, Upgrade Ratings, the Rosters look editor): full-size
  text, each option in a box with − / + buttons on either side (tap them, or LEFT / RIGHT), rating bars, a
  big "+1 FOR nn XP" button per rating on the upgrade screen (greyed when capped or unaffordable), and the
  long look-and-style list scrolls with MORE arrows.

## v0.19 — room to throw, a slower game, RETRO OVERHEAD

- **Separation**: CPU man coverage now lines up three ways on each receiver and mixes them play to play —
  **press** (on top of him, jams the release, then runs with him and is late on the cuts), **off** (the
  called cushion, 2.5–5 yards) and **soft** (bails to 6–8 yards and gives up the short stuff and the
  catch-and-run). The called coverage sets the odds (RED ZONE and MAN UNDER press most, COVER 1 and QB SPY
  play off most; Rookie plays softer, All-Pro presses more, a slower defender respects speed). Defenders
  also carry their momentum through a receiver's cut for a beat (longer for low coverage ratings and lower
  difficulties) instead of mirroring it, and the minimum cushion in off coverage went from 1.5 to 2.2 yards.
  Receivers are open (2.5+ yards) about a quarter more often at 1.5–2 seconds than in v0.18.
- **Time in the pocket**: rushers need a beat to see the ball move and come off their seven-yard spot, build
  up to speed over their first steps instead of sprinting from a standstill, and square up when they close.
  A quarterback who drops and stands there gets sacked after ~3.7 s of play time on Pro (was ~2.7), ~3.9 on
  Rookie, ~3.6 on All-Pro. The CPU quarterback's reads were slowed to match so the pass rush still gets home
  on him sometimes.
- **GAME SPEED** (Options): SLOW / NORMAL / FAST. The live play runs at 72% / 85% / 100% of real time; the
  default is NORMAL, so a game is noticeably calmer than v0.18 (FAST is the old pace). The huddle, the game
  clock, menus and replays are unaffected.
- **RETRO OVERHEAD** play style (Options → PLAY STYLE): the flat top-down map — the whole width of the field
  with the crowd above and below it, every player the same size, the offense moving right — with the same
  press-drag-release passing and swipe steering as RETRO SIDELINE. The aprons and stands are squeezed so the
  bands fit around the turf. Both retro styles now apply to **Practice** too.
- **THROW AIM** (Options): the drag-to-aim gain in the retro styles was cut by about half (MEDIUM); LOW and
  HIGH are there for a mouse or a big screen. The dead zone before a drag counts as a throw grew a little.
- Options is a scrolling list now (the last rows — SCALING, MUSIC, SOUND EFFECTS — had fallen off the
  bottom of the screen).
- Drawing order of players is now by screen row in every camera (the turned replay cameras could draw a
  far player over a near one).

## v0.18 — menus you can actually tap

- Every menu, list and option row is a tap target on a touch screen: tap a menu item to open it, a team to
  pick it, a row's value to change it (left half goes back, right half forward), a draft prospect to move the
  cursor and again to draft him, a depth-chart player to grab and another to swap, a trade target, an offer
  to sign. Dialogs take a tap (left = yes, right = cancel). On-screen OK / BACK buttons stand in for Enter
  and Esc on every screen, and screens with their own actions grow small buttons (CPU PICKS, CONFIRM, AUTO,
  PROPOSE, NEXT TEAM, SIM TO MY PICK...). Swiping still moves the highlight if you prefer.
- **Audibles show their choices**: calling an audible now puts the three options on screen as play tiles
  (the formation's first three plays, or three fronts on defense) with 1 / 2 / 3 caps; tap one or press the
  key. Before, you had to know the page by heart.
- **Play art before the snap**: V on the keyboard or the PLAY ART button shows the called play (since v0.20
  drawn on the turf rather than in a panel). Works in both play styles, on offense and defense.

## v0.17 — RETRO SIDELINE play style

Options → PLAY STYLE → **RETRO SIDELINE** (the default stays CLASSIC '94). Play calling, rules, teams, modes,
stats, replay and the whole Classic game are untouched; only the live play changes, Retro Bowl style:

- **Sideline camera**: a perspective view from the stands with both sidelines on screen and the stands in
  true perspective behind the far wall; your offense always moves to the right. Sprites face the camera
  correctly in the turned view (also fixed in the replay's sideline cameras).
- **Snap by pressing**: press and hold anywhere (finger or left mouse button) and the ball is snapped; the QB
  drops back by himself. The called routes are drawn on the turf before the snap.
- **Slingshot passing**: drag away from where you want the ball; a dotted arc and a landing ring show the
  spot (and the distance). Release to throw. The ball goes to the spot — the nearest receiver goes and gets
  it (light assist), so leading him is the skill. Second finger / right-click / E flips LOB and BULLET.
  Accuracy, arm strength, pressure and a moving QB still scatter and cap the throw.
- **Drag back to run**: an arrow pointing into the backfield means take off; release and the QB scrambles
  (the QB CAN RUN rule and the no-run zones still apply).
- **The runner runs himself**: swipe up / down to cut (a juke when a defender is close), swipe ahead for a
  burst (stamina), swipe back to stutter-step, or hold and drag to bend the run — he never stops going
  downfield. Keyboard: arrows steer, Space bursts, E stutters.
- **Defense is simulated**: call it as always, then watch from the sideline; hold Space (or SKIP) to
  fast-forward. The between-play camera slides along the sideline to the next spot.
- Classic's passing windows, stick control and defensive control are all still there under CLASSIC '94.

## v0.16

- **The football**: drawn properly — a striped, laced brown ball with a top highlight and an underside
  shadow, in 16 orientations and two sizes. A pass spirals along its path, nose up on the way out and down
  on the way in; a pitch points at the back; a dead ball lies on the turf. The carried ball is a little
  bigger with a visible lace.
- **Jersey numbers** shrunk to a 5x4 badge (2x4 micro digits; a single digit is 3x4) instead of covering the
  whole chest.
- **Phones and tablets**: touch controls (above), the picture fills a small screen instead of sitting at
  integer scale, full-screen and landscape lock on Android, a wake lock so the screen stays on, a "turn your
  phone sideways" card in portrait, and all on-screen prompts name the touch buttons instead of keys.
- **Installable app (PWA)**: `python build.py` now also writes `dist/pwa/` — the game page with a web-app
  manifest, icons and a service worker that caches it for offline play. Hosted over HTTPS it installs to the
  home screen on iOS and Android and runs full screen.

## v0.15

- **Instant replay**: every live play is recorded; touchdowns replay themselves in slow motion from the
  sideline, and **R** on any result screen replays the whole play from the TV angle. Four cameras
  (TV, both sidelines, end zone), 1/4 - 1/2 - full speed, pause and scrub.
- **Presentation loop**: a pregame matchup card (stadium at tonight's light and weather, both
  emblems, home / visitors, team strength, conditions, week or playoff round), a line of color
  commentary under every result banner, and a player of the game on the final stats screen.
- **Sprites redrawn as pixel art**: the bake now cel-shades every part into three flat tones with the
  light fixed upper-left (the classic light / base / dark stripes on a limb), instead of a lambert
  gradient cut into bands. Faces are stamped like a sprite artist draws them (a flat skin tone that
  never falls into the brim's shadow, a dark eye line placed from the 3D anchors, eye black when
  worn), caps and hair are true partial domes (a bug had every cap swallow the whole head), inner
  lines only where a limb crosses the body, no isolated shade or line pixels, and very dark team
  colors are lifted so the black outline still reads. Proportions moved toward hand-drawn sports
  sprites: bigger head, longer neck, thicker arms and legs, bigger hands and feet, a deeper chest, a
  2-px flag, and side views turned 24 degrees toward the camera so a profile is not a sliver.
- **Animation**: the throw gets a follow-through (4 frames), the catch a tuck (3), the flag pull a rip
  (5), the dive a launch frame (2), the pre-snap stance breathes (2), and a player who falls on a whiff
  gets back up (3) before he can run again. Raised-arm poses (celebrations, flag held up, overhead
  catches, official's signals) were rebuilt on a shoulder joint whose "out" angle spreads a raised arm
  instead of crossing it over the head. The sheet holds 2,752 frames.

## v0.14

- **Body types**: three builds (slim / average / stocky) and three heights, assigned from position and
  ratings and editable in the look editor. The sheet now holds 2,560 frames.
- **Animation coverage**: whiff-and-fall, hurdling a downed defender, chest / one-handed / over-the-
  shoulder catches, jump pass under pressure, spike / flex / dance celebrations, hands-on-head
  dejection, kneeling in the huddle, the QB pointing out the defense, and the runner reacting to a pull.
- **Pixel cleanup** in the bake: orphan pixels and nubs removed, pinholes filled, shading speckle quieted.
- **Heads and faces**: goatees and beards, visors, high-top and afro hair, two more skin tones and hair
  colors, a square jaw on stocky builds.
- **Sound**: a reactive crowd bed (home fans roar for home plays, groan at failures, rise while a pass
  is in the air), a real whistle, first-down / cheer / groan / two-minute / final stingers, a quiet
  play-call loop.
- **Weather** (Options → WEATHER, varies by default): rain darkens and wets the turf with a 5% catch
  penalty and slicker cuts; snow whitens the stands, builds up on the field over the game and slows
  everyone a little.
- **AI & depth**: play-action is now sold (QB fakes, defenders near the line bite); All-Pro defenses
  disguise coverage 30% of the time; man coverage shades to the sideline and presses in the red zone;
  the CPU QB avoids bracketed receivers; **hot routes** for the human offense (1-4, then an arrow).

## v0.13

- Player scale re-measured against the field: sprites are now ~1.5x true height and ~2.2x true
  width at mid-screen (Madden '94 ran about 2.3x and 5x), and far players shrink with the field.
- Huddle break: the offense huddles behind the ball and the defense sets up, then everyone jogs to
  his mark; the snap waits until the formation is set. No-huddle (N) skips it.
- Sideline crew: a coach at each bench, TV cameramen tracking the line of scrimmage; a scoreboard on
  the far end stands shows the live score and clock.
- Distant crowd rows sample a box-filtered half-res texture (no sparkle); smaller midfield emblem.
- Drawn lettering (gradient, outline, shadow) for the title logo and the result banners.

## Teams

16 original teams in familiar city colorways (Atlanta Talons, Miami Sharks, New England Colonials,
Philadelphia Liberty, Pittsburgh Forge, Buffalo Blizzard, New Orleans Gators, Dallas Horsemen,
Green Bay Lumberjacks, Chicago Grizzlies, Minnesota Comets, Kansas City Stampede, Denver Yetis,
San Francisco Miners, Seattle Ospreys, Las Vegas Outlaws). Nicknames, cap emblems and every player
name are invented; no league marks or real names appear. Atlanta's #7 quarterback (J. Hawthorne)
has 99 speed, 99 agility and a 99 arm.

Every team has an original pixel emblem (play-call screen, banners, team cards).

**Rosters** (main menu) lets you rename and renumber any player on any team, and (C) restyle him;
edits are saved in the browser and "Reset this team" restores the defaults.

**Player style** — every player has a look: skin tone, hair color, and a style kit: headwear (cap,
backwards cap, headband, skull cap), hair style (short, long, bald), eye black (none / style 1 /
style 2), arm sleeves (none / one arm / both) in team, white or black, gloves (white, black, team,
gold), legwear (shorts, black tights, team tights, high socks), cleats (black, white, team, gold)
and an accent color for the headband, skull cap and sock stripe. Generated rosters get varied
styles so a field looks like a real league; your Superstar's is fully editable.

**Playbook** (main menu) is the play editor. Pick a formation and one of its 8 slots, then assign
library routes or draw custom ones (up to 5 waypoints), set the A/B/C/D reads, make it a run
(pick the carrier, draw the path, handoff or pitch), name it, and save over that slot. The book
stays capped at 8 plays per formation, so a new play always replaces one; R restores the stock
play. Your plays show up in the play-call grid and as audibles; the CPU keeps the stock book.

## Modes

* **Exhibition** — any two of the 16 teams, you vs. the CPU.
* **Superstar** — create a player (name, look & style, offensive + defensive position, ratings),
  pick a team, and play locked to him on both sides of the ball. XP for yards, catches, TDs,
  flag pulls, picks, sacks and deflections, plus a win bonus, 19 career milestones (first TD,
  100-yard game, two-pick game, 1,000 career yards, a title...), three season goals set by your
  positions, and season awards (Pro Bowl, All-Pro, MVP, a ring). All-Pro difficulty pays 1.25x,
  Rookie 0.8x. Career XP sets your level, Rookie through Hall of Famer; each level raises the
  rating cap by 2 (85 at level 1, 99 at level 8) and level 6 unlocks gold gloves and cleats.
  Upgrades get dearer up the scale; the key ratings for your two positions cost 15% less. A game
  grade (A+ to F), a trophy case, season review, career and season stats, and an editable style.
  7-game season, top 4 make the playoffs, then a new season with fresh goals. **Training camp**
  once a week: six plays against a coverage you pick, up to 40 XP (scaled by difficulty). At
  level 5 you are **team captain** and your teammates play +2 across the board. Your **contract**
  (two seasons to start) ends in offers: a re-sign if you earned it, a contender, and a
  rebuilding club with a bigger signing bonus — change teams or stay.
* **Franchise** — GM and coach. Pick a team for its colors, then a draft lottery (sixteen balls
  in a drum, picks revealed 16 to 1) sets the order for an 8-round snake fantasy draft of every
  player in the league. On your pick, sort the board by overall, position, age or any single
  rating, filter by position, draft (A) or take the CPU's best available (B); Enter sims the CPU
  picks, which draft by need. Then play or sim each game, set the depth chart (top five start),
  check standings, league rosters and stat leaders (simulated games get a generated box score,
  so the league has leaders in passing, receiving, pulls, picks and sacks). **Trades**: one-for-one
  with any CPU team, three a season, deadline week 5; the CPU weighs overall, age and need and
  won't give up its only QB or center. Top 4 make the playoffs. **Offseason**: players age (the
  young improve, the old decline, 35-year-olds retire), then a two-round **rookie draft** of a
  40-man class, worst record picking first, then **final cuts** back to eight. Seasons repeat
  with the roster you build.
* **Practice** — pick the defense, then your play. No clock, same spot (your own 15) every snap. Esc quits.
* **Options** — half length, downs, difficulty, two-minute clock stops, timeouts, penalties,
  interception spot, auto pull, hints, scanlines, pixel-perfect vs. fill-window scaling, audio.

## Rules implemented

5-on-5, no contact; drives start at the own 5; 4 downs to cross midfield, 4 to score (configurable);
no-run zones 5 yards before midfield and the goal line (no runs, no QB keepers); ball spotted where the ball is at the pull;
diving catch is down at the catch; TD 6, then 1 pt from the 5 (pass only) or 2 from the 10;
safety 2; interceptions are live; sacks (the QB can be pulled in the pocket; the CPU QB feels
the rush by his Agility and a fast one takes off around it) and end-zone pulls; overtime by alternating conversion
tries; penalties: delay of game, offside, illegal rush, flag guarding (spin into a defender).

## Not in this build (next up)

Mobile/touch controls, two-player, online, instant replay, audible presets (the editor is built to
feed them), laterals/pitches after the catch, multi-player trades and free agency.
