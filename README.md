## Miscrits Auto Bot

A GUI automation bot built to grind EXP efficiently in Miscrits by performing automated actions like attacking enemies and auto-capturing rare Miscrits. It uses image recognition to detect specific UI elements and simulate interactions, allowing continuous farming without manual input.

### ⚠️ Warning

This bot relies heavily on image recognition, which may be CPU-intensive on some systems.  
It is designed to work best with Miscrits running in **windowed mode** and has **not** been fully optimized for **fullscreen mode**. For best results, keep the game window visible and avoid overlapping elements.

---

### 🚀 Features

- Rare Miscrit detection and intervention options  
- Auto-capture functionality with customizable behavior  
- Phone Notifications via NotifyRun  

---

### 🛠️ Installation & Setup

#### 1. Install Python Dependencies

```bash
pip install notify-run pillow pyautogui keyboard
```

#### 2. Optional (NotifyRun Setup for Phone Notifications)

NotifyRun allows the bot to send push notifications to your browser or phone, so you can be alerted when rare Miscrits appear or actions complete—without needing to watch the game continuously.

1. Open your command prompt and run:

```bash
notify-run register
```

This will open a browser window to link your device. After linking, you can send a test notification with:

```bash
notify-run send "NotifyRun is set up!"
```

Your channel URL (e.g., `https://notify.run/YOUR_CHANNEL_ID`) will be saved automatically.  
**Make sure to allow notifications on your phone or browser when prompted.**

---

### 📦 Updates as of 13/06/2025

- Added **Auto-Capture** feature that attempts to catch rare Miscrits automatically after attacking.

---

### 📝 TODO

- Option to disable auto-capture after a single attempt to avoid spending platinum  
- Support for selecting **multiple images** for rare Miscrit detection  
- Add ability to **edit click positions** for attack and capture  

---

### 🐛 Known Bugs / Errors

- Auto-capture currently attempts a second catch, which may unintentionally spend platinum  
- Multiple image detection is temporarily broken—only works with **one** rare image selected  
