import tkinter as tk
from tkinter import filedialog, scrolledtext
from PIL import Image, ImageTk
import threading
import pyautogui
import time
import keyboard
import os

searchCD = 2

class MiscritBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Miscrit Bot GUI")
        self.root.configure(bg="#1e1e1e")

        self.running = False

        # Paths
        self.attack_path = tk.StringVar(value=r"D:\\Bot\\Attacks\\darkwishywashy.png")
        self.search_paths = []
        self.search_index = 0
        self.search_thumbnails = []
        self.miscrit_path = tk.StringVar(value=r"D:\\Bot\\Miscrits\\mymiscrit.png")
        self.rare_miscrit_path = tk.StringVar(value="")
        self.heal_path = tk.StringVar(value=r"D:\\Bot\\UI\\heal.png")
        self.yes_path = tk.StringVar(value=r"D:\\Bot\\UI\\yes.png")
        self.battle_complete_path = r"D:\\Bot\\UI\\continue.png"

        self.last_battle_CD = 0
        self.setup_ui()

    def setup_ui(self):
        style_opts = {"bg": "#2e2e2e", "fg": "white", "font": ("Segoe UI", 10)}
        button_opts = {"bg": "#3e3e3e", "fg": "white", "activebackground": "#5e5e5e", "bd": 0, "font": ("Segoe UI", 10)}

        self.log_area = scrolledtext.ScrolledText(self.root, height=10, width=60, state='disabled', bg="#121212", fg="white", insertbackground="white")
        self.log_area.grid(row=7, column=0, columnspan=4, pady=10, padx=10)

        self.create_image_selector("Attack Button", self.attack_path, 0, style_opts, button_opts)

        tk.Label(self.root, text="Search Objects:", **style_opts).grid(row=1, column=1, sticky='w')
        tk.Button(self.root, text="Select Images", command=self.select_multiple_search_images, **button_opts).grid(row=1, column=2)

        self.search_preview_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.search_preview_frame.grid(row=2, column=0, columnspan=4, pady=5)

        self.create_image_selector("My Miscrit", self.miscrit_path, 3, style_opts, button_opts)
        self.create_image_selector("Rare Miscrit", self.rare_miscrit_path, 4, style_opts, button_opts)

        tk.Button(self.root, text="Start Bot", command=self.start_bot, **button_opts).grid(row=5, column=1, pady=5)
        tk.Button(self.root, text="Stop Bot", command=self.stop_bot, **button_opts).grid(row=5, column=2, pady=5)

    def create_image_selector(self, label, path_var, row, style_opts, button_opts):
        tk.Label(self.root, text=label + ":", **style_opts).grid(row=row, column=1, sticky='w')
        entry = tk.Entry(self.root, textvariable=path_var, width=40, bg="#2a2a2a", fg="white", insertbackground="white")
        entry.grid(row=row, column=2)
        tk.Button(self.root, text="Select", command=lambda: self.select_image(path_var, row), **button_opts).grid(row=row, column=3)
        canvas = tk.Canvas(self.root, width=50, height=50, bg="#1e1e1e", highlightthickness=0)
        canvas.grid(row=row, column=0, padx=5)
        self.update_image_preview(canvas, path_var.get())
        setattr(self, f"canvas_{row}", canvas)

    def select_image(self, path_var, row):
        file_path = filedialog.askopenfilename(filetypes=[("PNG images", "*.png")])
        if file_path:
            path_var.set(file_path)
            canvas = getattr(self, f"canvas_{row}")
            self.update_image_preview(canvas, file_path)

    def select_multiple_search_images(self):
        files = filedialog.askopenfilenames(filetypes=[("PNG images", "*.png")])
        if files:
            self.search_paths = list(files)
            self.search_index = 0
            self.log(f"Selected {len(files)} search images.")
            self.display_search_previews()

    def display_search_previews(self):
        for widget in self.search_preview_frame.winfo_children():
            widget.destroy()

        self.search_thumbnails.clear()
        for img_path in self.search_paths:
            try:
                if os.path.exists(img_path):
                    img = Image.open(img_path).resize((50, 50), Image.Resampling.LANCZOS)
                    tk_img = ImageTk.PhotoImage(img)
                    label = tk.Label(self.search_preview_frame, image=tk_img, bg="#1e1e1e")
                    label.image = tk_img
                    label.pack(side='left', padx=2)
                    self.search_thumbnails.append(tk_img)
            except Exception as e:
                self.log(f"Error loading preview for {img_path}: {e}")

    def update_image_preview(self, canvas, image_path):
        try:
            if os.path.exists(image_path):
                img = Image.open(image_path).resize((50, 50), Image.Resampling.LANCZOS)
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
            threading.Thread(target=self.bot_loop, daemon=True).start()
            self.log("Bot started...")

    def stop_bot(self):
        self.running = False
        self.log("Stopping the bot...")

    def bot_loop(self):
        last_battle_time = time.time()

        while self.running:
            try:
                if keyboard.is_pressed('q'):
                    self.stop_bot()
                    break
            except Exception as e:
                self.log(f"Error checking keyboard input: {e}")

            try:
                if self.rare_miscrit_path.get():
                    rare_loc = pyautogui.locateOnScreen(self.rare_miscrit_path.get(), confidence=0.85)
                    if rare_loc:
                        self.log("RARE MISCRIT FOUND! Stopping bot to avoid killing it.")
                        self.running = False
                        break
            except Exception as e:
                self.log(f"Error checking rare miscrit: {e}")

            try:
                yes_loc = pyautogui.locateOnScreen(self.yes_path.get(), confidence=0.65)
                if yes_loc:
                    x, y = pyautogui.center(yes_loc)
                    pyautogui.click(x, y)
                    self.log("Yes button found and clicked")
            except Exception as e:
                self.log(f"{e}")

            if time.time() - last_battle_time > 60:
                self.log("More than 60 seconds since last battle, looking for heal button")
                try:
                    heal_loc = pyautogui.locateOnScreen(self.heal_path.get(), confidence=0.65)
                    if heal_loc:
                        x, y = pyautogui.center(heal_loc)
                        pyautogui.click(x, y)
                        self.log("Heal button found and clicked")
                    else:
                        self.log("Heal button not found, continuing...")
                except Exception as e:
                    self.log(f"Error during heal button detection: {e}")
                last_battle_time = time.time()

            try:
                attack_loc = pyautogui.locateOnScreen(self.attack_path.get(), confidence=0.65)
                if attack_loc:
                    x, y = pyautogui.center(attack_loc)
                    pyautogui.click(x, y)
                    self.log("Attack button found, clicking")
                    last_battle_time = time.time()
                    continue
            except Exception as e:
                self.log(f"Error during attack detection: {e}")

            try:
                complete_loc = pyautogui.locateOnScreen(self.battle_complete_path, confidence=0.65)
                if complete_loc:
                    x, y = pyautogui.center(complete_loc)
                    pyautogui.click(x, y)
                    self.log("Battle complete, clicking to continue")
                    time.sleep(1)
                    continue
            except Exception as e:
                self.log(f"Error during battle complete check: {e}")

            try:
                miscrit_loc = pyautogui.locateOnScreen(self.miscrit_path.get(), confidence=0.65)
                if miscrit_loc:
                    self.log("In battle, waiting for attack button")
                    continue
            except Exception as e:
                self.log(f"Error during in-battle detection: {e}")

            try:
                if not self.search_paths:
                    continue

                image_path = self.search_paths[self.search_index]
                self.search_index = (self.search_index + 1) % len(self.search_paths)

                search_loc = pyautogui.locateOnScreen(image_path, confidence=0.9)
                if search_loc:
                    x = search_loc.left + search_loc.width // 2
                    y = search_loc.top + search_loc.height - 35
                    self.log(f"Found bush using image: {os.path.basename(image_path)} at ({x}, {y})")
                    pyautogui.moveTo(x, y)

                    pyautogui.mouseDown()
                    self.log("Mouse held down")

                    for i in range(3):
                        pyautogui.mouseUp()
                        time.sleep(0.1)
                        pyautogui.mouseDown()
                        self.log(f"Click {i + 1}")

                    pyautogui.mouseUp()
                    self.log("Mouse released after triple click")

                    for i in range(searchCD, 0, -1):
                        self.log(f"Cooldown: {i} seconds remaining...")
                        time.sleep(1)

            except Exception as e:
                self.log(f"Error during bush detection: {e}")

            time.sleep(0.5)

if __name__ == "__main__":
    root = tk.Tk()
    app = MiscritBotGUI(root)
    root.mainloop()
