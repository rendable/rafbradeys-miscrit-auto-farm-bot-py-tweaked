                try:
                    search_loc = pyautogui.locateOnScreen(self.search_path.get(), confidence=0.95)
                    if search_loc is not None:
                        x = search_loc.left + search_loc.width // 2
                        y = search_loc.top + search_loc.height - 35 // 2
                        self.log(f"Bush found at: {x}, {y}")
                        pyautogui.moveTo(x, y)

                        pyautogui.mouseDown()
                        self.log("Mouse held down")

                        for i in range(3):
                            pyautogui.mouseUp()
                            time.sleep(0.1)  # short pause between up/down
                            pyautogui.mouseDown()
                            self.log(f"Click {i + 1}")

                        pyautogui.mouseUp()
                        self.log("Mouse released after triple click")

                        for i in range(searchCD, 0, -1):
                            self.log(f"Cooldown: {i} seconds remaining...")
                            time.sleep(1)
                except Exception as e:
                    self.log(f"Error during bush detection: {e}")