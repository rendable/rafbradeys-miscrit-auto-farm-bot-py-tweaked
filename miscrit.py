import tkinter as tk
from notify_run import Notify
from tkinter import filedialog, scrolledtext, ttk
from PIL import Image, ImageTk
import threading
import pyautogui
import time
import keyboard
import os
import json


SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")
print("Current working directory:", os.getcwd())

searchTimes = 1 
rareMiscritGrayscale = True


class MiscritBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Miscrit Bot GUI")
        self.root.configure(bg="#1e1e1e")

        self.running = False
        self.attack_count = 0
        self.capture_attempts = 0

        self.searchCD_var = tk.IntVar(value=2)
        self.rare_attack_attempts_var = tk.IntVar(value=2)
        self.capture_clicks_var = tk.IntVar(value=2)
        self.auto_capture_mode = tk.StringVar(value="none")  # "none", "auto", "intervention"
        self.attack_path = tk.StringVar()
        self.miscrit_path = tk.StringVar()
        self.rare_miscrit_path = tk.StringVar()

        self.capture_button_path = tk.StringVar()
        self.confirm_capture_path = tk.StringVar()
        self.rare_attack_path = tk.StringVar()
        
        #constant button paths (not changeable by user), if some UI elements changed during an update, you may want to change these.
        # if you want to change these, edit the paths directly in the setting.json file :)
        self.okay2_path = tk.StringVar()
        self.okay_path = tk.StringVar()
        self.keep_path = tk.StringVar()
        self.heal_path = tk.StringVar()
        self.yes_path = tk.StringVar()

        self.search_paths = []
        self.search_index = 0
        self.search_thumbnails = []

        self.battle_complete_path = ""

        self.load_settings()
        self.last_battle_CD = 0
        self.setup_ui()
        
    def get_absolute_path(self, relative_path):
        """Convert relative path to absolute path based on script location"""
        if not relative_path:  # If path is empty
            return ""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, relative_path)
        
    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                try:
                    data = json.load(f)
                    self.attack_path.set(data.get("attack_path", ""))
                    self.miscrit_path.set(data.get("miscrit_path", ""))
                    self.rare_miscrit_path.set(data.get("rare_miscrit_path", ""))
                    self.heal_path.set(data.get("heal_path", ""))
                    self.yes_path.set(data.get("yes_path", ""))
                    self.battle_complete_path = data.get("battle_complete_path", "")
                    self.capture_button_path.set(data.get("capture_button_path", ""))
                    self.confirm_capture_path.set(data.get("confirm_capture_path", ""))
                    self.search_paths = data.get("search_paths", [])
                    self.searchCD_var.set(data.get("search_cooldown", 2))
                    self.rare_attack_attempts_var.set(data.get("rare_attacks", 2))
                    self.capture_clicks_var.set(data.get("capture_clicks", 2))
                    self.auto_capture_mode.set(data.get("auto_capture_mode", "none"))
                    self.rare_attack_path.set(data.get("rare_attack_path", ""))
                    self.okay2_path.set(data.get("okay2_path", ""))
                    self.okay_path.set(data.get("okay_path", ""))
                    self.keep_path.set(data.get("keep_path", ""))

                except json.JSONDecodeError:
                    print("Settings file is corrupted, loading defaults.")
        else:
            self.save_settings()

    def save_settings(self):
        print("Saving settings...")  

        data = {
            "attack_path": self.attack_path.get(),
            "miscrit_path": self.miscrit_path.get(),
            "rare_miscrit_path": self.rare_miscrit_path.get(),
            "heal_path": self.heal_path.get(),
            "yes_path": self.yes_path.get(),
            "battle_complete_path": self.battle_complete_path,
            "capture_button_path": self.capture_button_path.get(),
            "confirm_capture_path": self.confirm_capture_path.get(),
            "search_paths": self.search_paths,
            "search_cooldown": self.searchCD_var.get(),
            "rare_attacks": self.rare_attack_attempts_var.get(),
            "capture_clicks": self.capture_clicks_var.get(),
            "auto_capture_mode": self.auto_capture_mode.get(),
            "rare_attack_path": self.rare_attack_path.get(),
            "okay2_path": self.okay2_path.get(),
            "okay_path": self.okay_path.get(),
            "keep_path": self.keep_path.get(),
        }
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(data, f, indent=2)

    def setup_ui(self):
        style_opts = {"bg": "#2e2e2e", "fg": "white", "font": ("Segoe UI", 10)}
        button_opts = {"bg": "#3e3e3e", "fg": "white", "activebackground": "#5e5e5e", "bd": 0, "font": ("Segoe UI", 10)}

        control_frame = tk.Frame(self.root, bg="#1e1e1e")
        control_frame.grid(row=0, column=0, padx=10, pady=10)

        self.create_image_selector("Attack Button", self.attack_path, 0, style_opts, button_opts)
        self.create_image_selector("Spam While waiting for user:", self.rare_attack_path, 1, style_opts, button_opts)
        self.create_image_selector("Rare Miscrit", self.rare_miscrit_path, 2, style_opts, button_opts)

        tk.Label(self.root, text="Search Objects:", **style_opts).grid(row=3, column=1, sticky='w')
        tk.Button(self.root, text="Select Images", command=self.select_multiple_search_images, **button_opts).grid(row=3, column=2, sticky='w')

        self.search_preview_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.search_preview_frame.grid(row=4, column=0, columnspan=4, pady=5)
        self.display_search_previews()

        # Spinboxes
        tk.Label(self.root, text="Search Cooldown (s):", **style_opts).grid(row=5, column=1, sticky='w')
        tk.Spinbox(self.root, from_=1, to=100, textvariable=self.searchCD_var, width=5, bg="#2a2a2a", fg="white", font=("Segoe UI", 10), command=self.save_settings).grid(row=5, column=2, sticky='w')

        tk.Label(self.root, text="Capture Clicks:", **style_opts).grid(row=6, column=1, sticky='w')
        tk.Spinbox(self.root, from_=1, to=50, textvariable=self.capture_clicks_var, width=5, bg="#2a2a2a", fg="white", font=("Segoe UI", 10), command=self.save_settings).grid(row=6, column=2, sticky='w')

        tk.Label(self.root, text="Attack Click Window (5s per x):", **style_opts).grid(row=7, column=1, sticky='w')
        tk.Spinbox(self.root, from_=1, to=50, textvariable=self.rare_attack_attempts_var, width=5, bg="#2a2a2a", fg="white", font=("Segoe UI", 10), command=self.save_settings).grid(row=7, column=2, sticky='w')

        # Radio buttons for capture modes
        style = ttk.Style()
        style.configure('TRadiobutton', background='#2e2e2e', foreground='white')

        self.auto_capture_frame = tk.LabelFrame(self.root, text="Rare Miscrit Handling", bg="#2e2e2e", fg="white")
        self.auto_capture_frame.grid(row=8, column=0, columnspan=4, pady=5, padx=5, sticky="ew")

        ttk.Radiobutton(
            self.auto_capture_frame,
            text="No Auto Handling",
            variable=self.auto_capture_mode,
            value="none",
            command=self.save_settings,
            style='TRadiobutton'
        ).pack(side='left', padx=5)

        ttk.Radiobutton(
            self.auto_capture_frame,
            text="Auto Capture",
            variable=self.auto_capture_mode,
            value="auto",
            command=self.save_settings,
            style='TRadiobutton'
        ).pack(side='left', padx=5)

        ttk.Radiobutton(
            self.auto_capture_frame,
            text="Wait for Intervention",
            variable=self.auto_capture_mode,
            value="intervention",
            command=self.save_settings,
            style='TRadiobutton'
        ).pack(side='left', padx=5)

        # Bot control buttons
        tk.Button(self.root, text="Start Bot", command=self.start_bot, **button_opts).grid(row=9, column=0, pady=10)
        tk.Button(self.root, text="Stop Bot", command=self.stop_bot, **button_opts).grid(row=9, column=3, pady=10)

        # Log area
        self.log_area = scrolledtext.ScrolledText(self.root, height=10, width=60, state='disabled', bg="#121212", fg="white", insertbackground="white")
        self.log_area.grid(row=10, column=0, columnspan=4, pady=10, padx=10)

    def create_image_selector(self, label, path_var, row, style_opts, button_opts):
        def select_callback():
            file_path = filedialog.askopenfilename(filetypes=[("PNG images", "*.png")])
            if file_path:
                # Store relative path if the file is in the script directory or subdirectory
                try:
                    rel_path = os.path.relpath(file_path, os.path.dirname(os.path.abspath(__file__)))
                    if not rel_path.startswith('..'):  # Only use relative path if it's within project folder
                        path_var.set(rel_path)
                    else:
                        path_var.set(file_path)
                except ValueError:
                    path_var.set(file_path)
                
                canvas = getattr(self, f"canvas_{row}")
                self.update_image_preview(canvas, path_var.get())
                self.save_settings()

        tk.Label(self.root, text=label + ":", **style_opts).grid(row=row, column=1, sticky='w')
        entry = tk.Entry(self.root, textvariable=path_var, width=40, bg="#2a2a2a", fg="white", insertbackground="white")
        entry.grid(row=row, column=2)
        tk.Button(self.root, text="Select", command=select_callback, **button_opts).grid(row=row, column=3)
        canvas = tk.Canvas(self.root, width=50, height=50, bg="#1e1e1e", highlightthickness=0)
        canvas.grid(row=row, column=0, padx=5)
        self.update_image_preview(canvas, path_var.get())
        setattr(self, f"canvas_{row}", canvas)

    def select_multiple_search_images(self):
        files = filedialog.askopenfilenames(filetypes=[("PNG images", "*.png")])
        if files:
            self.search_paths = []
            for file_path in files:
                try:
                    rel_path = os.path.relpath(file_path, os.path.dirname(os.path.abspath(__file__)))
                    if not rel_path.startswith('..'):  # Only use relative path if it's within project folder
                        self.search_paths.append(rel_path)
                    else:
                        self.search_paths.append(file_path)
                except ValueError:
                    self.search_paths.append(file_path)
            
            self.search_index = 0
            self.display_search_previews()
            self.save_settings()
            self.log(f"Selected {len(files)} search images.")

    def display_search_previews(self):
        for widget in self.search_preview_frame.winfo_children():
            widget.destroy()
        self.search_thumbnails.clear()
        for img_path in self.search_paths:
            try:
                abs_path = self.get_absolute_path(img_path)
                if os.path.exists(abs_path):
                    img = Image.open(abs_path).resize((50, 50), Image.Resampling.LANCZOS)
                    tk_img = ImageTk.PhotoImage(img)
                    label = tk.Label(self.search_preview_frame, image=tk_img, bg="#1e1e1e")
                    label.image = tk_img
                    label.pack(side='left', padx=2)
                    self.search_thumbnails.append(tk_img)
            except Exception as e:
                self.log(f"Error loading preview for {img_path}: {e}")

    def update_image_preview(self, canvas, image_path):
        try:
            abs_path = self.get_absolute_path(image_path)
            if os.path.exists(abs_path):
                img = Image.open(abs_path).resize((50, 50), Image.Resampling.LANCZOS)
                tk_img = ImageTk.PhotoImage(img)
                canvas.image = tk_img
                canvas.create_image(0, 0, anchor='nw', image=tk_img)
        except Exception as e:
            self.log(f"Failed to load image: {e}")

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + '\n')
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def start_bot(self):
        if not self.running:
            self.running = True
            self.attack_count = 0
            self.capture_attempts = 0
            threading.Thread(target=self.bot_loop, daemon=True).start()
            self.log("Bot started...")

    def stop_bot(self):
        self.running = False
        self.log("Stopping the bot...")

    def handle_auto_capture(self):
        """Handle the auto-capture sequence using normal attacks"""
        max_attacks = self.rare_attack_attempts_var.get()
        
        # Perform normal attacks for the specified duration
        if self.attack_count < max_attacks:
            try:
                attack_path = self.get_absolute_path(self.attack_path.get())
                if attack_path and os.path.exists(attack_path):
                    attack_loc = pyautogui.locateOnScreen(attack_path, confidence=0.7, grayscale=False)
                    if attack_loc:
                        x, y = pyautogui.center(attack_loc)
                        pyautogui.click(x, y)
                        self.attack_count += 1
                        self.log(f"Attacked ({self.attack_count}/{max_attacks})")
                        time.sleep(5)  # Wait for attack animation
                        return True
            except Exception as e:
                self.log(f"Error attacking: {e}")
            return False
        
        # After attack window, attempt capture
        else:
            self.log("Attack window complete, attempting capture...")
            try:
                capture_img = self.get_absolute_path(self.capture_button_path.get())
                if capture_img and os.path.exists(capture_img):
                    capture_loc = pyautogui.locateOnScreen(capture_img, confidence=0.7, grayscale=False)
                    if capture_loc:
                        x, y = pyautogui.center(capture_loc)
                        for i in range(self.capture_clicks_var.get()):
                            pyautogui.click(x, y)
                            self.log(f"Clicked capture button ({i+1}/{self.capture_clicks_var.get()})")
                            time.sleep(1.2)

                        confirm_start = time.time()
                        while time.time() - confirm_start < 3 and self.running:
                            try:
                                confirm_img = self.get_absolute_path(self.confirm_capture_path.get())
                                if confirm_img and os.path.exists(confirm_img):
                                    confirm_loc = pyautogui.locateOnScreen(confirm_img, confidence=0.7, grayscale=False)
                                    if confirm_loc:
                                        x, y = pyautogui.center(confirm_loc)
                                        pyautogui.click(x, y)
                                        self.log("Capture confirmed!")
                                        self.attack_count = 0
                                        time.sleep(3)
                                        return True
                            except:
                                pass
                            time.sleep(0.3)

                        self.log("Couldn't find confirm button")
                        return False
            except Exception as e:
                self.log(f"Error during capture attempt: {e}")
            return False

    def handle_intervention_mode(self):
        """Handle the intervention mode with rare attacks"""
        try:
            attack_path = self.get_absolute_path(self.rare_attack_path.get())
            if attack_path and os.path.exists(attack_path):
                attack_loc = pyautogui.locateOnScreen(attack_path, confidence=0.7, grayscale=False)
                if attack_loc:
                    x, y = pyautogui.center(attack_loc)
                    pyautogui.click(x, y)
                    self.log("Used rare attack (waiting for intervention)")
                    time.sleep(1)
                    return True
        except Exception as e:
            self.log(f"Error with rare attack: {e}")
        return False

    def bot_loop(self):
        last_battle_time = time.time()

        while self.running:
            if keyboard.is_pressed('q'):
                self.stop_bot()
                break

            try:
                yes_path = self.get_absolute_path(self.yes_path.get())
                if yes_path:
                    yes_loc = pyautogui.locateOnScreen(yes_path, confidence=0.65, grayscale=False)
                    if yes_loc:
                        x, y = pyautogui.center(yes_loc)
                        pyautogui.click(x, y)
                        self.log("Yes button found and clicked")
                        time.sleep(1)
            except: pass
            
            try:
                okay_path = self.get_absolute_path(self.okay_path.get())
                if okay_path:
                    okay_loc = pyautogui.locateOnScreen(okay_path, confidence=0.65, grayscale=False)
                    if okay_loc:
                        x, y = pyautogui.center(okay_loc)
                        pyautogui.click(x, y)
                        self.log("Okay button found and clicked")
                        time.sleep(1)
            except: pass
            
            try: 
                okay2_path = self.get_absolute_path(self.okay2_path.get())
                if okay2_path:
                    okay2_loc = pyautogui.locateOnScreen(okay2_path, confidence=0.65, grayscale=False)
                    if okay2_loc:
                        x, y = pyautogui.center(okay2_loc)
                        pyautogui.click(x, y)
                        self.log("Okay2 button found and clicked")
                        time.sleep(1)
            except: pass
            
            try:
                keep_path = self.get_absolute_path(self.keep_path.get())
                if keep_path:
                    keep_loc = pyautogui.locateOnScreen(keep_path, confidence=0.65, grayscale=False)
                    if keep_loc:
                        x, y = pyautogui.center(keep_loc)
                        pyautogui.click(x, y)
                        self.log("Keep button found and clicked")
                        time.sleep(1)
            except: pass

            if time.time() - last_battle_time > 60:
                try:
                    heal_path = self.get_absolute_path(self.heal_path.get())
                    if heal_path:
                        heal_loc = pyautogui.locateOnScreen(heal_path, confidence=0.65, grayscale=False)
                        if heal_loc:
                            x, y = pyautogui.center(heal_loc)
                            pyautogui.click(x, y)
                            self.log("Heal button found and clicked")
                            time.sleep(1)
                except: pass
                last_battle_time = time.time()
            

            try:
                rare_path = self.get_absolute_path(self.rare_miscrit_path.get())
                if rare_path and os.path.exists(rare_path):
                    rare_loc = pyautogui.locateOnScreen(rare_path, confidence=0.75, grayscale=False)
                    if rare_loc:
                        self.log("Rare miscrit detected - handling...")
                        notify = Notify()
                        notify.send("Rare miscrit detected!")
                        
                        if self.auto_capture_mode.get() == "intervention":
                            self.log("Waiting for user intervention (15 seconds)...")
                            start_time = time.time()
                            while time.time() - start_time < 15 and self.running:
                                remaining = 15 - int(time.time() - start_time)
                                self.log(f"Waiting for intervention... {remaining}s remaining (press 'q' to stop)")
                                time.sleep(1)
                            
                            # After waiting, start spamming rare attacks
                            self.log("Starting safe attack loop until user stops...")
                            while self.running:
                                self.handle_intervention_mode()
                                time.sleep(1)
                        elif self.auto_capture_mode.get() == "auto":
                            self.log("Handling rare miscrit with auto-capture")
                            notify.send("Rare miscrit detected, Auto Capture in 10 seconds!")
                            time.sleep(10)  # Wait before starting auto capture
                            while self.running and self.handle_auto_capture():
                                pass
                            self.attack_count = 0  # Reset counter after capture attempt
            except: pass

            try:
                attack_path = self.get_absolute_path(self.attack_path.get())
                if attack_path:
                    attack_loc = pyautogui.locateOnScreen(attack_path, confidence=0.65, grayscale=False)
                    if attack_loc:
                        x, y = pyautogui.center(attack_loc)
                        pyautogui.click(x, y)
                        self.log("Attack button clicked")
                        time.sleep(1.5)
                        last_battle_time = time.time()
            except: pass

            try:
                complete_path = self.get_absolute_path(self.battle_complete_path)
                if complete_path:
                    complete_loc = pyautogui.locateOnScreen(complete_path, confidence=0.65, grayscale=False)
                    if complete_loc:
                        x, y = pyautogui.center(complete_loc)
                        pyautogui.click(x, y)
                        self.log("Battle complete, clicking to continue")
                        time.sleep(1)
            except: pass

            try:
                miscrit_path = self.get_absolute_path(self.miscrit_path.get())
                if miscrit_path:
                    miscrit_loc = pyautogui.locateOnScreen(miscrit_path, confidence=0.65, grayscale=False)
                    if miscrit_loc:
                        self.log("In battle, waiting for attack button")
                        time.sleep(1)
                        continue
            except: pass

            try:
                if not self.search_paths:
                    time.sleep(1)
                    continue

                image_path = self.search_paths[self.search_index]
                abs_image_path = self.get_absolute_path(image_path)
                self.search_index = (self.search_index + 1) % len(self.search_paths)

                if abs_image_path:
                    search_loc = pyautogui.locateOnScreen(abs_image_path, confidence=0.8, grayscale=False)
                    if search_loc:
                        x = search_loc.left + search_loc.width - 25
                        y = search_loc.top + search_loc.height - 35
                        self.log(f"Found bush at ({x}, {y})")
                        pyautogui.moveTo(x, y)
                        pyautogui.mouseDown()
                        for i in range(searchTimes):
                            pyautogui.mouseUp()
                            time.sleep(0.1)
                            pyautogui.mouseDown()
                        pyautogui.mouseUp()

                        for i in range(self.searchCD_var.get(), 0, -1):
                            if not self.running: break
                            self.log(f"Cooldown: {i} seconds remaining...")
                            time.sleep(1)
            except: pass
            time.sleep(0.5)

if __name__ == "__main__":
    root = tk.Tk()
    app = MiscritBotGUI(root)
    root.mainloop()