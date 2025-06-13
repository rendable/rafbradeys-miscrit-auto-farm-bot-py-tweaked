## Miscrits Auto Bot

A simple bot for Miscrits that helps you grind EXP by auto-attacking enemies and capturing rare Miscrits using image recognition.

---

### ⚠️ Warning

This bot relies heavily on image recognition, which may be CPU-intensive on some systems.  
It is designed to work best with Miscrits running in **windowed mode** and has **not** been fully optimized for **fullscreen mode**.  

While I have **not been banned** for using this bot, **using third-party automation tools may still result in a ban**, so use at your own risk.

---

### 🚀 Features

- Rare Miscrit detection and intervention options
- Automated attacks on enemies using image recognition
- Auto-capture functionality with customizable behavior  
- Phone Notifications via NotifyRun (Only Works locally when connected to the same network)

---

### 📦 Updates as of 13/06/2025

- Added **Auto-Capture** feature that attempts to catch rare Miscrits automatically after attacking.
- Now uses relatie paths for images, so you can run the bot from any directory without needing to change paths in the code

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

### 🖼️ Adding Images for Rare Miscrit Detection

You can add your own images for rare Miscrit detection using the **Snipping Tool**—make sure the image is **clear** and **not obstructed**.  
If you haven't encountered a specific Miscrit yet, you may still obtain its image by snipping it from the **Map screen** where available Miscrits for the day are displayed.

Even if the Miscrit image is **greyed out** or **black and white**, it will still be detected because the bot enables **grayscale matching (`grayscale=True`)** for rare detection.

---

### 🗡️ Adding Images for Attacks

You may also add your own images for attack buttons using the **Snipping Tool**, but unlike rare detection, **grayscale is not enabled** for these.  
The image **must exactly match** what’s shown on screen—including color, clarity, and position—for detection to work properly.

You can use the sample images already included in the provided folders, but keep in mind they are limited to what has been tested.

---

### 🔍 Adding Images for Searchables

Searchable images (e.g., for buttons like "Battle Complete", "Yes", etc.) can also be customized.  
Just like attacks, these **do not use grayscale matching**, so be sure your snipped image **matches exactly** what appears in-game.  

Only one image per searchable is supported at the moment, and detection may fail if UI elements change due to resolution or screen scaling.

---

### 🐛 Known Bugs / Errors

- Auto-capture currently attempts a second catch, which may unintentionally spend platinum  
- Multiple image detection is temporarily broken—only works with **one** rare image selected  

---

### 📝 TODO

- Option to disable auto-capture after a single attempt to avoid spending platinum  
- Support for selecting **multiple images** for rare Miscrit detection  
- Add ability to **edit click positions** for attack and capture
- Instead of notifyrun, use **Discord Webhook** for notifications
- Optimize performance for better CPU usage (as of now it can be quite high)