
                # Group 1: Attack Buttons
        self.create_image_selector("Attack Button", self.attack_path, 0, style_opts, button_opts)
        self.create_image_selector("Rare Attack Button", self.rare_attack_path, 1, style_opts, button_opts)

        # Group 2: Search Settings
        tk.Label(self.root, text="Search Objects:", **style_opts).grid(row=2, column=1, sticky='w')
        tk.Button(self.root, text="Select Images", command=self.select_multiple_search_images, **button_opts).grid(row=2, column=2)
        self.search_preview_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.search_preview_frame.grid(row=3, column=0, columnspan=4, pady=5)
        self.display_search_previews()

        # Group 3: Other Selectors
        self.create_image_selector("Rare Miscrit", self.rare_miscrit_path, 4, style_opts, button_opts)

        # Group 4: Settings
        tk.Label(self.root, text="Search Cooldown (s):", **style_opts).grid(row=5, column=1, sticky='w')
        tk.Spinbox(self.root, from_=1, to=100, textvariable=self.searchCD_var, width=5, bg="#2a2a2a", fg="white", font=("Segoe UI", 10), command=self.save_settings).grid(row=5, column=2, sticky='w')

        tk.Label(self.root, text="Capture Clicks:", **style_opts).grid(row=6, column=1, sticky='w')
        tk.Spinbox(self.root, from_=1, to=50, textvariable=self.capture_clicks_var, width=5, bg="#2a2a2a", fg="white", font=("Segoe UI", 10), command=self.save_settings).grid(row=6, column=2, sticky='w')

        tk.Label(self.root, text="Attack Click Window:", **style_opts).grid(row=7, column=1, sticky='w')
        tk.Spinbox(self.root, from_=1, to=50, textvariable=self.rare_attack_attempts_var, width=5, bg="#2a2a2a", fg="white", font=("Segoe UI", 10), command=self.save_settings).grid(row=7, column=2, sticky='w')

        # Group 5: Toggles
        self.auto_capture_toggle.grid(row=8, column=2, columnspan=2, pady=5)
        self.intervention_toggle.grid(row=8, column=0, columnspan=2, pady=5)

        # Group 6: Log + Controls
        tk.Button(self.root, text="Start Bot", command=self.start_bot, **button_opts).grid(row=9, column=0, pady=5)
        tk.Button(self.root, text="Stop Bot", command=self.stop_bot, **button_opts).grid(row=9, column=3, pady=5)
        self.log_area.grid(row=10, column=0, columnspan=4, pady=10, padx=10)

