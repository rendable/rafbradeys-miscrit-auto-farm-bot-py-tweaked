## Miscrits Auto Bot

A GUI automation bot designed to assist with gameplay in Miscrits by performing automated actions such as attacking, capturing rare Miscrits, and managing interactions using image recognition and customizable settings.

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

