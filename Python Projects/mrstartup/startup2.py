import customtkinter as ctk
import random
import json
import os


SAVE_FILE = "startup_save.json"

class StartupSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Startup Simulator")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --- Game state ---
        self.money = 1000
        self.users = 100
        self.devs = 0
        self.growth_rate = 1.0  # users/sec
        self.tick_rate = 1000   # ms per tick

        # --- Layout Frames ---
        self.main_frame = ctk.CTkFrame(root, corner_radius=10)
        self.main_frame.pack(padx=15, pady=15, fill="both", expand=True)

        self.header = ctk.CTkLabel(
            self.main_frame,
            text="💼 Startup Headquarters",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        self.header.pack(pady=(5, 10))

        # --- Stats Dashboard ---
        self.stats_frame = ctk.CTkFrame(self.main_frame, corner_radius=12)
        self.stats_frame.pack(fill="x", padx=10, pady=10)

        self.money_label = ctk.CTkLabel(self.stats_frame, text="", font=("Arial", 16))
        self.users_label = ctk.CTkLabel(self.stats_frame, text="", font=("Arial", 16))
        self.devs_label = ctk.CTkLabel(self.stats_frame, text="", font=("Arial", 16))
        self.rate_label = ctk.CTkLabel(self.stats_frame, text="", font=("Arial", 16))

        for w in (self.money_label, self.users_label, self.devs_label, self.rate_label):
            w.pack(anchor="w", padx=10, pady=3)

        # --- Progress Bar for Users ---
        self.progress_label = ctk.CTkLabel(self.main_frame, text="User Growth Progress")
        self.progress_label.pack()
        self.user_progress = ctk.CTkProgressBar(self.main_frame, width=350)
        self.user_progress.pack(pady=5)
        self.user_progress.set(0.0)

        # --- Action Buttons (Right Side Panel) ---
        self.actions_frame = ctk.CTkFrame(self.main_frame)
        self.actions_frame.pack(pady=10)

        ctk.CTkButton(self.actions_frame, text="👨‍💻 Hire Dev ($500)", command=self.hire_dev).pack(pady=4)
        ctk.CTkButton(self.actions_frame, text="🚀 Launch Feature ($1000)", command=self.launch_feature).pack(pady=4)
        ctk.CTkButton(self.actions_frame, text="📢 Advertise ($800)", command=self.advertise).pack(pady=4)
        ctk.CTkButton(self.actions_frame, text="💾 Save Progress", command=self.save_game).pack(pady=4)
        ctk.CTkButton(self.actions_frame, text="📂 Load Game", command=self.load_game).pack(pady=4)

        # --- Event Log ---
        self.log_box = ctk.CTkTextbox(self.main_frame, height=150, width=420)
        self.log_box.pack(pady=10)
        self.log("Welcome to your startup office!")

        self.update_ui()
        self.root.after(self.tick_rate, self.game_tick)

    # -----------------------------
    def log(self, message):
        self.log_box.insert("end", f"> {message}\n")
        self.log_box.see("end")

    def update_ui(self):
        self.money_label.configure(text=f"💰 Money: ${int(self.money)}")
        self.users_label.configure(text=f"👥 Users: {int(self.users)}")
        self.devs_label.configure(text=f"👨‍💻 Devs: {self.devs}")
        self.rate_label.configure(text=f"⚡ Growth Rate: +{self.growth_rate:.1f}/s")

        progress = min(self.users / 1_000_000, 1.0)
        self.user_progress.set(progress)

    # -----------------------------
    def hire_dev(self):
        if self.money >= 500:
            self.money -= 500
            self.devs += 1
            self.growth_rate += 0.5
            self.log("You hired a new developer! 👨‍💻")
        else:
            self.log("Not enough money to hire a dev!")
        self.update_ui()

    def launch_feature(self):
        if self.money >= 1000:
            self.money -= 1000
            self.growth_rate *= 1.3
            self.log("Launched a shiny new feature ✨")
        else:
            self.log("You need $1000 to launch a feature.")
        self.update_ui()

    def advertise(self):
        if self.money >= 800:
            self.money -= 800
            gained = random.randint(200, 600)
            self.users += gained
            self.log(f"Ad campaign brought in {gained} users 📈")
        else:
            self.log("You can’t afford to advertise.")
        self.update_ui()

    # -----------------------------
    def random_event(self):
        events = [
            ("Server crash 💀", lambda: self.lose_users(0.2)),
            ("VC ghosted you 💸", lambda: self.lose_money(0.3)),
            ("Intern pushed to prod 🔥", lambda: self.lose_users(0.1)),
            ("Went viral on Reddit 🎉", lambda: self.gain_users(0.5)),
            
            
        ]
        if random.random() < 0.05:
            event, effect = random.choice(events)
            self.log(event)
            effect()

    def lose_users(self, frac):
        lost = int(self.users * frac)
        self.users -= lost
        self.log(f"Lost {lost} users!")

    def gain_users(self, frac):
        gained = int(self.users * frac)
        self.users += gained
        self.log(f"Gained {gained} new users!")

    def lose_money(self, frac):
        lost = int(self.money * frac)
        self.money -= lost
        self.log(f"Lost ${lost} in bad investments!")

    # -----------------------------
    def game_tick(self):
        self.users += self.growth_rate
        self.money += self.users * 0.05
        self.random_event()
        self.update_ui()

        if self.money <= 0:
            self.log("💀 You went bankrupt! Game over.")
            return
        if self.users >= 1_000_000:
            self.log("🏆 You reached 1M users! You win!")
            return

        self.root.after(self.tick_rate, self.game_tick)

    # -----------------------------
    def save_game(self):
        data = {
            "money": self.money,
            "users": self.users,
            "devs": self.devs,
            "growth_rate": self.growth_rate,
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
        self.log("Game saved! 💾")

    def load_game(self):
        if not os.path.exists(SAVE_FILE):
            self.log("No save file found.")
            return
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        self.money = data["money"]
        self.users = data["users"]
        self.devs = data["devs"]
        self.growth_rate = data["growth_rate"]
        self.update_ui()
        self.log("Game loaded! 📂")


# -----------------------------
if __name__ == "__main__":
    app = ctk.CTk()
    simulator = StartupSimulator(app)
    app.mainloop()
