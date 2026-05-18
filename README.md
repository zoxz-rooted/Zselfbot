# Zoxzs Discord Selfbot
(documentation included)


A modern, dark-themed Discord selfbot toolkit built with **CustomTkinter**. Features a hacker-style splash screen, round buttons, scrollable panels, and a complete suite of Discord automation tools — including a **perfected guild nuker** with auto-role assignment and guaranteed spam delivery.

---

## Features

| Category | Tools |
|----------|-------|
| **Webhooks** | Spammer, Deleter |
| **Token Tools** | Info Lookup, Browser Login, Account Nuker, Status Rotator, Token Onliner |
| **Server Tools** | Server Info Lookup, Server Cloner, **Guild Nuker** |
| **Generators** | Nitro Generator, Bot Invite Generator, 4-Char Username Checker |
| **Utilities** | ID to Token (Base64), Report Bot |

---

## Guild Nuker — Total Annihilation

The flagship tool. Six phases of destruction:

1. **Rename** — Server renamed to `NUKED BY ZOXZS`, description wiped
2. **Purge Channels** — All existing channels deleted concurrently
3. **Purge Roles** — All roles except `@everyone` deleted
4. **Create 50 Channels** — Named `nuked-by-zoxz-1` through `nuked-by-zoxz-50`
5. **Create 10 Roles** — Named `cooked` in random neon colors, hoisted + mentionable
6. **Auto-Assign Roles** — Every member gets all 10 `cooked` roles
7. **Spam** — All 50 channels spammed simultaneously with guaranteed delivery (20 retries per message, rate-limit aware)

---

## Installation

```bash
pip install customtkinter requests pillow
```

Place your `image.png` (splash screen logo) in the same directory.

---

## Usage

```bash
python zoxzs_selfbot.py
```

The splash screen loads first, then the main UI appears.

---

## Token Onliner

Place tokens in `input/tokens.txt` (one per line) and hit **Start Onliner**.

---

## Proxy Support

Nitro generator and username checker support HTTP proxies. Load from `input/proxies.txt` or auto-scrape from public sources.

---

## UI

- Dark hacker theme (`#0b0b12` background)
- Round buttons (`corner_radius=22`)
- Scrollable panels (no cut-off buttons)
- Live console with color-coded output
- Status bar with real-time stats

---

## Disclaimer

This tool is for **educational and authorized testing purposes only**. The developer is not responsible for misuse.

---

## Credits

Developed by **RIN** for **PT**.
