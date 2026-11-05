# Exvius Live Feed (`Frostzone123/exvius-live-feed`)

Lightweight live-configuration feed for custom **In-Game Mailbox Gifts**, **Over-the-Air (OTA) Server Hot-Patches**, and **Patched APK Releases**.

## Direct APK Downloads (`v0.1.21-patched`)
- **[Download Standard Patched APK (`exvius-offline-v0.1.21-patched.apk`)](https://github.com/Frostzone123/exvius-live-feed/releases/download/v0.1.21-patched/exvius-offline-v0.1.21-patched.apk)** — Vanilla starting Lapis/Gil + all Emulator & Android 13–16 fixes + Live Mailbox/OTA feed.
- **[Download Bonus Patched APK (`exvius-offline-v0.1.21-patched-bonus.apk`)](https://github.com/Frostzone123/exvius-live-feed/releases/download/v0.1.21-patched/exvius-offline-v0.1.21-patched-bonus.apk)** — Includes a one-time **9,000,000 Lapis + 100,000,000 Gil** starter bonus + all fixes + Live Mailbox/OTA feed.
- **[View Release Notes](https://github.com/Frostzone123/exvius-live-feed/releases/tag/v0.1.21-patched)**

---

## 1. Sending In-Game Mailbox Gifts (`mailbox.json`)

Edit [`mailbox.json`](mailbox.json) (even directly from GitHub in your browser!) and add a new entry to the `"mails"` array.

Every time a player opens the app (or loads their save), the game fetches `mailbox.json` and delivers any new `mail_id` directly into their **in-game Mailbox**! Because `mail_id` is tracked per save file, each player will only receive a given `mail_id` once.

### Example `mailbox.json` Entry
```json
{
  "mail_id": "weekend_gift_002",
  "title": "Weekend Event Bonus!",
  "message": "Enjoy 10,000 Lapis and 10 Rare Summon Tickets!",
  "icon_type": 2,
  "items": [
    [50, 1, 10000],
    [23, 180, 10]
  ]
}
```

### Item Type Reference (`[item_type, item_id, count]`)
| `item_type` | What It Grants | `item_id` | Example (`[type, id, count]`) |
| :--- | :--- | :--- | :--- |
| **`50`** | **Lapis** | `1` | `[50, 1, 10000]` (10,000 Lapis) |
| **`30`** | **Gil** | `1` | `[30, 1, 5000000]` (5,000,000 Gil) |
| **`51`** | **Friend Points** | `1` | `[51, 1, 10000]` (10,000 Friend Points) |
| **`23`** | **Tickets / Important Items** | Ticket ID (e.g. `180` = 5★/NV Ticket) | `[23, 180, 10]` (10 Tickets) |
| **`10`** | **Unit** | 9-digit `F_UNIT_MST` ID | `[10, 213000105, 1]` (1x Lightning) |
| **`21`** | **Equipment (Weapon/Armor/Acc)** | `F_EQUIP_ITEM_MST` ID | `[21, 403046900, 1]` |
| **`22`** | **Materia (Ability)** | `F_MATERIA_MST` ID | `[22, 504200010, 1]` |
| **`20`** | **Consumable / Regular Item** | `F_ITEM_MST` ID | `[20, 101000100, 10]` (10x Potion) |
| **`27`** | **Vision Card** | `F_VISION_CARD_MST` ID | `[27, 100000001, 1]` |

### `icon_type` Options
- `0`: Standard Envelope
- `1`: Exclamation / Notice
- `2`: Treasure Chest
- `3`: Gold Invitation

---

## 2. Pushing Over-the-Air (OTA) Server Hot-Patches (`patches/manifest.json`)

Whenever you want to push an updated Python server module (e.g., `ffbe_gacha.py`, `ffbe_battle.py`, `player_state.py`) or JSON data file to your friends **without making them download a new APK**:

1. Put the updated `.py` or `.json` file into the `patches/` folder in this repo.
2. Add an entry to [`patches/manifest.json`](patches/manifest.json) with its filename and SHA-256 hash:
   ```json
   {
     "schema": 1,
     "revision": 2,
     "files": [
       {
         "name": "ffbe_gacha.py",
         "url": "https://raw.githubusercontent.com/Frostzone123/exvius-live-feed/main/patches/ffbe_gacha.py",
         "sha256": "<sha256-of-file>"
       }
     ]
   }
   ```
3. On next app launch, your friends' apps will automatically download the file into `exvius/live_patches/` and load it ahead of the bundled version!
