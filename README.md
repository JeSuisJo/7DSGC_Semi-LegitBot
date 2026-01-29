# 7DSGC_Semi-LegitBot

Automation bot for **The Seven Deadly Sins: Grand Cross** (7DSGC).

---

## Prerequisites

- Python 3
- ADB (Android Debug Bridge) — included in `platform-tools/`
- Emulator or Android device with the game installed, connected via USB debugging

**Emulator setup:** the game window must be **1080×800** resolution with **200 DPI**.

---

## Where to stand before starting a mode?

**Your character must be at the tavern** before launching any mode.

Tavern style (season 1, 3, or 4KOA) does not matter — the bot works with any of them.

![Required position: tavern](img/README1.png)

Stand as shown in the image above, then start the chosen mode.

---

## The 3 modes

| Mode | Description |
|------|-------------|
| **1. Daily** | Full daily routine: equipment recycling, beer, food, daily demons, special dungeon, Yggdrasil, expeditions, daily PvP, send friend points. |
| **2. Auto Demon Farm** | Farm 1★ demons in a loop (with or without tickets), via the boss menu. |
| **3. Equipement Farm** | Automated equipment farming. |

---

## How to run

```bash
python main.py
```

Then select the mode (1, 2, or 3) from the menu.

---

## Configuration

Settings (e.g. daily demons with/without tickets) are in `config.json`.
