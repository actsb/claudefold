# Robot vacuums without a camera — Video and experts brief (agent 2)

Compiled 2026-11-23 for "Robot Vacuums Without a Camera 2026: LiDAR Models That Don't Film Your Home (and What You Give Up)". About 50 web searches plus direct page reads (curl/WebFetch). Tags: Official / Independent / Vendor / Weak / UNVERIFIED. Prices that appear on review cards (CNET/PCMag "at Amazon" etc.) are **not** to be published. Nothing here comes from Amazon pages.

**Big 2026 context the post should mention:** On July 28, 2026 the FCC added "foreign-produced advanced robotic devices" to its Covered List. Robot vacuums are included. Models that were authorized earlier can still be made, imported and sold; new foreign-made models need an exemption. The FCC issued a waiver so that authorized products keep getting software and firmware updates (security patches included) **through at least January 1, 2029**. Source: Vacuum Wars, Amanda Cartwright, published 2026-07-30, updated 2026-09-09, https://vacuumwars.com/fcc-restricts-future-foreign-made-robot-vacuums-existing-models-unaffected/ [Independent]. PCMag's Nov 2026 list says all its picks are unaffected and available in the US (https://www.pcmag.com/picks/the-best-robot-vacuums). Good for a "what about firmware updates" note; don't overstate it.

---

## 0. Camera status of the candidates (what the makers' own pages say)

