# Owners brief: Video Doorbells Without a Subscription 2026 (Ring vs eufy vs Aqara vs Reolink)

Research agent 1 (Owners), compiled 2026-11-11 for the Nov 11 guide (blueprint `research/bf-devices-blueprint-2026-11.md` §3). About 50 web searches and 20 page fetches, plus one own data pull (the CPSC recall API).

**Rules followed.** No Amazon customer reviews, ratings, Q&A or review digests (Fakespot, ReviewMeta) were used. I dropped two search summaries that quoted "an Amazon reviewer" or an Amazon-sourced average (BGR's Battery Doorbell Plus figure). **Do not publish any Amazon number.**

**Access limits.**
* Best Buy (503), Walmart, Sam's Club (bot wall) and Lowe's (403) refused direct fetches. Every retailer rating below comes from a **search-result snippet** of the retailer's own review page. The snippet date is unknown, so each is marked "snippet, seen 2026-11-11". The counts move between cached copies, so give a range or say "about".
* reddit.com is blocked. Reddit material comes from the reddit.sentinel-team.org snapshot mirror **[Weak]**. Post dates there are worked back from "N days ago", so they are approximate.
* Brand forums (community.eufy.com, forum.aqara.com, community.ring.com, community.home-assistant.io) loaded fine, and their post dates are exact.

**Tags:** [Official] maker or government page · [Retailer snippet] · [Forum] brand or community forum with an exact date · [Weak] Reddit mirror or aggregator · [Independent] trade press · [Own data] · [Inference] · **UNVERIFIED**.

---

## 1. eufy Video Doorbell E340 (T8214111; battery or wired, dual camera, 8 GB built-in eMMC)

### Ratings at non-Amazon stores (all are snippets seen 2026-11-11)
| Store | Rating | Count | Note | Source |
|---|---|---|---|---|
| Best Buy (SKU 6547262) | 4.5 / 5 | 366 to 462 across cached pages (about 450 to 461 most recent) | Video quality sub-score 4.7 to 4.8 | https://www.bestbuy.com/site/reviews/eufy-smart-wi-fi-e340-2k-wired-and-battery-operated-video-doorbell-with-dual-cameras-black/6547262 |
| Lowe's | 4.5 / 5 | 74 | 87% would recommend | https://www.lowes.com/reviews/eufy-e8214119-doorbells/5019730589 |
| Walmart | 4.3 / 5 | 123 ratings (47 written) | Main E340 listing | https://www.walmart.com/ip/seort/5084823477 |
| Sam's Club | about 4.5 / 5 | 42 | 74% five-star | https://www.samsclub.com/reviews/product/15214200488 |
| Verizon | 4.5 / 5 | 43 | | https://www.verizon.com/products/eufy-security-video-doorbell-e340-with-dual-cameras |
| Navy Exchange | 4.54 / 5 | 41 | | https://www.mynavyexchange.com/eufy-security-e340-video-doorbell/19456444 |
| eufy.com own store | not found | | | UNVERIFIED |

### Praise
* **Picture quality and no monthly fee** lead the Best Buy praise (video sub-score about 4.7) [Retailer snippet, Best Buy].
* **Battery life varies widely and depends on settings.** A Best Buy owner went "2 months no charge" since unboxing [Retailer snippet, Best Buy p.5]. A Homes & Gardens tester ran it five months and called the charges long-lasting [Independent, https://homesandgardens.com/solved/eufy-e340-video-doorbell-review]. EFTM measured 33 days on "Optimal Surveillance" [Independent, https://eftm.com/2023/12/eufy-security-e340-dual-camera-solo-video-doorbell-review-a-smart-doorbell-with-offline-storage-240803].
* **The package camera (Delivery Guard) and motion accuracy** got praise, including from one owner who pairs it with HomeBase 3 [Retailer snippet, Best Buy].
* A wired owner on a 24 V AC transformer with a mechanical chime in the loop says it works "perfectly", including pre-roll and 120 s clips [Forum, community.eufy.com hard-wired thread, page 4, https://community.eufy.com/t/eufy-e340-video-doorbell-hard-wired-issues/3969948?page=4].

### Complaints and what fails first
1. **Fast battery drain on busy entrances.** Owner reports run from about two weeks (Lowe's owner; an Anker-store reviewer: "barely lasts 2.5 weeks") to months [Retailer snippets]. On the eufy forum, an owner lost 50% in one week on Balanced mode with a zone (2023-11-25). By 2024-06-30 he had switched to button-press-only activation because night motion and passing cars drained it [Forum, https://community.eufy.com/t/e340-battery-life/4023773]. A Reddit owner in 2026 writes of a drain "after 2 or 3 days" [Weak, mirror snapshot]. One commenter (via aggregator) warns against the E340 if the door faces a street [Weak].
2. **Wired mode does not mean battery-free.** The battery must stay in, and the wiring only trickle-charges it. The "Hard Wired Issues" thread started 2023-10-19 and passed 77 replies (the URL reaches /77). Owners see the plug icon briefly, then the unit falls back to battery and drains. Support blamed under-sized transformers (24 VAC 10 VA is not enough) and promised a firmware fix that owners say did not cure it [Forum, https://community.eufy.com/t/eufy-e340-video-doorbell-hard-wired-issues/3969948]. Owners cite **16 VAC 30 VA as the minimum for pre-roll**, and say the chime must be bypassed or disabled for pre-roll [Weak, Reddit mirror and forum; check against eufy's spec]. eufy's own troubleshooting page lists 16 to 24 V AC, 30 VA recommended [Official, https://service.eufy.com/article-description/Troubleshooting-eufy-Security-Video-Doorbell-E340-and-Indoor-Chime-Issues].
3. **Cold stops charging.** eufy says that in cold weather the E340 "may fail to recharge or even stop working", and gives a battery range of -20 °C to 50 °C [Official, https://service.eufy.com/article-description/Does-cold-weather-impact-eufy-Battery-Powered-Video-Doorbell]. Forum users say charging is cut near 32 to 40 °F [Forum, UNVERIFIED as a spec].
4. **Built-in storage glitches.** One owner, a week after install, saw storage show "full" with "0 MB free and 0 MB used". Formatting failed, the app has no restart option, and only a full reset and re-setup fixed it (2024-10-14/15) [Forum, https://community.eufy.com/t/e340-doorbell-stopped-sending-events-and-unable-to-format-sd-card/4534387]. The storage is not a removable card, so a failure here cannot be fixed by swapping a card.
5. **Firmware regressions (2026).** Reddit owners report an update from 3.1.4.0 to 3.2.5.0 that never completed and was followed by a return, weaker motion detection after 3.2.5.2, "loses connection multiple times per day" (April 2026), and the doorbell no longer ringing the mechanical chime [Weak, r/EufyCam mirror snapshots, Mar to Jun 2026, e.g. https://reddit.sentinel-team.org/subreddits/EufyCam/snapshots/2026-06-16T05%3A21%3A34.43805Z]. A German site reports "massive problems" with firmware 3.2.3.0 [Weak, https://www.smarthomeassistent.de/eufy-e340-doorbell-massive-probleme-mit-firmware-3-2-3-0/].
6. **Notification lag.** Expert Reviews calls it "quite slow at delivering alerts" [Independent, https://www.expertreviews.co.uk/technology/home-security/eufy-video-doorbell-e340-review]. A HomeBase 3 owner measured about 6 s of doorbell lag while S300 cameras on the same base were near-instant [Forum, https://community.eufy.com/t/alexa-notification-lag-delay-eufy-battery-doorbell-with-echo-show-and-dot/1114547?page=2]. Other eufy owners report 5 to 10 min delays on cameras; the model is not always the E340 [Forum].
7. **Setup on 2.4 GHz only.** A Best Buy owner had trouble on a mesh network with a shared SSID; others call setup "clunky" [Retailer snippet, Best Buy].
8. **Existing chime.** eufy says the E340 works with mechanical chimes [Official]. Owners report the chime not firing, and support answered vaguely that it "may not be compatible with all chime systems" [Forum, https://community.eufy.com/t/indoor-chime-not-ringing/5772893]. The app cannot silence the mechanical chime [Forum]. A Best Buy reviewer says buying extra chimes was needed [Retailer snippet].
9. **Support quality.** Slow or unhelpful support recurs in Best Buy and forum reports [Retailer snippet; Forum].

### HomeBase notes
* An S380 (HomeBase 3) owner with eight cameras reported the doorbell offline around firmware 3828 and said "quite a few users" saw the same [Weak, r/EufyCam mirror, 2026]. eufy's fix is to power-cycle for 30 s, then remove and re-add the base [Official, https://service.eufy.com/ca/article-description/S380-HomeBase-HomeBase-3-Goes-Offline].
* A Reddit fix after a factory reset is to use "Connect to Router" rather than "Connect to HomeBase" [Weak].
* A buyer found the **S330 wired doorbell does not store video on HomeBase 3, while the E340 does** [Forum, https://community.eufy.com/t/just-purchased-from-eufy-direct-s330-wired-doorbell-homebase-3-combo-video-storage/4659531]. UNVERIFIED with eufy; check before writing.

### Variant traps owners trip on
* **E340 vs S330.** S330 is wired-only; aggregator Reddit comments say it needed a transformer upgrade but is solid [Weak, redditrecs via search]. A comparison site picks the E340 for unwired doors and the S330 for hard light [Weak, smarthomecompared].
* **"E340" is also a floodlight camera.** Several community threads, such as "E340 Floodlight Cam – Wi-Fi Issues After 18 Months" [Forum, https://community.eufy.com/t/e340-floodlight-cam-wi-fi-issues-after-18-months/5759201], are not about the doorbell. Readers who search for the doorbell will hit them.
* **E30:** I found no doorbell E30 owner data. Search results for "E30" are the **Floodlight Cam E30**. UNVERIFIED that a US "Video Doorbell E30" exists; the guide should say "E340 (not the floodlight)".
* The E340 has no HDR and no HomeKit [Weak, comparison pages].

---

## 2. Reolink Video Doorbell (WiFi D340W, PoE D340P, Battery D340B, and the new Video Doorbell 2nd Gen)

### Ratings (snippets seen 2026-11-11)
| Store | Model | Rating | Count | Source |
|---|---|---|---|---|
| Reolink.com own store | Video Doorbell WiFi | 4.51 / 5 | 84 | https://reolink.com/review/reolink-video-doorbell-wifi (snippet; the page renders empty when fetched) |
| Reolink.com own store | Video Doorbell 2nd Gen | 4.67 / 5 | 3 | https://reolink.com/review/reolink-video-doorbell-2nd-gen (snippet) |
| Best Buy | Smart Wi-Fi Video Doorbell wired with chime (SKU 6551473) | 4.5 / 5 | 8 | https://www.bestbuy.com/site/reviews/reolink-smart-wi-fi-video-doorbell-wired-with-chime-white/6551473 |
| Best Buy | Battery Doorbell D340B | 3.6 to 3.8 / 5 | 4 to 5 | https://www.bestbuy.com/product/reolink-battery-doorbell-smart-2k-4mp-black/6620128 |
| Best Buy | D340B (another listing) | "4.8 / 5105 reviews" | | https://www.bestbuy.com/product/reolink-d340b-smart-video-doorbell-2k-4mp-battery-operated-wireless-wi-fi-with-head-to-toe-view-and-plug-in-chime-black/J3R84PK8PT — **UNVERIFIED, probably marketplace or syndicated; do not publish** |
| Home Depot, Walmart, Lowe's, Costco | | not found | | UNVERIFIED |

Reolink has few US big-box reviews; most of its evidence is forums.

### Praise
* **Home Assistant, Frigate and NVR integration** is the main reason owners pick it. One owner (2024-07-12) called the HA and Frigate integration strong and the PoE model "highly recommended" [Forum, https://community.home-assistant.io/t/doorbell-recommendations/315527?page=3].
* **The WiFi model can be stable with current firmware.** One owner on existing doorbell wiring was stable "for nearly two years", and later firmware fixed connectivity (2024-12-10) [Forum, same thread]. Another owner has run one since release alongside five PTZ cameras (2024-11-05) [Forum].
* **PoE is the reliable choice:** "much more reliable than Wi-Fi" and "issue-free" [Weak, redditrecs via search].
* **Night vision** is reviewed well [Independent, multiple].
* **The HA integration keeps working with internet access blocked** [Official, https://home-assistant.io/integrations/reolink].

### Complaints and what fails first
1. **WiFi model drops offline.** One ipcamtalk tester saw repeated timeouts across firmware versions while 40 other clients on the same network stayed stable, and said friends and Reddit users saw the same. Another theory: the WiFi unit's CPU and RAM are too weak for several simultaneous streams (it recovered after HA connections were cut) [Weak or forum, ipcamtalk posts 850746 and 1010459, via search; the pages return 403]. A 2024-07-12 HA forum owner says the WiFi model "kept shutting off" [Forum].
2. **PoE is not flawless.** One owner's PoE unit dropped off the switch more than a dozen times a day [ipcamtalk 911755, snippet]. A HA user (2024-11-25) reports repeated PoE problems across several sites, an unreliable RTSP stream and settings that need the app [Forum]. A wired unit lost power on each press or detection even after a replacement and a bigger transformer (2024-03-05) [Forum].
3. **Weather.** The microphone failed after heavy rain despite the IP65 rating; the owner replaced the mic and added a cover (2025-05-17) [Forum, HA thread page 3].
4. **Lag into Home Assistant.** 3 to 5 s from press to automation against an instant Reolink app [Forum, https://community.home-assistant.io/t/reolink-video-doorbell-delay-with-home-assistant-seeking-advice/758336]. About 10 s when the doorbell sits on another VLAN or its internet is blocked, a "known bug" per one thread [Forum]. HA's docs explain a fallback to 5 s polling when push fails [Official, HA integration page].
5. **Chime.** Reolink's own guide says wiring to an existing **mechanical chime may buzz or hum**, and sells the RLA-PK1 Power Kit to fix it (Battery, D340B and SE models) [Official, https://support.reolink.com/articles/54017694345625-RLA-PK1-Power-Kit-Installation-Guide-Fix-Mechanical-Chime-Buzzing-with-Reolink-Doorbells/]. MBReviews says the WiFi model "can't use the existing chime" [Independent, https://www.mbreviews.com/reolink-video-doorbell-wifi-review/]. Reolink's install note says the old mechanical chime stops ringing once the old button is removed [Official, Reolink community]. The included wireless chime can be hard to pair (5MP model) [Weak, ShopSavvy].
6. **microSD.** No mass failure pattern found. One D340W owner saw "no SD card detected" [Weak, asktech.support]. Reolink lists "unformatted or format failed" with incompatible or badly seated cards as the cause [Official, https://support.reolink.com/hc/en-us/articles/12703470902809-Troubleshooting-for-Video-Doorbell-PoE].
7. **Resold units.** An eBay unit died within hours; a unit from a different seller worked (2024-11-05, 2025-01-19) [Forum]. [Inference] Buy new from Reolink or a major retailer.

### Video Doorbell 2nd Gen (new, on sale 2026-07-20)
* Qualcomm QCC730 low-power WiFi, 4MP 1:1 head-to-toe view, microSD up to 512 GB, $149.99 at reolink.com [Official or press, https://reolink.com/blog/reolink-releases-the-video-doorbell-2nd-gen/].
* Caveats: **24/7 recording and pre-record only in wired mode**, **no chime in the box**, and it does **not work with the older Reolink Chime** [Independent, T3 and digitalreviews via search]. Switching to wired mode needs NVR firmware v3.6.5+, and through Home Hub only after an update "expected September 2026" [Official, https://support.reolink.com/articles/60553722670617-FAQs-Reolink-Battery-Video-Doorbell-2nd-Gen/]. UNVERIFIED whether that update shipped.
* Owner data is too thin to judge: one forum post reports a drain in about two days with the PC-app live feed not timing out [Forum, https://community.reolink.com/post/41903, date not captured]. The marketing claim is 300 days or "up to 10 months". **Too new for an owner verdict.** Say so.

---

## 3. Aqara Doorbell Camera Hub G410 (and G410 Select, G400, G4)

### Ratings (snippets seen 2026-11-11)
| Store | Model | Rating | Count | Source |
|---|---|---|---|---|
| Best Buy (SKU 6638669) | **G410 Select** (wired or battery) | 4.4 / 5 | 48 to 55 across snapshots | https://www.bestbuy.com/site/reviews/aqara-video-doorbell-camera-wired-battery-powered-hub-g410-select-black/6638669 |
| | | video sub-score 4.8, app 4.2; 91% would recommend (one snapshot) | | same |
| Trustpilot (aqara.com, all products) | | 42 reviews; several 1-star about the G410 ("G410 Doorbell is junk") and support | | https://ca.trustpilot.com/review/aqara.com [Weak; not product-specific] |
| aqara.com US store, Home Depot, Walmart | | not found | | UNVERIFIED |

**Variant note:** the model Best Buy sells is the **G410 Select**. Retail listings say Aqara's HomeGuardian cloud was introduced for the Select, with a 3-month trial [Weak, domadoo and passionhome.sg]. Colours differ (Select: black or white; base: black or grey). A full spec difference is UNVERIFIED, so do not claim one without Aqara's page.

### Praise
* **Fast in HomeKit.** One owner since launch calls it "rock solid", "significantly better than the G4", with battery life the only gripe. Another says eufy's delay was "horrible" and the G410 has "no delay" [Weak, redditrecs aggregator via search; the site has since shut down]. MacStories (one month): rings arrive "quickly", the mmWave radar cut recorded events, and lingerer alerts dropped after faces were added [Independent, https://www.macstories.net/reviews/one-month-with-the-aqara-g410-video-doorbell/].
* **Survives weather when sheltered.** In r/HomeKit (about mid-July 2025, 15 comments), a Canadian owner reports it running since about Christmas through extreme cold, freezing rain and snow under an open porch. A Chicago owner reports a year with no downtime through hot summers and sub-zero winters [Weak, https://reddit.sentinel-team.org/posts/1rrr395/snapshots/2026-03-13T08%3A36%3A51.352236Z]. An Aqara forum owner reports no water damage through storms [Forum, https://forum.aqara.com/t/water-damage-risk-with-g410/353799].
* **Custom MP3 chimes, adjustable chime volume, and a hub (Matter, Thread, Zigbee) built in** [Independent, MacStories, BGR].

### Complaints and what fails first
1. **AA battery life far below the "up to 5 months" claim, plus sudden-drain episodes.**
   * Thread of 2026-09-29 to 10-02 (8 replies): IKEA 2400 mAh rechargeables lasted just under 1 month at 5 to 10 clips a day; the included alkalines about 1 month plus 2 weeks; Energizer Max 2 months for one owner and 3 to 4 months for another; 1.5 V rechargeables usually 3 to 4 months, shorter in a stormy season with false triggers [Forum, https://forum.aqara.com/t/g410-battery-life/340924].
   * **Nov 4 to 5, 2026, still open:** after a new firmware, an owner whose batteries used to last 2 to 3 months got a low-battery warning 3.5 h after fresh AAs. Energizers lasted about 4 days, alongside constant phantom "lingering" alerts. Support asked them to try low-power mode. A forum user suspects the mmWave sensor [Forum, https://forum.aqara.com/t/g410-major-battery-drain/355433].
   * Other titles: "G410 batteries dead in less than 24 hours" [Forum, https://forum.aqara.com/t/g410-batteries-dead-in-less-than-24-hours/230925]. A 2026-03-27 post: 6 AAs lasted 11 days [Forum, below].
   * Aqara staff say 1.2 V NiMH cells or mixed old and new cells shorten life [Forum, via search]. WhistleOut says the battery level isn't reported accurately in the apps [Independent, https://www.whistleout.com.au/Broadband/Reviews/Aqara-G410-Review].
2. **Missed presses, offline at the moment of the ring, missing recordings.** In a 2026-03-19 post (firmware 4.5.20, wired), the camera goes offline 20 to 30 s on a press, sends no snapshot and records nothing to SD or cloud. The cause was likely an undersized 8 V/8 VA transformer. Another owner (2026-05-11) had clips cached but not written to SD, fixed by a restart. AqaraBot closed the thread as "resolved via email" with no details [Forum, https://forum.aqara.com/t/g410-issue-stream-drops-events-not-recorded-notifications-missing/272367].
3. **WiFi and chime-repeater distance.** In r/HomeKit (about Feb 2025, 20 comments), a brick wall between the doorbell and the chime or repeater hurt the link; a wood spacer helped, but a reboot was still needed about every 4 days [Weak, https://reddit.sentinel-team.org/posts/1pur03q/snapshots/2025-12-26T11%3A00%3A38.028453Z]. Other thread titles: "G410 constantly disconnecting", "Network connection failed", "G410 Notification Delays", "False Lingerer Notifications" [Forum, https://forum.aqara.com/tag/DoorbellCameraHubG410]. Support blames distance to the repeater or chime, or interference [Forum].
4. **Not waterproof (IPX3 main unit).** TechRadar's review headline says it is "not waterproof" [Independent, https://www.techradar.com/home/smart-home/aqara-doorbell-camera-hub-g410-review]. Mighty Gadget calls IPX3 "minimal" [Independent]. The forum asks whether a G410 rain cover exists; owners 3D-print one because the G4 case does not fit [Forum, https://forum.aqara.com/t/silicone-waterproof-cover-for-g410/41800].
5. **HomeKit video is capped below 2K** (1080p per BGR, 1200p per MacStories) [Independent].
6. **No legacy mechanical chime** per an owner comment [Weak, redditrecs via search]. UNVERIFIED with Aqara.
7. **"Fails at being a doorbell" (2026-03-27):** 11 days on 6 AAs, not waterproof, wiring couplers missing from the box, features behind a subscription. Two replies partly agree and one disputes it. AqaraBot closed it 2026-04-01 [Forum, https://forum.aqara.com/t/aqara-g410-a-doorbell-that-fails-at-being-a-doorbell/276270].
8. Best Buy owners mention the device is **larger than expected** [Retailer snippet].

### G410 vs G400 vs G4 (questions owners ask)
* The **G400 is wired-only** (PoE or 8 to 24 V doorbell wiring), with no battery and no hub. The **G410 runs on battery or wire and is a Matter, Thread and Zigbee hub**. 24/7 recording on the G410 works only wired [Weak, passionhome.sg; https://forum.aqara.com/t/g400-vs-g410-differences/272811 not opened].
* One owner prefers the G410's image to the G400's [Weak, aggregator]. In mid-2025 two r/HomeKit commenters advised waiting for the G400 [Weak]. G4 owners call the G410 a big step up [Weak].

---

## 4. Ring Battery Doorbell 2K (2nd Gen) and Wired Doorbell 2K

### Ratings (snippets seen 2026-11-11). **Watch the SKU: Ring re-uses "2nd Gen".**
| Store | Model | Rating | Count | Source |
|---|---|---|---|---|
| Best Buy SKU 6672118 / 12592817 | **Battery Doorbell (Newest Model), Retinal 2K, built-in battery** | no aggregate in snippets; "highly rated"; reviews short and positive ("good bang for your buck") | | https://www.bestbuy.com/product/ring-battery-doorbell-newest-model-retinal-2k-with-wide-angle-video-up-to-6x-zoom-two-way-talk-and-built-in-battery-speckled-grey/J39TLSSR6C/sku/6672118/reviews — rating UNVERIFIED |
| Best Buy | Wired Doorbell 2K (newest model, SKU 6672117 probable) | 4.6 / 5 | 29 | snippet; SKU match UNVERIFIED, https://www.bestbuy.com/product/ring-wired-doorbell-newest-model-retinal-2k-with-wide-angle-video-up-to-6x-enhanced-zoom-and-two-way-talk-speckled-grey/J39TLSPYTY/sku/6672117/reviews |
| Best Buy SKU 6589895 / 6589894 | Battery Doorbell (2024, head-to-toe, previous model) | 4.8 / 943 (Satin Nickel); 4.7 / 1,510 (Venetian Bronze) | | snippets |
| Best Buy SKU 6441424 | **"Ring Video Doorbell (2nd Gen.)", the 2020 model (5UM5E5), the recall family** | 4.7 / 5 | about 10,950 | snippet. **Do not cite this as the current "2nd Gen".** |
| Target, Home Depot, Walmart | Battery Doorbell 2K | not found | | UNVERIFIED |

### Praise
* Owners upgrading from older Rings describe a big jump in sharpness; it is the cheapest way into Ring's 2K line [Retailer snippet, Best Buy; Weak, smarthomecompared].
* Best Buy pros listed: video quality, field of view, ease of setup, two-way talk [Retailer snippet].
* **Without a plan, Live View, real-time motion alerts, two-way talk and motion zones still work.** Ring's own blog (2026-07-16) says of Live View: "Any camera. Any time. No subscription." It lists video history (up to 180 days), Snapshot Capture, **Person Detection** and the extended warranty as plan-only [Official, https://blog.ring.com/home-security/ring-cameras-without-subscription/]. **This upgrades the blueprint's "reported, not confirmed" note to confirmed by Ring**, and adds that person alerts need a plan.

### Complaints and what fails first
1. **The built-in battery means unmounting the whole doorbell to charge it via USB-C.** Owners say they wish they had bought the Plus, which has a pull-out pack. "The battery can't be replaced", says a Best Buy reviewer, still positive overall [Retailer snippet; Weak, smarthomecompared]. A 2024 head-to-toe owner was disappointed to be left without a doorbell while it charges [Retailer snippet].
2. **Cold.** Ring says very cold weather affects the battery, and that it may stop working completely at -5 °F until it warms [Official or forum staff, community.ring.com via search]. In r/Ring (about May 2025, 15 comments), a hardwired **Battery Doorbell Pro** loses preview and connectivity around -25 °C. Commenters explain that Ring battery doorbells run from the battery even when wired, that below about 30 °F the voltage sags, and that the only lasting fix is a wired-only model [Weak, https://reddit.sentinel-team.org/posts/1qzn61o/snapshots/2026-02-09T03%3A00%3A29.193967Z]. **No 2026 Battery Doorbell 2K-specific cold reports found.** [Inference] The same physics applies.
3. **No recordings without a plan is the big owner frustration**, and person detection needs a plan too [Official, Ring blog]. Forum owners report Live View failing "the minute your trial is over" [Forum, https://community.ring.com/t/live-view-is-not-working-without-subscription/223314, isolated].
4. **Late alerts.** An analysis of late-July 2026 1-to-3-star Ring **app-store** reviews finds late alerts and missed events dominate, with one alert about 3 min after motion [Weak, https://unstar.app/blog/ring-app-not-working-late-alerts-missing-footage-2026; app-store reviews, not Amazon]. A March 2026 app version (about 3.100.1) forced "Collections" [Weak, r/Ring mirror].
5. **Search Party backlash (Feb 2026).** On by default, switched off per camera in Control Center. Redditors and TikTokers posted how-tos, and one outlet claims mass returns [Independent, Engadget; Weak, gadgetreview "Ring Owners Revolt", scale UNVERIFIED]. The Flock partnership was cancelled, but Search Party stayed [Independent, GeekWire 2026, https://www.geekwire.com/2026/ring-cancels-flock-partnership-amid-broader-surveillance-concerns/].
6. **Chime.** Ring says the **Wired Doorbell 2K Plus**, the non-PoE Wired Doorbell 4K Pro, Video Doorbell Wired and Peephole Cam **do not support an in-home chime** and need a Chime Kit Mini [Official, https://ring.com/support/articles/vk1ml/connecting-your-ring-doorbell-to-an-existing-in-home-chime, "Last updated 2 months ago"]. **The base Wired Doorbell 2K is not on that page.** A review site says it does not ring a mechanical chime [Weak, smarthomecompared]. UNVERIFIED; check the linked compatibility list before publishing.
7. **Hardwired battery models eventually report battery power and drain** (owner reports on earlier models) [Weak, fixoryhq summarizing Ring Community].
8. **Naming.** A third-party site says Ring renamed the Battery Doorbell Plus (2nd Gen) to "Battery Doorbell 2K Plus" in August 2026 [Weak, UNVERIFIED]. Ring's own chime page does use "Wired Doorbell 2K Plus", which supports the 2K-suffix naming.

---

## 5. Alternates (only if needed)

* **TP-Link Tapo D235 or D225.** Reviews are positive (Expert Reviews "new king", T3 Platinum). The cons: 2.4 GHz only, and the microSD card sits in the outdoor unit, where a thief can take it (Coolblue owner) [Independent; Weak]. Battery reports run from under a day (D235 owner; fixed later via integration settings) to barely any drain after moving to mesh WiFi four months in [Forum, https://community.tp-link.com/en/home/forum/topic/834012]. CyberShack measured 1 to 3% a day over four weeks [Independent]. **No US big-box ratings found**, so I would not add it as a pick.
* **Google Nest Doorbell (battery).** It gives 3 h of free event history. Best Buy owners call it "terrible" given the plan price [Retailer snippet, https://www.bestbuy.com/site/reviews/google-nest-wi-fi-video-doorbell-battery-operated-snow/6473256]. Google confirmed outdoor Nest batteries struggle to charge in the cold [Independent, TechRadar, 2022]. It is not a no-subscription device.

---

## 6. What owners complain about (cross-cutting patterns for the box)

1. **Battery claims vs reality (all four battery models).** Makers say 5 to 10 months; owners at busy doors get 2 weeks to 3 months. The drivers owners name are street-facing doors, night motion, false triggers (storms, lingering alerts) and weak WiFi (a Tapo owner's mesh upgrade fixed it). The tip owners actually use is narrower detection zones and button-only or low-power modes.
2. **"Wired" battery doorbells still run on the battery.** eufy E340, Ring battery models and Aqara G410 owners all report that the transformer only trickle-charges. They cite undersized transformers (8 to 10 VA) as the cause of drain, missed presses or no pre-roll. eufy wants 16 to 24 V AC at 30 VA. Aqara's failure case had 8 V/8 VA. [Inference] Tell readers to check the transformer before buying.
3. **Cold stops charging or kills power.** eufy (charging stops) and Ring (dead at -5 °F; owners say trouble below about 30 °F) both say so officially. Wired-only models avoid it. The Aqara G410 on AAs had positive reports from Canada and Chicago (sheltered).
4. **The existing chime is a lottery.** Ring's 2K Plus and Wired lines don't ring it. Reolink buzzes without a power kit, and its 2nd Gen ships without a chime and won't pair the old one. eufy E340 owners report chimes that stop after firmware. The G410 reportedly has no mechanical support.
5. **Firmware updates break things.** E340 (3.2.3.0, 3.2.5.x), HomeBase 3 (3828), Aqara (battery drain after an update, Nov 2026). Owners complain of no release notes.
6. **Notification lag.** eufy (seconds to minutes; worse via HomeBase), Ring app reviews (minutes, July 2026), Reolink into Home Assistant (3 to 10 s, fixable). The Aqara G410 in HomeKit is the one praised as fast.
7. **Local storage glitches.** E340 built-in storage stuck "full", Reolink SD "not detected or format failed", G410 clips not written to SD. All are usually cured by reformat, restart or reset, but you lose footage until you notice.
8. **Weatherproofing.** G410 IPX3 (shelter it). One Reolink mic died after heavy rain (IP65).
9. **Support** is weak at eufy and Aqara (AqaraBot closes threads "resolved via email").
10. **Ring-specific:** no recordings or person alerts without a plan, Search Party on by default, and unmounting the base 2K to charge it.

Questions readers actually ask (for the FAQ): Does it work with my existing chime? Will it run off my doorbell wires without the battery? How long does the battery really last? Does it work in winter? Can I get Home Assistant or HomeKit without a cloud plan? Which version is this (G410 vs Select vs G400; E340 doorbell vs floodlight; Ring "2nd Gen" 2020 vs 2026)?

---

## 7. Recalls

**Own data (CPSC SaferProducts API, https://www.saferproducts.gov/RestWebServices/Recall, queried 2026-11-11).** I searched recall titles for Ring, eufy, Anker, Reolink, Aqara and "Doorbell", and product names for eufy, Reolink, Aqara and "Video Doorbell".
* **Ring: one recall,** #21028, **2020-11-10**, "Ring Recalls Video Doorbells (2nd Generation) Due to Fire Hazard". It covers model **5UM5E5** with certain serial numbers, about 350,000 US units sold **June to Oct 2020**. The battery can overheat when the **wood screws are used in place of the security screws**: 85 reports, 23 fires, 8 minor burns. The remedy is revised install instructions, and owners keep the doorbell; serial check at support.ring.com/ring-2nd-gen-recall [Official, https://www.cpsc.gov/Recalls/2021/Ring-Recalls-Video-Doorbells-2nd-Generation-Due-to-Fire-Hazard; Health Canada says a correctly installed unit poses no risk].
  * **Relevance to the current models: none directly.** The recall is the 2020 "Video Doorbell (2nd Generation)", not the 2026 "Battery Doorbell (2nd Gen)" / Battery Doorbell 2K, and not the Wired Doorbell 2K. **But the names collide.** Best Buy SKU 6441424 "Ring Video Doorbell (2nd Gen.)", with about 10,950 reviews, is the 2020 family. The guide should say this in one line. It should not attach the recall to the new model.
* **eufy:** no CPSC recall of any eufy product.
* **Anker (eufy's parent):** power banks, coolers and a speaker only: 2025-06-12 PowerCore 10000 A1263 (#25338), 2024-10-17 power banks (#25011), 2024-12-05 Soundcore speakers (#25056), 2024-03-07 EverFrost coolers (#24146), 2023-03-09 (#23147, Fantasia Trading). **No camera or doorbell.** A further Anker power-bank recall of about 481,000 units (reported in 2025) appears in news results; its CPSC number was not captured [UNVERIFIED].
* **Reolink, Aqara:** no CPSC recalls.
* **Video doorbells overall:** the 2020 Ring recall is the only CPSC doorbell recall.

**Our Recall Check page (`brand/pages/recall-check.html`, 228 entries, grepped 2026-11-11).** There is no entry for Ring, eufy, Reolink, Aqara or any doorbell. The related entries are **Anker PowerCore 10000 (A1263), recalled Jun 12, 2025**, already linked to our Black Friday tech guide, and **Wyze Solar Cam Pan security cameras**, a different brand but a related category. [Inference] The doorbell guide can link Recall Check in one sentence ("no open recalls for these models as of Nov 11, 2026; Ring's 2020 recall covered the older Video Doorbell 2nd Gen") without adding entries.

**Not a recall but buyers ask about it:** the eufy NY AG settlement (Jan 2025) over unencrypted streams is a privacy matter, not a CPSC safety recall. One news result gives $640,000 against the blueprint's $450,000 (Hunton); **use the Hunton figure and re-check**.
