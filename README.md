# Final Fantasy Brave Exvius (FFBE) Offline — Patched Edition

Welcome to the **Patched Edition** of **FFBE Offline**! Built upon the amazing reverse-engineering and preservation work by the original creator, **[Elvlin](https://github.com/Elvlin/exvius-offline)**, this project preserves the full *Final Fantasy Brave Exvius* experience as a standalone, offline-playable game with custom quality-of-life enhancements, custom banner systems, infinite summons, and native support for modern Android devices and emulators.

---

## Direct APK Downloads (`v0.1.24-patched`)

Choose the edition that best suits your playstyle:

* **[Download Bonus Patched APK (`exvius-offline-v0.1.24-patched-bonus.apk`)](https://github.com/Frostzone123/exvius-live-feed/releases/download/v0.1.24-patched/exvius-offline-v0.1.24-patched-bonus.apk)** *(Recommended)*
  * **9,000,000 Lapis & 100,000,000 Gil Starter Injection**: Enjoy complete summoning freedom and max out your favorite units and vision cards right from the start.
  * Includes all gameplay enhancements, custom banners, stability fixes, and live OTA updates.

* **[Download Standard Patched APK (`exvius-offline-v0.1.24-patched.apk`)](https://github.com/Frostzone123/exvius-live-feed/releases/download/v0.1.24-patched/exvius-offline-v0.1.24-patched.apk)**
  * **Vanilla Progression**: Standard starting resources for players who prefer earning every Lapis through story progression, missions, and trial challenges.
  * Includes all gameplay enhancements, custom banners, stability fixes, and live OTA updates.

**[View Full Release Notes & Changelogs on GitHub Releases](https://github.com/Frostzone123/exvius-live-feed/releases/tag/v0.1.24-patched)**

---

## Features & Enhancements

### New in v0.1.24 (Upstream & Engine Fixes)
* **Battle Trust Mastery (TMR) Gains:** Units now have a 30% chance to gain +1% Trust Mastery upon clearing quests.
* **Super Trust (STMR) Moogle Fusion:** Fusing duplicates raises Super Trust, and the first identical fusion delivers a 50% All Trust Moogle to your mailbox.
* **Exploration Chest Fixes:** Equipment and materia chests in explorations are now correctly added to your inventory and remain opened permanently.
* **Unit Level Sync:** Fixed level rollbacks between battle results and the unit list.
* **Autoplay Repeat Fix:** Autoplay repeat (xN) now awards exp, gil, and drops accurately without duplicate charges.

### "United Forces" Custom Step-Up (Banner 9900001)
Build your dream summon banner!
* **Player-Selected Rate-Ups:** Choose your favorite Neo Vision (NV) and 5★ units directly from the in-game *Drop Rates* menu.
* **Guaranteed NV Step:** Step 6 features a guaranteed NV slot that awards one of your selected rate-up units if none dropped in prior slots.
* **Empty Pool Safety Guard:** If no units are selected, the summon button is safely locked to prevent accidental Lapis loss until you pick your targets.

### Infinite Step-Up Summon Loops
* **No More One-Lap Limits:** Step-up banners no longer lock out or disappear after completing a lap.
* **Seamless Reset:** Once you finish the final step of any banner, it automatically loops back to Step 1, letting you pull as many times as you want.

### Over-The-Air (OTA) Live Updates
* **Zero-Reinstall Fixes:** The game automatically checks for lightweight live patches on startup.
* **Instant Delivery:** Server fixes, balance adjustments, quest repairs, and new banner updates apply automatically over the air without having to redownload 14 GB of game data or reinstall APKs.

### Modern Android & Emulator Compatibility
* **Android 13, 14, 15, and 16 Ready:** Upgraded native loaders prevent linker and binder aborts on modern Android versions.
* **BlueStacks Air / ARM64 Fixes:** Patched native runtime libraries resolve known startup crashes on modern emulators.
* **Adaptive Screen Layout:** Native support for widescreen phones (19.5:9, 20:9), tablets, landscape orientation, and multi-window display modes.

### Safe In-Place Updates
* All APK releases are signed with a unified persistent key. Future APK updates can be installed directly over existing installations without losing your save data or downloaded assets.

---

## Getting Started

1. **Download & Install:**
   Grab either the **Bonus Edition** or **Standard Edition** APK above and install it on your Android phone, tablet, or emulator (such as BlueStacks Air).
2. **Initial Asset Download:**
   On first launch, the app will download the official ~14.5 GB client data assets. Make sure you have sufficient free storage space and a stable Wi-Fi connection.
3. **Jump In:**
   Once the asset download finishes, you can play through the entire story, summon any unit in the game's history, challenge high-level trials, and customize your party completely offline!

---

## Frequently Asked Questions

<details>
<summary><b>Does the game require an internet connection?</b></summary>

Internet access is only needed for the one-time initial download of the 14.5 GB base game assets and the quick startup check for live OTA patches. Core gameplay, battles, story, and summons run 100% locally on your device.
</details>

<details>
<summary><b>Will installing an updated APK erase my save file?</b></summary>

No! All releases use the same persistent signing key, allowing you to install updates directly over your existing app without touching your save data.
</details>

<details>
<summary><b>Where is my save data stored?</b></summary>

Your complete account progress (units, inventory, lapis, story clear state) is stored in a single file on your device at `files/local/state/campaign.json`.
</details>

---

## Credits & Acknowledgments

* **[Elvlin](https://github.com/Elvlin/exvius-offline)**: Creator of the original **Exvius Offline** project. Without their extraordinary reverse-engineering efforts, server reconstruction, and dedication to game preservation, none of this would be possible.
* **SQUARE ENIX CO., LTD. & gumi Inc.**: The original developers, artists, and creators of *Final Fantasy Brave Exvius*.

---

*Final Fantasy Brave Exvius is a registered trademark of SQUARE ENIX CO., LTD. This is a non-commercial, community preservation project.*
