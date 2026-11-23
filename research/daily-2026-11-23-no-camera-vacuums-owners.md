# Owners brief: Robot Vacuums Without a Camera 2026 (LiDAR models that don't film your home, and what you give up)

Research agent 1 (Owners), compiled 2026-11-23 for the Nov 23 roundup. About 52 web searches and 15 page fetches, plus one PDF text pull (iRobot's 205 fact sheet).

**Rules followed.** No Amazon customer reviews, ratings, Q&A or review digests were used. Search summaries that quoted Amazon averages or counts (AOL's Tapo figure, ShopSavvy's eufy C20 figure, Fakespot) were dropped. **Do not publish any Amazon number.**

**Access limits.**
* reddit.com refuses fetches, and the reddit.sentinel-team.org mirror now shows only threat summaries, no post titles. **No Reddit thread could be read directly.** Where Reddit is mentioned below, it comes through a third party and is tagged [Weak].
* Best Buy returned 503 on direct fetches. Best Buy, Sam's Club and Target figures below come from **search-result snippets** of the retailers' own review pages, seen 2026-11-23. Cached copies differ, so give ranges or say "about".
* RTINGS pages load without their test text (paywall/JS), so RTINGS findings are from search snippets.
* Maker pages (ecovacs.com/us, tp-link.com/us, us.roborock.com, service.eufy.com, homesupport.irobot.com) and the TP-Link community forum loaded fine, and their dates are exact.

**Tags:** [Official] maker or government page · [Retailer snippet] · [Forum] brand forum with exact date · [Independent] trade press or test lab · [Weak] aggregator, complaint site or third-hand Reddit · [Inference] · **UNVERIFIED**.

---

## 0. The sensor question first: what "no camera" means

* **LiDAR (LDS)** spins a laser and measures distance. It builds the map. It cannot take a picture. Every pick below has one.
* **Structured light / line laser** (Roborock "Reactive Tech", Ecovacs "TrueDetect 3D", eufy "point laser"/"triple-line laser") projects an infrared pattern and reads how it bends. Ecovacs's German T30S COMBO manual says its TrueDetect 3D sensor scans with a line laser and "collects images with a monocular camera" [Official, manual via https://www.manualslib.de/manual/1281081/Ecovacs-Deebot-T30S-Combo.html?page=14]. That is an infrared sensor reading a laser line, not an RGB camera that can send a photo of your living room, and Ecovacs's US T30S page lists no camera or video feature [Official, https://www.ecovacs.com/us/deebot-robotic-vacuum-cleaner/deebot-t30s, fetched 2026-11-23]. **The post should say this honestly**: "no RGB/AI camera" is the accurate claim for structured-light models, not "no image sensor of any kind". The pure-LiDAR picks (Tapo, Roborock Q7 M5, Roomba 105/205) have neither.
* **What the camera buys you**: object *recognition* (it knows a cord from a sock from dog poop). LiDAR-only robots mostly bump; structured-light robots see "something is there" but not what. A 2026 privacy guide puts it as: finding a flagship without any camera is getting hard, because obstacle avoidance increasingly depends on visual recognition [Weak, summarised in search, https://robovacguide.com/lidar-vs-camera-robot-vacuum/].
* **LiDAR is not a zero-risk sensor either**: the 2020 "LidarPhone" paper (ACM SenSys, Nov 2020; Sami, Dai, Tan, Roy, Han; NUS and University of Maryland) turned a hacked Xiaomi Roborock's LiDAR into a laser microphone and identified spoken digits with about 90% accuracy, but the attacker must already control the robot and the model must be trained on the target's voice [Independent, https://www.cs.umd.edu/~nirupam/images/2_publication/papers/LidarPhone_SenSys20_nirupam.pdf; https://www.securityweek.com/new-lidarphone-attack-uses-robot-vacuum-cleaners-eavesdropping]. Mozilla's Privacy Not Included still calls LiDAR the safer bet than cameras [Independent, https://www.mozillafoundation.org/en/privacynotincluded/wyze-robot-vacuum/].
* **A camera-free robot still makes a floor plan and talks to a cloud.** The map is data too (see section 9).

---

## 1. Confirmed camera-free list (Nov 2026, US)

| # | Model | Tier | Mapping | Obstacle sensing | Camera? | Evidence |
|---|---|---|---|---|---|---|
| 1 | **TP-Link Tapo RV30 Max Plus** | Budget, auto-empty | LiDAR + IMU | LiDAR only; top "anti-stuck" sensor; 22 mm climb | None mentioned | [Official] https://www.tp-link.com/us/smart-home/robot-vacuum/tapo-rv30-max-plus/ (fetched 2026-11-23) |
| 2 | **Roborock Q7 M5 / Q7 M5+** | Budget | PreciSense LiDAR | **No dedicated avoidance** (bumper + LiDAR) | None mentioned | [Official] https://us.roborock.com/pages/roborock-q7-series; RTINGS: no real-time obstacle avoidance [Independent, https://www.rtings.com/robot-vacuum/reviews/roborock/q7-m5]. **Note:** the US product URL us.roborock.com/products/roborock-q7-m5 returned 404 on 2026-11-23; the series page still lists M5/M5+ with "availability alerts". US stock UNVERIFIED, channels agent should check. |
| 3 | **Roborock Q10 S5+** | Budget–mid, auto-empty | PreciSense LiDAR | "Reactive Tech" structured light | None mentioned | [Official] https://us.roborock.com/products/roborock-q10-s5-plus (fetched 2026-11-23, 1-year warranty); Q10 S5 page says "Powered by structured light technology" [Official, https://us.roborock.com/products/roborock-q10-s5] |
| 4 | **iRobot Roomba 105 / 205 DustCompactor (Combo)** | Budget–mid | ClearView LiDAR (in-body) | LiDAR only | **No front-facing camera** per iRobot | iRobot support lists camera models as Max 875, Max 705, Plus 678/615/575/505, 10 Max and j5–j9, and says "All other models not listed do NOT have a front-facing camera" [Official, https://homesupport.irobot.com/articles/en_US/Knowledge/31161, fetched 2026-11-23]. 205 fact sheet: "ClearView LiDAR … avoids obstacles", no camera listed, $469 [Official, PDF https://filecache.mediaroom.com/mr5mm_irobot/182728/download/2025%20Fast%20Facts%20Sheet_205%20DustCompactor%20Combo.pdf]. **Conflict:** TechRadar's review text (via snippet) mentions "the camera" next to the LiDAR slot, and one Best Buy owner calls the front "mapping camera and Lidar". Treat as UNVERIFIED; the maker's list is the authority, but the video/experts agent should check the 205 manual. |
| 5 | **eufy Omni C20** | Mid, full mop dock | LDS | "Built-in point laser"; eufy says this makes it rotate and reposition often | None mentioned | [Official] https://service.eufy.com/article-description/Tips-on-Using-the-Omni-C20 (fetched 2026-11-23) |
| 6 | **Ecovacs Deebot N30 Omni / T30S** | Mid | LDS, TrueMapping 2.0 | TrueDetect 3D 3.0: N30 Omni spec says "Laser Obstacle Avoidance"; T30S spec says "Structured light" | None on US pages (IR sensor caveat in section 0) | [Official] https://www.ecovacs.com/us/shop/deebot-robotic-vacuum-cleaner/deebot-n30-omni-care (marked "Sold out", $699.98, 2026-11-23); https://www.ecovacs.com/us/deebot-robotic-vacuum-cleaner/deebot-t30s. **Trap:** T30S **Pro** and T30S **AI** variants differ; Ecovacs's French blog calls the T30S PRO a camera robot with video manager. Link the plain T30S only. |
| 7 | **Roborock Qrevo S** | Mid–premium, full dock | LiDAR | Reactive Tech structured light | No (Master/MaxV siblings add a camera) | [Independent] https://vacuumwars.com/roborock-qrevo-s-review; https://basic-tutorials.com/reviews/gadget-reviews/roborock-qrevo-s-pro/; [Official] https://global.roborock.com/pages/roborock-qrevo-s. US stock UNVERIFIED. |
| 8 | **Shark PowerDetect NeverTouch Pro (RV2820 family)** | Mid–premium | 360° LiDAR | LiDAR + "3D sensor" + front lasers | None mentioned; only the **UV Reveal RV3020XE** lists an "UltraRange Camera" | [Official] https://www.sharkninja.com/shark-powerdetect-robot-vacuum/RV2820AE.html; [Official] Shark RV3020XE copy via search. What the "3D sensor" is (ToF vs structured light) is UNVERIFIED. |

### Dropped or flagged
* **eufy E20**: US page says "Triple-Line Laser Obstacle Avoidance", but some regional eufy spec tables list "Active Binocular Infrared Camera + RGB camera" and the UK page "RGB Camera + LED" [Official, conflicting, https://eufy.com/products/t2070111; https://eufy.com/uk/products/t2070G11]. Do not call it camera-free.
* **eufy L60**: infrared avoidance, no camera, but eufy has discontinued the L60 series [Weak, search summary of eufy pages]. Skip.
* **Dreame D20 Plus**: LDS + bumper, no structured light (the D20 Pro Plus adds 3D structured light) [Official, Dreame blog via search]. US availability and "no camera" not stated by Dreame. UNVERIFIED; skip unless the channels agent finds a US listing.
* **Roborock Q5 Max+**: LiDAR, no avoidance at all; RTINGS says it fails to avoid anything smaller than a shoe and tangles in cords [Independent, https://www.rtings.com/robot-vacuum/reviews/roborock/q5-max-plus]. Older; Q7 M5 covers the slot.
* **Roomba Plus 505 / Max 705, T30S Pro, Qrevo Master/MaxV, Shark UV Reveal**: camera models. Contrast only.
* **Shark Matrix Plus**: 360° LiDAR, no camera found; RTINGS calls its avoidance "primitive" and unable to detect small objects [Independent, https://www.rtings.com/robot-vacuum/reviews/shark/matrix-plus-ur2360s]. Older; optional.

---

## 2. Tapo RV30 Max Plus (LiDAR only)

### Ratings at non-Amazon stores
* Best Buy US: no rating found in search (Best Buy Canada lists it, no score in snippet). UNVERIFIED.
* Tom's Guide calls it one of the best cheap robots it has tested; TechGearLab lists "disappointing obstacle avoidance" and "struggles with hair" and says shedding homes should look elsewhere [Independent, https://www.tomsguide.com/home/tp-link-tapo-rv30-max-plus-review; https://www.techgearlab.com/reviews/smart-home/robot-vacuum/tp-link-tapo-rv30-max-plus].

### Complaints and what fails first (TP-Link community forum)
1. **Dark carpet reads as a cliff.** Owner thread "Do not buy the TP-Link Tapo RV30 Max Plus if you have carpets" (2026-06-22, firmware 1.3.3 Build 260206): a black-and-red rug triggers "high surface"/"cliff sensor blocked" errors and strands the robot; marking it as carpet did not help; owner asked for a cliff-sensor off switch. TP-Link staff (2026-06-26) said it "isn't a common problem", a known fix exists, and took the case private. A second owner reported the same on 2026-07-07 [Forum, https://community.tp-link.com/en/home/forum/topic/867066]. *This is a cliff-sensor problem shared by most budget robots, not a LiDAR one; worth one line for owners of dark rugs.*
2. **Docking and phantom errors.** Owner (bought late Nov 2024, post 2024-12-28, firmware 1.1.9): stops about a metre short of the dock with "Can not find the docking station" until remapped; false "wheel stuck" and "main brush stuck" errors with no blockage. Moderator asked for 0.5 m side and 1.5 m front clearance and escalated by email [Forum, https://community.tp-link.com/en/home/forum/topic/731804].
3. **Battery range.** Thread title: "RV30 Max Plus battery is miserable – only lasts ~750 sq-ft" [Forum, https://community.tp-link.com/us/smart-home/forum/topic/830470; title only seen]. Another: shuts down mid-clean at about 23–25% instead of returning [Forum, https://community.tp-link.com/en/home/forum/topic/851384; via search snippet].
4. **App connection.** "RV30 Max Plus Can't connect to App" [Forum, https://community.tp-link.com/en/home/forum/topic/827806; title only].

---

## 3. Roborock Q7 M5 / M5+ (LiDAR only, no avoidance sensor)

* **What testers say about obstacles:** RTINGS lists "frequently getting stuck on rugs, cords, and clutter" and says neither it nor close rivals reliably avoid cords, socks or pet waste [Independent, https://www.rtings.com/robot-vacuum/reviews/roborock/q7-m5]. T3/Independent: "object avoidance is hit and miss … often ploughed right into things left on the floor like books or socks", but it rarely got lost thanks to LiDAR [Independent, https://www.t3.com/home-living/vacuum-cleaners/roborock-q7-m5]. TechGearLab: pre-clear socks and cords [Independent, https://www.techgearlab.com/reviews/smart-home/robot-vacuum/roborock-q7-m5-plus].
* **Owner reviews:** none found at Walmart/Target/Sam's for the exact M5/M5+ (Walmart's Q7 page is the Q7 L5, a different model). A Best Buy page (SKU 6508377) that surfaced is not confirmed as the Q7 M5. UNVERIFIED; do not use.
* **Praise in tests:** mapping accuracy, suspension over thresholds [Independent, TechRadar https://www.techradar.com/home/robot-vacuums/roborock-q7-m5-robot-vacuum-review].
* **Verdict line for post [Inference]:** the purest "no camera, no image sensor" pick, and the one that demands a tidy floor.

---

## 4. Roborock Q10 S5+ (LiDAR + structured light)

* **Retailer snippets:** Sam's Club review page exists with mixed reviews; one 2-star owner says their older Q5 Pro "had much less technical flaws" than the new Q10 S5+ [Retailer snippet, https://www.samsclub.com/reviews/product/20293424436, seen 2026-11-23].
* **Navigation is the main complaint:** Tom's Guide headline: "it cleans well but has zero sense of direction"; lists poor navigation, poor battery life, loud emptying, fiddly mop [Independent, https://tomsguide.com/home/roborock-q10-s5-review]. Robot-Review gave its obstacle avoidance 6 of 24 points and lists LiDAR sensor failures, cliff-sensor faults and Wi-Fi issues among reported problems [Weak, https://robot-review.com/reviews/roborock-q10-s5-plus].
* **Hair: a strength.** Vacuum Wars: 0% tangling in its 7-inch hair test vs a 38% average; GearLab: brush stays mostly hair-free [Independent, https://vacuumwars.com/roborock-q10-s5-review; GearLab].
* **Maker store seen 2026-11-23:** $229.99 against $549.99 list, page shows both "Out of stock, coming soon!" and "Add to Cart" [Official, us.roborock.com]. (Maker price, not Amazon; channels agent to confirm.)

---

## 5. iRobot Roomba 105 / 205 DustCompactor (LiDAR only)

### Ratings (snippets, seen 2026-11-23)
| Store | Model | Rating | Count | Note |
|---|---|---|---|---|
| Best Buy (SKU 6618889 / 10735578) | 205 DustCompactor | about 4.1–4.2 / 5 | about 77–90 | 86% would recommend; pros "mapping, navigation, suction" [Retailer snippet, https://www.bestbuy.com/site/reviews/irobot-roomba-205-dustcompactor-vacuum-compacts-dirt-inside-no-emptying-for-60-days-bagless-intense-suction-black/6618889?page=3] |
| Best Buy | 105 / 105 Combo | not captured | | owner themes below |

### Complaints
1. **Rugs and rug edges.** Several Best Buy 105 owners: "gotten stuck a few times, mainly on rugs", "stuck constantly on the rug edges", "finds ways to get itself stuck in the most peculiar places" [Retailer snippets, https://www.bestbuy.com/site/reviews/irobot-roomba-105-vacuum-easy-to-use-intense-power-lifting-suction-lidar-navigation-multi-surface-cleaning-self-charging-black/6618891?page=2 and ?page=4]. Counter-view: one owner in a small furnished space says it has not got stuck yet.
2. **Obstacle avoidance only sees furniture.** A 205 Best Buy owner: "obstacle avoidance" is practically limited to seeing furniture [Retailer snippet, https://www.bestbuy.com/site/reviews/irobot-roomba-205-dustcompactor-vacuum-auto-compacts-debris-within-robot-no-emptying-for-60-days-bagless-intense-suction-black/10202358?page=2]. VacuumWars: no listed obstacle avoidance on the 205 series [Independent, https://vacuumwars.com/irobots-new-2025-lineup-buyers-guide].
3. **Second app.** The 2025 line uses the new **Roomba Home** app (100/200/400/500/700/Mini series sold after March 2025), not iRobot Home (Classic) [Official, App Store listing https://apps.apple.com/us/app/-/id6504274697]. Owners with older Roombas complain about running two apps; some say the new one "never connected" or needed restarts; others found setup "very easy" [Retailer snippets, Best Buy 105 pages].
4. **Reliability and support, 2026.** A 205 bought April 2026: stopped working randomly, wrong battery level on dock; another (7 May 2026, 1 star): "no one day … without encountering issues"; long, scripted phone support [Weak, Trustpilot, https://uk.trustpilot.com/review/irobot.co.uk?page=3]. Spain's OCU lists a public complaint (April 2026) about a **second** defective Roomba 205 DustCompactor Combo [Weak, https://www.ocu.org/reclamar/lista-reclamaciones-publicas/solicitud-de-sustituci-C3-B3n-por-m/5dcbd74b15c711a115]. Self-selected; no pattern count possible.
5. **Expert verdict:** TechRadar's 205 review headline: "a crushing disappointment"; LiDAR is better than old V-SLAM Roombas but "erratic and unsophisticated" next to other LiDAR robots [Independent, https://www.techradar.com/home/robot-vacuums/irobot-roomba-205-dustcompactor-combo-review].

### iRobot ownership status (Chapter 11 and Picea)
* iRobot announced the Picea deal on **2025-12-14** (secured lender and contract maker Picea to acquire it through a court-supervised Chapter 11) [Official, https://media.irobot.com/2025-12-14-iRobot-Announces-Strategic-Transaction-to-Drive-Long-Term-Growth-Plan].
* Deal **closed 2026-01-23**: Picea owns 100% of the equity [Official, https://media.irobot.com/2026-01-23-iRobot-Completes-Court-Supervised-Transaction-with-Picea,-Enabling-the-Next-Chapter-of-Growth]. US and EU consumer data moved to an independent US subsidiary, **iRobot Safe**, with a board of US citizens; HQ stays in Bedford, MA [Independent, https://www.automate.org/robotics/industry-insights/acquisition-completed-irobot-outlines-plans-for-us-eu-consumer-data-protections; https://www.therobotreport.com/irobot-emerges-from-chapter-11-picea-u-s-subsidiary/].
* Pre-closing promise: no anticipated disruption to app functionality, customer programs or product support; TechRadar reported the CEO calling it "business as usual" with no warranty impact [Independent, https://techradar.com/home/robot-vacuums/the-irobot-takeover-is-complete-but-it-looks-like-the-roomba-brand-is-clinging-on-to-its-us-roots]. **No post-closing warranty policy change found; no 2026 app outage found.** UNVERIFIED beyond that.
* Why owners worry: Neato's parent ended Neato cloud services early, in October 2025 [Weak, https://apple.gadgethacks.com/news/neato-cloud-shutdown-irobot-crisis-rock-smart-home]. iRobot says a Roomba works without the app, but scheduling/maps need it [Official, iRobot app page]. One Trustpilot user claims 900-series cloud features ended without notice [Weak, single claim, UNVERIFIED].
* **For the post [Inference]:** a Roomba 105/205 is now a Picea-owned product with US-governed data; buy from a store with a long return window and register the warranty.

---

## 6. eufy Omni C20 (LDS + point laser)

* **Retailer ratings:** none found at Best Buy, Walmart or Costco in search. UNVERIFIED.
* **The spin:** eufy itself says the point laser makes it "rotate and position itself frequently", and tells owners to clear wires, small toys and socks and tie up curtains [Official, https://service.eufy.com/article-description/Tips-on-Using-the-Omni-C20]. A eufy community post attributes the spinning to a front-facing LiDAR [Forum, https://community.eufy.com/t/another-day-in/5229710, via snippet].
* **Testers:** RTINGS: avoidance sensors "work fairly well" but it "does a poor job" adapting to obstacles and "tends to get stuck on certain carpeting and tassels"; poor mopping because there is no onboard water tank (the dock pre-wets pads) [Independent, https://rtings.com/robot-vacuum/reviews/eufy/omni-c20].
* **What fails first (from the error articles eufy had to write):** mop-pad holder stuck / "cleaning mop has been interrupted" (sweeps only); mop pads not spinning (hair round the bracket, possible motor fault); dirty-water tray level error (lid seal air leak); "can't find the station"; "laser sensor may be blocked or laser sensor error, please contact customer service" [Official, https://service.eufy.com/article-description/Voice-Alerts-Quick-Solutions-for-the-Omni-C20 and linked articles]. eufy runs a self-service repair application that covers the C20 for several mop alerts [Official, https://service.eufy.com/au/article-description/eufy-Repair-Application-Instructions]. *Existence of a support article is not a failure rate; say "eufy's own help pages cover…".*
* **Owner threads on community.eufy.com specifically for the C20 were not found.** UNVERIFIED.

---

## 7. Ecovacs Deebot N30 Omni / T30S (LDS + TrueDetect 3D)

* **Ratings (snippet, seen 2026-11-23):** Best Buy N30 **Pro** Omni (SKU 6599628): 4.1 / 5 from about 83 reviews; praise for mopping ("far superior to an iRobot"), mapping, low noise; complaints: small dustbin; one March 2025 buyer coming from an N8 found it disappointing and hoped for a warranty swap [Retailer snippet, https://www.bestbuy.com/site/reviews/ecovacs-robotics-n30-pro-omni-robot-vacuum-spinning-mop-with-auto-cleaning-station-black/6599628?page=2]. Walmart lists the N30 Omni (item 15510003334) with no rating captured.
* **Hair at the brush ends:** The Gadgeteer's N30 Omni review (2024-11-22): main brush handles tangles well but hair still winds round the axle ends and needs regular removal [Independent, https://the-gadgeteer.com/2024/11/22/ecovacs-deebot-n30-omni-robot-vacuum-and-mop-review-the-edge-of-cleaning].
* **Ecovacs's own FAQ** "Why is the TrueDetect 3D Smart Detection System sometimes unable to avoid obstacles?" exists, and a separate FAQ explains how to switch TrueDetect off [Official, https://help.ecovacs.com/us/support/faq-detail?id=185]. Contents not fetched; UNVERIFIED.
* **Stock:** N30 Omni Care "Sold out" on ecovacs.com/us 2026-11-23 [Official]. Channels agent to confirm which N30/T30S variant is actually buyable.
* **Brand privacy history matters here** (section 9): Ecovacs had the DEF CON 2024 findings and the October 2024 hijackings, though those were camera/mic models (Deebot X2). Say so plainly.

---

## 8. Roborock Qrevo S and Shark PowerDetect

### Qrevo S (LiDAR + structured light)
* **Sam's Club:** 4.7 / 5 from about 140 ratings, 84% five-star [Retailer snippet, https://www.samsclub.com/reviews/product/20711067396, seen 2026-11-23]. Text not seen.
* **The cost of no camera, from testers:** RTINGS: the front structured-light sensor is "almost useless in practice", so it can run over pet waste [Independent, https://www.rtings.com/vacuum/reviews/roborock/qrevo-s]. Vacuum Wars: structured light only means "poor obstacle avoidance" vs the camera-equipped Master/MaxV [Independent]. Basic-tutorials (Qrevo S Pro): "satisfactory" in everyday use [Independent]. RTINGS also flags high recurring parts costs.

### Shark PowerDetect NeverTouch Pro (LiDAR + 3D sensor)
* **Ratings (snippets):** Best Buy (SKU 6599392) about 4.2 / 5; Sam's Club about 3.9 / 5 [Retailer snippets, https://bestbuy.com/site/reviews/shark-robot-vacuum-mop-powerdetect-nevertouch-pro-combo-self-emptying-self-refilling-with-self-clean-pad-wash-dry-black/6599392; https://www.samsclub.com/reviews/product/15219458937, seen 2026-11-23].
* **Complaints:** Sam's owner: "gets stuck a LOT"; Best Buy owners: mop stopped working and it "would go in circles randomly"; dustbin sticking; mopping "holds it back". One owner said no-go zones fixed the sticking; Shark replies suggest stable 2.4 GHz, app updates, factory reset and remap [Retailer snippets].
* **Testers:** RTINGS (retested July 2025): poor with socks and loose cables; praises the lift system that climbs obstacles [Independent, https://www.rtings.com/robot-vacuum/reviews/shark/powerdetect-rv2820ze]. Vacuum Wars: the 3D sensor and front lasers worked "about half the time" [Independent]. TechRadar: "impressive", but over-sensitive [Independent].
* **Dock clogs:** no robot-specific clog complaint pattern found (the clog replies found were for the PowerDetect stick vac). UNVERIFIED.

---

## 9. Privacy-motivated owners: incidents with dates

| Date | Incident | Camera model? | Source |
|---|---|---|---|
| **2022-12-19** | MIT Technology Review: 15 images (incl. a woman on the toilet, a child) captured in 2020 by **development** Roomba J7 units, sent to Scale AI for labelling, posted by Venezuela-based gig workers to private Facebook/Discord groups. iRobot said the testers had signed consent; it had shared over 2 million images with Scale AI, one of several annotators; iRobot blamed Scale AI, which blamed the workers. These were not retail units. | Yes (J7 dev) | https://www.technologyreview.com/2022/12/19/1065306/roomba-irobot-robot-vacuums-artificial-intelligence-training-data-privacy/; https://petapixel.com/2022/12/21/robot-vacuum-took-photo-of-woman-on-toilet-that |
| **2024-08-10** | DEF CON 32: Dennis Giese and Braelynn Luedtke show 11 Ecovacs devices could be taken over over Bluetooth from about 130 m, cameras and mics switched on with no indicator; data/tokens survived account deletion. Ecovacs first downplayed, then (2024-08-22) said it would fix them. | Yes | https://techcrunch.com/2024/08/09/ecovacs-home-robots-can-be-hacked-to-spy-on-their-owners-researchers-say/; https://techcrunch.com/2024/08/22/ecovacs-says-it-will-fix-bugs-that-can-be-abused-to-spy-on-robot-owners |
| **Oct 2024** (incidents May 2024) | ABC (Australia) reports hijacked **Deebot X2** units in several US cities: a Minnesota owner heard slurs through the speaker; one in LA chased a dog (May 24); one in El Paso shouted slurs (five days later). Ecovacs: "found no evidence" of a breach of its systems, told users to change passwords, promised an X2 security upgrade in November. ABC: unclear how many were hit. | Yes (camera + mic) | https://www.tomsguide.com/home/smart-home/hacked-ecovacs-vacuums-went-haywire-across-the-us; https://www.engadget.com/cybersecurity/hackers-are-making-robot-vacuums-randomly-yell-racial-slurs-184017187.html |
| **2025-09** (published ~2025-09-02) | Korea's KISA and Korea Consumer Agency test six models: **Dreame X50 Ultra** camera could be activated remotely; Narwal Freo Z Ultra and Ecovacs Deebot X8 Pro Omni had weak app authentication exposing cleaning photos; Samsung and LG best. Fixes reported since. | Yes | https://www.koreajoongangdaily.com/business/security-flaws-found-in-ecovacs-dreame-robot-vacuums/12223836; https://www.asiae.co.kr/en/article/2025090208480104825 |
| **~2025-11** | iLife A11: an engineer (Harishankar) blocked its telemetry and says a remote "kill" command bricked it; he revived it offline. One person's account, no maker statement. | No camera; LiDAR budget bot | https://www.tomshardware.com/tech-industry/big-tech/manufacturer-issues-remote-kill-command-to-nuke-smart-vacuum-after-engineer-blocks-it-from-collecting-data-user-revives-it-with-custom-hardware-and-python-scripts-to-run-offline |
| **Feb 2026** (patched ~Feb 8–11) | **DJI Romo**: hobbyist Sammy Azdoufal, building a PS5-controller app, found DJI's MQTT broker let him reach about 7,000 Romo units in 24 countries, including live camera feeds, mic audio and floor plans. DJI patched; Romo later disappeared from DJI's online store (reported Feb 26); DJI launched a bug bounty (Mar 2026). | Yes | https://www.malwarebytes.com/blog/news/2026/02/hobby-coder-accidentally-creates-vacuum-robot-army; https://dronexl.co/2026/02/17/dji-romo-security-breach/; https://www.semafor.com/article/02/23/2026/robot-vacuum-hack-reveals-live-video-from-7000-customers; https://dronedj.com/2026/03/10/dji-romo-security-bug-bounty/ |

**Takeaways for the post [Inference]:** every incident that exposed *images* involved a camera robot. The iLife case shows a camera-free robot can still phone home. The map, Wi-Fi details and microphone (if any) remain exposure points.

### What privacy-minded owners actually do
* An r/privacy thread (2024-07-11) "'Safe' robot vacuum? Is that possible nowadays?" [Weak, mirror https://red.bismuth.it/r/privacy/comments/1e0cct3/safe_robot_vacuum_is_that_possible_nowadays/lcosmhn/?context=3; not read]. A Cool Down write-up of another Reddit thread says commenters told a poster that local-only control "usually takes extra work" [Weak, https://www.thecooldown.com/?p=799700].
* **Valetudo** (cloud-free firmware): runs only on the robots on its official supported list (Dreame, Roborock, Xiaomi, MOVA, Viomi rebrands), rooted using Dennis Giese's methods; exposes a local web UI, REST API and MQTT with Home Assistant autodiscovery; rooting cuts off the vendor cloud [Official project, https://valetudo.cloud/pages/general/supported-robots.html; https://valetudo.cloud/pages/general/why-valetudo.html]. A secondary guide counts 49 models [Weak, https://www.privacysmarthome.com/guides/valetudo-supported-robot-vacuums-list-2026/]. **None of our eight picks is confirmed as supported.** Check the list before saying anything. Warn that rooting can void the warranty.
* Home Assistant forum: the official Roborock integration commands locally but needs the cloud for setup and fallback [Forum, community.home-assistant.io, via snippet].
* Maker controls: iRobot camera models encrypt obstacle images, delete them after 30 days unless contributed, and let you switch Obstacle Image Review off [Official, https://homesupport.irobot.com/articles/en_US/Knowledge/31161]. Roborock's trust centre says its video feature is off by default and needs a physical button press (updated Jan 2026) [Official, https://us.roborock.com/pages/roborock-trust-center, via snippet].

---

## 10. What a camera-free robot does badly (vs camera models): complaint patterns

Counts are from the sources in this brief (each model counted once per pattern if a tester or owner reported it). Small, self-selected sample; present as "in our reading", not statistics.

| Pattern | Camera-free models where reported | Count (of 8) | Typical source |
|---|---|---|---|
| Hits or drags **cords/cables** | Q7 M5, Q10 S5+, Roomba 105/205 (furniture-only avoidance), Omni C20 (eufy says clear wires), Shark PowerDetect, Tapo RV30 (GearLab), Qrevo S | 7 | RTINGS, GearLab, maker tips, Best Buy |
| **Socks/small items** eaten or pushed | Q7 M5, Omni C20, Shark PowerDetect, Q10 S5+ | 4 | T3, eufy, RTINGS |
| **Pet waste** not avoided (tester says it can run over it) | Q7 M5, Qrevo S, (Q5 Max+ dropped) | 2 explicit; assume all LiDAR-only | RTINGS |
| **Stuck on rugs/tassels/rug edges** | Roomba 105, Omni C20, Q7 M5, Tapo RV30 (dark rug = cliff) | 4 | Best Buy, RTINGS, TP-Link forum |
| **Navigation/docking errors** | Tapo RV30, Q10 S5+, Shark PowerDetect, Omni C20 | 4 | forums, Tom's Guide, Best Buy |
| **Hair wrap** | Tapo RV30, N30 Omni (axle ends) | 2 (Q10 S5+ praised as tangle-free) | GearLab, The Gadgeteer |

**Pet-waste reality check:** the famous 2016 "pooptastrophe" (Jesse Newton's Roomba smeared dog poop through his house overnight) is what owners fear [Independent, https://www.digitaltrends.com/home/poopocalypse-roomba-robot-vaccume/]. Practical rule from that story: don't schedule a camera-free robot to run while a puppy or sick pet is home alone.

---

## 11. Camera models people compare against (the "what you give up")

* **iRobot Roomba Max 705** (PrecisionVision AI camera, plus LiDAR): iRobot's Pet Owner Official Promise covers the Max 705 Vac, Max 705 Combo and Max 708 Combo — a free replacement if it fails to avoid **solid** dog/cat waste, first-year terms, and you must keep PrecisionVision on [Official, AU terms https://www.shopirobot.com.au/pet-owner-official-promise; US https://www.irobot.com/en_US/pet-promise.html; check US terms]. Ratings (snippets, seen 2026-11-23): Best Buy about 4.5 / 5 from about 147–150; **Target 4.1 / 5 from about 109 with only 33% recommending**; iRobot's own site about 3.9 [Retailer snippets, https://www.bestbuy.com/site/reviews/name/6618888; https://www.target.com/p/irobot-roomba-max-705-vac-robot-vacuum-autoempty-dock/-/A-94371675]. (The j7/j9 that launched the promise in 2021 are the predecessors.)
* **Roborock Saros 10R** (camera + structured light): RTINGS rates its avoidance "great", good with pet waste, weak spots USB cords and rug tassels; Tom's Guide four-month owner (dog + 2 cats) reports one cable incident in three months and turned on a feature that photographs pets/obstacles; weak pet-hair pickup per RTINGS/GearLab [Independent, https://rtings.com/robot-vacuum/reviews/roborock/saros-10r; https://www.tomsguide.com/home/home-appliances/roborock-saros-10r-review]. Saros 10 announces when the camera is live [Independent, 9to5Google 2025-04-18].
* **Dreame X50 Ultra** (camera): strong object recognition in tests; misses crumpled paper and short wires sometimes (TechRadar) [Independent, https://www.techradar.com/home/robot-vacuums/dreame-x50-ultra-complete-review]. It is also the model whose camera KISA could activate remotely in the Sept 2025 Korean test (since fixed) — the cleanest single illustration of the trade-off.

**Even cameras miss cords**: RTINGS notes some camera-and-light models still struggle with pet waste and power cords [Independent, RTINGS best-robot list via snippet]. Fair framing: a camera cuts the cord/poop risk a lot; it does not remove it.

---

## 12. Warranty notes owners hit

* **Roborock US:** limited warranty covers repair; replacement at Roborock's discretion; proof of purchase needed; repaired units get the longer of 90 days or the remaining term; repair doesn't restart the clock [Official, https://us.roborock.com/pages/service-warranty]. Complaint-site reports (2026): a Saros 20 Sonic back from service twice with the same "LiDAR blocked" error (from Aug 2026); a Saros 10 returned with scratched LiDAR [Weak, https://www.sikayetvar.com/en/roborock-us/roborock-saros-20-sonic-unresolved-sensor-issue]. Pattern for the post [Inference]: **the LiDAR turret is the part owners most often report failing**, camera or not — keep it dust-free and don't buy a no-turret-bumper model for a cluttered house.
* **iRobot:** see section 5; no 2026 change found.
* **TP-Link:** forum moderators escalate to email specialists; carpet/cliff fix handled privately (section 2).
* **eufy:** self-service repair application for mop alerts (section 6).

---

## Gaps for the writer
* No direct Reddit reading this cycle (blocked).
* US availability of Q7 M5 (US product URL 404), Qrevo S and N30 Omni (sold out at maker) needs the channels agent.
* Roomba 205 "camera" mention in TechRadar vs iRobot's no-camera list: manual check needed before stating "no camera" flatly (iRobot's own list is the source to cite).
* Shark "3D sensor" type and eufy C20 sensor naming (point laser vs LiDAR) are maker-vague.