| Model | Camera? | Obstacle sensing per maker | Source (read 2026-11-23) | Verdict |
|---|---|---|---|---|
| **Roborock Q7 M5 / M5+** | No camera mentioned | "PreciSense LiDAR Navigation … scans 360° and creates detailed maps"; the Q7 series page lists no obstacle sensor at all | https://us.roborock.com/pages/roborock-q7-series [Official]; Vacuum Wars (Christopher White, updated 2026-10-16): "no front obstacle-avoidance sensors", top-mounted LiDAR, no camera, https://vacuumwars.com/roborock-q7-m5-and-m5-review/ | **CONFIRMED camera-free** (LiDAR + bumper only) |
| **Roborock Q10 S5 / S5+ / X5+** | No camera | "Reactive Tech Obstacle Avoidance — Powered by structured light" + PreciSense LiDAR | https://us.roborock.com/pages/roborock-q10-series [Official] | **CONFIRMED camera-free** (LiDAR + structured light) |
| **Tapo RV30 Max Plus** | No camera | "LiDAR + IMU Dual Navigation"; obstacle avoidance listed as LiDAR | https://www.tp-link.com/in/products/details/tapo-rv30-max-plus.html (India spec page; no US spec sheet found) [Official]; The Verge: "there's no AI-powered obstacle detection — so cables and socks will trip it up" | **CONFIRMED camera-free** (LiDAR only). Note a newer "RV30 Max Plus Gen 2" exists (https://www.tapo.com/en/product/robot-vacuum/tapo-rv30-max-plus-gen-2/); not checked |
| **iRobot Roomba 205 DustCompactor (Vac / Combo)** | No camera listed | "ClearView LiDAR sleekly hidden inside the robot quickly maps your home, avoids obstacles and cleans in neat rows, even in the dark" | iRobot Fast Facts PDF: https://filecache.mediaroom.com/mr5mm_irobot/182728/download/2025%20Fast%20Facts%20Sheet_205%20DustCompactor%20Combo.pdf [Official] | **CONFIRMED camera-free** by spec sheet (no camera feature listed; iRobot never says "no camera" in words). CNET: "Only avoided one of six objects" |
| **iRobot Roomba 105 (Vac / Combo / +AutoEmpty)** | No camera listed | Same ClearView LiDAR line in its Fast Facts sheet (turret on top in the photo) | https://media.irobot.com/download/2025+Fast+Facts+Sheet_105+Vac.pdf (via https://media.irobot.com/media-kits?item=44) [Official] | **CONFIRMED camera-free** by spec sheet |
| iRobot Plus 505 / Max 705 | **Camera** (PrecisionVision) | iRobot help: "You cannot disable obstacle detection on Roomba Plus 500 and Max 700 Series" | https://homesupport.irobot.com/articles/en_US/Knowledge/31161 | Camera contrast. Plus 405: camera status UNVERIFIED (Japanese press implies camera only on 505) |
| **eufy Omni C20** | No camera | eufy comparison table: "Obstacle Avoidance: Infrared + Point laser"; page FAQ: "uses infrared to identify obstacles and detect carpets… The laser emits onto surfaces and receives reflected signals" | https://www.eufy.com/products/t2280111 [Official]; RTINGS: static (non-spinning) LiDAR | **CONFIRMED camera-free** |
| **eufy L60** | No camera (LDS + infrared) | — | **DISCONTINUED**: eufy blog "eufy L60 Discontinued: Here're Your Best Alternatives!", updated Nov 11, 2026, https://www.eufy.com/blogs/robovac/eufy-l60-discontinued : "eufy has now discontinued the entire L60 series… New L60 units are no longer planned for restock". eufy names Auto-Empty C10 and Omni C28 ("LDS + laser line obstacle avoidance") as alternatives | **Drop from picks** (or mention as discontinued) |
| eufy E20 (3-in-1) | UNVERIFIED | RTINGS review exists (published 2025-04-24, updated 2026-09-23); sensor type not confirmed from eufy | https://www.rtings.com/robot-vacuum/reviews/eufy/e20 | UNVERIFIED — don't list as camera-free without eufy spec |
| **Ecovacs Deebot T30S** | No camera listed; **has voice assistant (YIKO 2.0, i.e. microphones)** per US launch release | "TrueDetect 3D 3.0, utilizing structured infrared light patterns to deduce three-dimensional object contours and depth"; Obstacle Avoidance: "Structured light" | https://www.ecovacs.com/us/deebot-robotic-vacuum-cleaner/deebot-t30s [Official]; PR Newswire May 16, 2024 https://prnewswire.com/news-releases/ecovacs-unveils-deebot-t30s-combo-with-truedge-and-tangle-free-cleaning-302147157.html | **Camera-free (structured light)**, but mics + Ecovacs security history (section 2) |
| Ecovacs N30 Omni | UNVERIFIED | US page returned 404; Best Buy Canada calls TrueDetect 3D "laser-based" for N30 Pro Omni | — | UNVERIFIED |
| Shark PowerDetect (RV2820 series) | **Conflicting** | SharkNinja page: "With 360 degree LiDAR and a 3D Sensor the robot intelligently detects and avoids objects", but the same page also carries "Sensors, lasers, & an UltraRange Camera map and navigate your home" (likely another model in a comparison block); Homes & Gardens says a front camera is used for mapping | https://www.sharkninja.com/shark-powerdetect-robot-vacuum/RV2820AE.html | **UNVERIFIED — do not list as camera-free** |
| Dreame D10 Plus Gen 2 | No camera | Dreame EU spec: "Navigation LDS / Obstacle Avoidance LDS + Mechanical Barrier Avoidance" | https://ee.dreametech.com/en/products/dreame-d10-plus-gen-2 [Official, EU site] | Camera-free (LiDAR + bumper). US availability not checked |
| Roborock Qrevo Curv / Edge | **Camera** | RTINGS: "similar RGB camera and 3D structured light sensor as Roborock's premium MaxV models" | https://www.rtings.com/robot-vacuum/reviews/roborock/qrevo-curv | Camera contrast; Qrevo S camera status UNVERIFIED |
| Roborock Saros 10R / S8 MaxV, Dreame X50 Ultra, Roomba j7/j9 | **Camera** | Saros 10R: dual-light 3D ToF + RGB camera (StarSight 2.0), ~108 obstacle types (Roborock newsroom https://newsroom.roborock.com/gl/news/roborock-launches-saros-10r-at-ces-2025-ultra-slim-and-highly-intelligent-robotic-vacuum-flagship); j7 = first Roomba with front-facing visible-light camera (IEEE Spectrum https://spectrum.ieee.org/irobot-roomba-j7) | Camera contrasts |

Engineering note for Prof. H (careful wording): a "structured light" or "line laser" module still uses an image sensor to read where the projected infrared pattern lands (triangulation), so "no RGB camera" is the honest claim, not "no image sensor at all". RTINGS describes 3D structured light as "A light source, usually infrared, illuminates the entire area in front of the robot vacuum, and a sensor reads all reflections" (https://www.rtings.com/robot-vacuum/tests/obstacle-avoidance). We found no maker statement on whether those IR frames are stored; say UNVERIFIED rather than "never stored".

---

## 1. How the obstacle sensors work (expert / technical sources)

* **RTINGS, "Our Robot Vacuum Tests – Obstacle Avoidance"** https://www.rtings.com/robot-vacuum/tests/obstacle-avoidance [Independent]. Four types: **bump sensors** ("arguably not avoidance", the robot already hit something); **light-based** (visible or infrared); **3D structured light** (IR floods the area ahead, a sensor reads the reflections, very high resolution); **camera-based** (monocular or binocular). RTINGS separates *detecting* an object from *recognizing* it; recognition usually needs AI on camera or structured-light images. Scoring counts touches, full avoids and interventions on bare floor and carpet, with a bonus for always avoiding pet waste.
* **LiDAR/LDS**: a spinning (or front-mounted) laser rangefinder that maps walls and furniture. It sees in the dark but sees *above* most floor clutter. Vacuum Wars on the Q7 M5: users "must clear cables, socks, and toys first". The Verge on Tapo RV30: "cables and socks will trip it up".
* **Patent background (line laser/structured light)**: projected points or lines of light, an imager, triangulation to tell floor from obstacle; one patent notes a **blind area** near the robot and trouble with thin vertical objects (chair legs) and space under sofas. USPTO 9632505 / 9002511 (iRobot "Methods and systems for obstacle detection using structured light"): https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9632505 [Weak-to-Official; use as background only].
* **Camera + AI**: The Verge (Tuohy): "These models use cameras (worth noting) to see objects in their path and onboard processors to 'decide' how to approach them… robot vacuums with AI detection are less likely to get stuck". CNET (Nov 2026): Roomba Combo 10 Max was "The only vacuum to flawlessly dodge six out of six hazards" in its lab; it uses dual 1080p RGB cameras and AI (per CNET text).
* **What you give up (quotable data)**: CNET lab, Roomba 205 Combo "Only avoided one of six objects". Robot-Review (independent site) on Roborock Q10 S5+: obstacle score 6/24 vs 16.6 average, structured light reliably avoids only objects taller than ~3 inches (https://robot-review.com/reviews/roborock-q10-s5-plus) [Independent, smaller site]. Vacuum Wars Q10 S5 scorecard: obstacle avoidance 1.25 vs 3.39 average (https://vacuumwars.com/roborock-q10-s5-review).

---

## 2. Privacy: what each maker says about camera images (dated) and the camera-off switch

### Roborock — "Trust Center" (Last updated: August 2026) [Vendor/Official]
https://us.roborock.com/pages/roborock-trust-center (same text at https://global.roborock.com/pages/privacy-new)
* "When obstacles are detected, the photo is saved on the robot in an encrypted format rather than as a standard image file."
* "The cloud acts only as a temporary communication channel and does not store the image."
* "Roborock's AI training uses only data from simulated home environment, not real users." / "All AI computations are performed on-device, with no data sent to the cloud or shared with third parties"
* Off switch (FAQ): "You can disable the 'Hello Rocky' built-in voice assistant and AI obstacle recognition related features." "Once turned off, the camera and microphone remain inactive."
* Pet Snap: "Withdrawing permission automatically deletes all photos".
* Maps: page says data collected "includes map data, device status, and anonymized usage information" — it does **not** say maps stay local. Says practices "may vary by product model".
* Exact app menu path for the camera-off toggle on S8 MaxV/Saros: **not found** in an official help page (support.roborock.com returned 403). Say "in the app's settings" without a path.
* Independent counterpoint: none confirmed. (A site called arewescrewed.pages.dev disputes Roborock's claims; anonymous, do not use.)

### iRobot — help articles (undated) [Official]
* "Camera, PrecisionVision, and Obstacle Image Review" https://homesupport.irobot.com/articles/en_US/Knowledge/31161 — turn off in classic iRobot HOME app: Product Settings > Cleaning Settings > Obstacle Detection. **"You cannot disable obstacle detection on Roomba Plus 500 and Max 700 Series."** Images "encrypted"; iRobot "cannot view or access your images unless they are contributed to the image database"; non-contributed images "automatically deleted from our servers after 30 days" (i.e. they *are* on iRobot servers for up to 30 days).
* "What is Obstacle Image Review opt-in?" https://homesupport.irobot.com/articles/en_US/Knowledge/31163 — when on, "your robot will also capture images of the detected obstacle and the surrounding area". Opt out: menu (three lines) > Account > Privacy > Map Features > robot > Obstacle Image Review toggle. Robot still avoids obstacles; you lose the feedback loop.
* **MIT Technology Review, Eileen Guo, Dec 19, 2022**, "A Roomba recorded a woman on the toilet. How did screenshots end up on Facebook?" https://www.technologyreview.com/2022/12/19/1065306/roomba-irobot-robot-vacuums-artificial-intelligence-training-data-privacy/ [Independent]. Images from **development** Roomba J7 units (iRobot: hardware/software changes "not and never were present on iRobot consumer products for purchase"), labeled by Scale AI contract workers in Venezuela who posted them to private groups; iRobot said it shared over 2 million images with Scale AI. Follow-up Jan 10, 2023 (testers felt misled): https://www.technologyreview.com/2023/01/10/1066500/roomba-irobot-robot-vacuum-beta-product-testers-consent-agreement-misled/
* CNET Nov 2026 quotes an iRobot executive: "We use Amazon Cloud Services, and our servers are in the US" (context: iRobot's ownership change; on the CNET best list page). Use only if needed.

### eufy (Anker) [Official]
* "eufy Clean X10 Pro Omni – Discontinuation of the Real Obstacle Photos Feature FAQ" (undated): https://service.eufy.com/article-description/eufy-Clean-X10-Pro-Omni-Discontinuation-of-the-Real-Obstacle-Photos-Feature-FAQ — photo viewing removed by firmware V2.2.40; identification still runs "locally on the robot"; "if the user does not enable the 'User Experience Program' option, the identified photos will not be uploaded to the cloud". (Implication: if you *do* join that program, photos may be uploaded; page doesn't say. Mark as inference.)
* Older AI.See article (NZ mirror) said photos were encrypted, sent to the phone, not stored on servers, with non-obstacle areas and people locally mosaicked; turn off at Settings > AI Recognition > Real Photos — per search snippet only, https://support.nz.eufy.com/support/solutions/articles/154000211062 ; the US page we fetched no longer shows that text. UNVERIFIED for current firmware.
* eufy's "best robot vacuum for privacy" blog = Vendor marketing; skip.

### Dreame [Vendor]
* Older Dreame privacy policy (PDF mirror, 2024): obstacle photos not stored or uploaded, deleted after the object is identified; AI recognition can be toggled off and the robot falls back to basic avoidance. https://cybershack.com.au/wp-content/uploads/2024/05/Dreame-Privacy-Policy.pdf — third-party mirror; UNVERIFIED as current.
* Dreame told CHOICE (Australia) that remote-view footage is not stored unless the user saves it, and saved footage goes to a cloud server: https://www.choice.com.au/data-protection-and-privacy/data-collection-and-use/who-has-your-data/articles/what-your-robot-vacuum-knows-about-you [Independent; article date not read]. Maps: encrypted on device with a copy synced to Dreame Cloud (L10s Ultra data document, Dec 2025, per snippet; UNVERIFIED).

### Ecovacs — the cautionary tale [Independent]
* **DEF CON 32 (Aug 2024), Dennis Giese and Braelynn Luedtke**, "Reverse engineering and hacking Ecovacs robots". TechCrunch, Lorenzo Franceschi-Bicchierai, **Aug 9, 2024**: Bluetooth takeover from about 450 ft (130 m); attackers could switch on cameras and microphones remotely, most newer models have no recording indicator; Wi-Fi credentials and room maps readable; data and auth token survived account deletion (risk for second-hand buyers). Ecovacs initially said users "do not need to worry excessively about this." https://techcrunch.com/2024/08/09/ecovacs-home-robots-can-be-hacked-to-spy-on-their-owners-researchers-say/
* TechCrunch **Aug 22, 2024**: Ecovacs reversed, said it would fix issues in the **Goat G1 and Deebot X1** and the app; security director Martin Ma admitted the company "inadvertently overlooked" the researchers' December 2023 emails. https://techcrunch.com/2024/08/22/ecovacs-says-it-will-fix-bugs-that-can-be-abused-to-spy-on-robot-owners
* **ABC News (Australia), Oct 5, 2024**: Ecovacs' "product improvement program" collects photos, video and voice recordings to train AI; Ecovacs said data is anonymized at the machine level before upload. URL from search result: https://www.abc.net.au/news/2024-10-05/robot-vacuum-deebot-ecovacs-photos-ai/104416632 (not opened; facts via Schneier https://www.schneier.com/blog/archives/2024/10/deebot-robot-vacuums-are-using-photos-and-audio-to-train-their-ai.html).
* Relevance to a no-camera pick: the T30S has no RGB camera but does have microphones for its voice assistant, and the Bluetooth/account issues were about the platform, not only cameras.

### DJI Romo, Feb 2026 (newest example)
* A developer (Sammy Azdoufal) building a PS5-controller app for his own DJI Romo found the server gave him access to roughly 6,700–7,000 Romo units in 24 countries, including live camera feeds, microphone audio and maps; reported patched after DJI was alerted. Tom's Hardware: https://www.tomshardware.com/tech-industry/cyber-security/user-accidentally-gains-control-of-over-6-700-robot-vacuums-while-tinkering-with-their-own-device-to-enable-control-with-a-playstation-controller-security-flaw-reveals-floor-plans-and-live-video-feeds ; PopSci https://popsci.com/technology/robot-vacuum-army . The Verge original not opened (UNVERIFIED). Good one-liner: a server bug turned cameras into strangers' webcams; a camera-free robot only leaks a floor map.

### Ratings by privacy groups
* **Mozilla *Privacy Not Included**: "Eufy RoboVacs" carries the warning label (review dated Nov 9, 2022), https://www.mozillafoundation.org/en/privacynotincluded/eufy-robovacs/ ; Wyze Robot Vacuum carries it (Nov 1, 2023). iRobot Roombas page (Nov 1, 2023) — label status UNVERIFIED (page 403). Nothing found for Roborock or Ecovacs. Mozilla stopped updating the guide (UNVERIFIED; don't claim). Treat all as dated.
* **Consumer Reports**: scores robot vacuums on privacy/security using The Digital Standard; snippet says no robotic vacuum tested scored above a "middling Good" for data privacy, and only iRobot earned Excellent for security (older article "Is Your Robotic Vacuum Sharing Data About You?", https://www.consumerreports.org/robotic-vacuums/is-your-robotic-vacuum-sharing-data-about-you-a1563001307/ — date UNVERIFIED, likely 2020–21). 2026 CR snippet: Roomba Max 705 high for data security, "so-so" for data privacy. Paywalled; paraphrase cautiously.

---

## 3. Expert reviews of the camera-free candidates

### The Verge — Jennifer Pattison Tuohy (VERIFIED byline)
"The best robot vacuums we've tested for 2026", published 2022-03-31, **modified 2026-01-13**, https://www.theverge.com/22997597/best-robot-vacuum-cleaner [Independent]
* **Best budget: Tapo RV30 Max Plus.** "lidar mapping, room-specific cleaning, multiple suction and water levels… and an auto-empty dock"; "did an excellent job of navigating my house"; "I had to tidy up before it ran, as there's no AI-powered obstacle detection — so cables and socks will trip it up."
* Mentions Roborock Q10 S5 Plus ($549.99 list at the time) for "10,000Pa of suction power for a budget bot" and a 2.7-liter self-emptying base.
* Other no-camera notes in the guide: Narwal Freo Z10 "Obstacle avoidance is spotty (no camera)"; SwitchBot K11 Plus "No obstacle avoidance (no camera)". Top picks are camera bots (Matic, Roborock Saros 10).

### PCMag — Andrew Gebhart
* "The Best Robot Vacuums We've Tested (November 2026)", editors' note **Nov 1, 2026**, https://www.pcmag.com/picks/the-best-robot-vacuums [Independent]. **Tapo RV30 Max Plus = "Best Affordable Robot Vacuum", Editors' Choice, 4.0**. **iRobot Roomba 205 DustCompactor Combo = "Best for Compacting Dust", 3.5 Good**: "vacuums well on multiple surfaces and minimizes maintenance by compacting dirt in its dustbin, but its battery life and mopping capabilities fall short"; cons "Short battery life / Got stuck in testing / Poor mopping performance" (205 review first published 2025-06-23). Page says all picks are "unaffected by the FCC's foreign robot vacuum ban".
* "TP-Link Tapo RV30 Max Plus Review", **Dec 19, 2024**, https://www.pcmag.com/reviews/tp-link-tapo-rv30-max-plus — Bottom line: "the best 2-in-1 robot mop and vacuum we've tested for under $300, and it can even empty its own dustbin." Cons: "Struggles with stubborn debris", "Unintuitive Alexa controls". RV30 has a LiDAR periscope on top; RV20 puts LiDAR in the front.
* No PCMag review of the Roborock Q7 M5 found (URL 404).

### CNET — Ajay Kumar (Smart Home & Robotics Editor)
"Best Robot Vacuums We've Tested in 2026", schema date **Nov 13, 2026** (body says updated Oct 8, 2026), https://www.cnet.com/home/kitchen-and-household/best-robot-vacuum/ [Independent]
* **iRobot Roomba 205 DustCompactor Combo = "Best value, best for hardwood (tied)", 7.8.** Best hardwood sand pickup 99.27%; small robot and base; mechanical paddle compacts up to 60 days of debris; cons: no mop settings in app, **"Only avoided one of six objects."** Lab technician named: Schylar Breitenstein.
* Best overall: Roomba Combo 10 Max (camera) — "the only vacuum to flawlessly dodge six out of six hazards".

### RTINGS (dates from page metadata)
* **Roborock Q7 M5** — published 2026-08-03, updated 2026-11-05, https://www.rtings.com/robot-vacuum/reviews/roborock/q7-m5 . Snippets: "the best cheap robot vacuum" RTINGS has tested; "doesn't have a self-emptying dock or real-time obstacle avoidance" (base M5). Body text not readable by our tools; quote only these snippet phrases.
* **eufy Omni C20** — published 2025-01-24, updated 2026-09-23, https://www.rtings.com/robot-vacuum/reviews/eufy/omni-c20 . Snippets: static (non-spinning) LiDAR, slower mapping but fits under low furniture; "does a poor job of maneuvering itself and adapting to obstacles"; tends to get stuck on certain carpeting and tassels.
* **eufy E20** — published 2025-04-24, updated 2026-09-23. Snippet scores: 6.9 multi-surface, 6.5 pets, 8.5 hard-floor debris, 6.2 carpet; good if you don't need mopping.
* RTINGS budget list (snippet, date UNVERIFIED): top budget pick moved to eufy E20; eufy Auto-Empty C10 listed as best cheap. https://www.rtings.com/robot-vacuum/reviews/best/budget
* No RTINGS reviews found for Tapo RV30 Max Plus, Roomba 105/205, Ecovacs T30S (404s).

### Vacuum Wars
* Q7 M5 / M5+ review, Christopher White, updated **Oct 16, 2026** (above): LiDAR, no front obstacle sensors, good value especially on sale, made Vacuum Wars' "Top 5 Budget" list.
* Omni C20 review: "No Obstacle Avoidance" section, LiDAR + IR, no camera or structured light, https://vacuumwars.com/complete-eufy-c20-robot-vacuum-review-the-pros-and-cons/ (date not read).
* Q10 S5 review: structured light, obstacle score 1.25 vs 3.39 avg.

### TechRadar
* Roomba 205 DustCompactor Combo, Derek Adams, **Jul 15, 2025**: "a crushing disappointment"; 78 dB max at 5 ft; dock "refuses to stay put". https://www.techradar.com/home/robot-vacuums/irobot-roomba-205-dustcompactor-combo-review
* Roborock Q7 M5: "the best budget robot vacuum I've tested" (snippet), https://www.techradar.com/home/robot-vacuums/roborock-q7-m5-robot-vacuum-review

### Wirecutter — UNVERIFIED
NYT pages blocked (403) and not indexable by our search. An aggregator claims Wirecutter's Jan 2026 #1 was the Roborock Q7 M5+ — **UNVERIFIED; do not cite**. Byline (Ben Keough or others) **not verified**. Leave Wirecutter out.

### Consumer Reports
A CR model page exists for the Roborock Q7 M5 (https://www.consumerreports.org/appliances/vacuum-cleaners/roborock-q7-m5/m420715/) but the score is paywalled. No CR numbers to quote.

---

## 4. YouTube videos (titles and IDs exactly as in youtube.com search-result URLs, 2026-11-23)

1. **"Roborock Q7 M5 / M5+ Review - A Budget Combo Robot Vacuum"** — ID `vJrQ91fYapU` — https://www.youtube.com/watch?v=vJrQ91fYapU (channel not confirmed)
2. **"ROBOROCK Q7 M5: Best $250 Robovac - In-Depth Review & Tests"** — ID `BoxKAOXbWYc` — https://www.youtube.com/watch?v=BoxKAOXbWYc (channel not confirmed; "$250" is the creator's price, don't repeat as ours)
3. **"*REVIEW* Roomba 205 DustCompactor Vac Robot"** — ID `wRcdDOEKQB8` — https://www.youtube.com/watch?v=wRcdDOEKQB8 (alt: "iRobot ROOMBA 205 Review - GREAT ROBOT VACUUM", ID `tnhuObvIk_I`)
4. **"Reverse engineering and hacking Ecovacs robots - the bad and the really bad"** — ID `O7QCr1ZsxYk` — https://www.youtube.com/watch?v=O7QCr1ZsxYk (title matches the Giese/Luedtke DEF CON 32 talk; uploader not confirmed as the official DEF CON channel)

Avoid for Tapo: several top Tapo RV30 Max Plus results carry #TPLinkPartner (sponsored). Non-sponsored-looking option: "TPlink Tapo RV30 plus max review (Self emptying)" ID `r3-37N1vGPg` (not vetted). "TP-Link Tapo RV30 Max Plus Gen 2 … Consumer Product Test" ID `ZgmbphPb9nw` covers the **Gen 2**, a different model.

---

## 5. Product photos

`ls brand/photos` checked first; no existing file for these models. iRobot Press Center media kits carry the line **"*The materials included on these pages are provided for media use only"** (https://media.irobot.com/, read 2026-11-23) — the same basis as the existing `irobot-roomba-max-705-vac.jpg` entry in `research/photo-manifests/cleaning.json`. Files saved unaltered (server size, no crop/resize).

```json
[
 {
  "product": "iRobot Roomba 205 DustCompactor Vac",
  "status": "ok",
  "file": "brand/photos/irobot-roomba-205-dustcompactor-vac.jpg",
  "kind": "brand",
  "credit": "iRobot press kit",
  "source": "https://media.irobot.com/media-kits?item=48",
  "image_url": "https://media.irobot.com/download/Roomba_205_Vac_Black_Photo_Studio_ChargingDock_RightFacing.jpg",
  "terms": "https://media.irobot.com/",
  "terms_quote": "*The materials included on these pages are provided for media use only",
  "uses": ["web"],
  "checked": "2026-11-23",
  "notes": "Official iRobot Press Center media kit 'Roomba 205 DustCompactor Vac'. 2048x2048 white-background studio shot, black robot with its small charging dock, no people. The Combo kit (item=49) has the same body; its equivalent file is Roomba_205_Combo_Black_Photo_Studio_ChargingDock_RightFacing.jpg (not saved). Media use only; no alterations."
 },
 {
  "product": "iRobot Roomba 105 Vac",
  "status": "ok",
  "file": "brand/photos/irobot-roomba-105-vac.jpg",
  "kind": "brand",
  "credit": "iRobot press kit",
  "source": "https://media.irobot.com/media-kits?item=44",
  "image_url": "https://media.irobot.com/download/Roomba_105_Vac_AutoEmpty_Black_Photo_Studio_Front_Flat.jpg",
  "terms": "https://media.irobot.com/",
  "terms_quote": "*The materials included on these pages are provided for media use only",
  "uses": ["web"],
  "checked": "2026-11-23",
  "notes": "Official iRobot Press Center media kit 'Roomba 105 Vac' (file name says AutoEmpty; image shows the robot alone, no dock). 2048x1149, white background with a graphic spray of dust particles around the robot; LiDAR turret visible. Media use only; no alterations."
 }
]
```

No acceptable press photo found (use name tiles):
* **Roborock Q7 M5 / M5+ and Q10 S5+**: no PR Newswire release or newsroom media for these US models (only a 2022 Q-series US release and a 2025 Australian release for other Q models). Matches the existing manifest note for Q7 M5+.
* **Tapo RV30 Max Plus**: TP-Link US press release Nov 14, 2024 (https://www.tp-link.com/us/press/news/21467/) has **no images**; a Business Wire copy exists (https://www.businesswire.com/news/home/20241114792236/en/…) but returned 403, so whether it carries a photo and terms is UNVERIFIED. Worth a manual browser check.
* **eufy Omni C20**: only Anker Japan's PR TIMES release (Feb 26, 2025); PR TIMES terms restrict for-profit use (same problem as the held eufy Omni S2 entry). Not downloaded.
* **Ecovacs T30S**: US PR Newswire release (May 16, 2024) carries only the Ecovacs logo.
* **Dreame D10 Plus Gen 2**: none (matches existing manifest).
* **Shark PowerDetect**: none (matches existing manifest).

---

## 6. "Before you buy: settings and privacy" — official how-to pages

No-go zones / virtual walls
* **Roborock**: Edit Map > No-Go Zone / Invisible Wall; up to 10 of each (Roborock app listing). Official tutorials are for older models: https://support.roborock.com/hc/en-us/articles/360036401271-Roborock-S6-No-Go-Zones-and-Virtual-Walls-Tutorial (map saving must be on). Roborock S5 manual note: zones should not be relied on to fence off hazards.
* **iRobot**: Smart Map > Zones > Keep Out Zone; app may suggest a zone where the robot gets stuck. https://homesupport.irobot.com/articles/en_US/Knowledge/64102 (and /21094). 205 Fast Facts confirms "create keep-out zones".
* **Tapo**: Map icon > Edit Map > "Virtual Wall/No-Go Zones" > Save; zones can't cross or sit too close to the dock. https://www.tapo.com/us/faq/287/
* **eufy**: Map Edit > No-Go Zone / Virtual Boundary / No-Mop Zone; needs a saved map; up to 10 each (X8/LR series article). eufy warns zones can be disabled by "map invalidation caused by environmental changes" and suggests physical magnetic strips near fireplaces. https://service.eufy.com/article-description/The-Differences-Between-Virtual-Boundary-No-Go-Zone-and-No-Mop-Zone and https://service.eufy.com/article-description/How-to-set-up-the-No-go-Zone-Virtual-Boundary-for-X8-X8-Hybrid

Camera-off / image settings (for readers who already own a camera bot)
* iRobot: Obstacle Detection toggle (not on Plus 500 / Max 700) and Obstacle Image Review opt-out, links in section 2.
* Roborock: disable AI obstacle recognition in the app; Roborock says camera then stays inactive (Trust Center, Aug 2026).
* eufy: real-photo feature removed by firmware V2.2.40; leave "User Experience Program" off.
* Ecovacs: don't join the "product improvement program" (ABC, Oct 2024).

Maps and local control
* Roborock Trust Center lists "map data" among data collected; no maker in this set offers an official fully local mode for the models above (none found).
* **Valetudo** (open-source project, GitHub "Hypfer/Valetudo"; author's name not checked): replaces the vendor cloud on supported, rooted Dreame/Roborock robots; "It is not a custom firmware". https://valetudo.cloud/ and https://github.com/Hypfer/Valetudo . Rooting voids warranties and the supported list is mostly older models; mention as an enthusiast option only. Giese's role in rooting tools not verified in this pass.
* Second-hand warning (DEF CON 2024): on Ecovacs, data and auth tokens survived account deletion. Generic advice: remove the robot from your account and factory-reset before selling.

Prof H Lab links required by the queue entry: https://profhlab.com/robot-vacuum-repair-costs/ and https://profhlab.com/robot-vacuum-consumables/ (not checked here).
