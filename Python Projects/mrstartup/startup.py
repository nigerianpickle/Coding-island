import tkinter as tk
import random
import json
import os

SAVE_FILE = "startup_save.json"

class StartupSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Startup Simulator")

        # --- Game state ---
        self.money = 1000
        self.users = 100
        self.devs = 0
        self.growth_rate = 1.0  # users/sec
        self.tick_rate = 1000   # ms per tick

        # --- GUI Labels ---
        self.money_label = tk.Label(root, text="")
        self.users_label = tk.Label(root, text="")
        self.devs_label = tk.Label(root, text="")
        self.rate_label = tk.Label(root, text="")
        for w in (self.money_label, self.users_label, self.devs_label, self.rate_label):
            w.pack()

        # --- Buttons ---
        tk.Button(root, text="👨‍💻 Hire Dev ($500)", command=self.hire_dev).pack(pady=3)
        tk.Button(root, text="🚀 Launch Feature ($1000)", command=self.launch_feature).pack(pady=3)
        tk.Button(root, text="📢 Advertise ($800)", command=self.advertise).pack(pady=3)
        tk.Button(root, text="💾 Save Progress", command=self.save_game).pack(pady=3)
        tk.Button(root, text="📂 Load Game", command=self.load_game).pack(pady=3)

        # --- Event Log ---
        self.log_box = tk.Text(root, height=8, width=40)
        self.log_box.pack(pady=5)
        self.log("Welcome to Startup Simulator!")

        self.update_ui()
        self.root.after(self.tick_rate, self.game_tick)

    # -----------------------------
    def log(self, message):
        self.log_box.insert(tk.END, f"> {message}\n")
        self.log_box.see(tk.END)

    def update_ui(self):
        self.money_label.config(text=f"💰 Money: ${int(self.money)}")
        self.users_label.config(text=f"👥 Users: {int(self.users)}")
        self.devs_label.config(text=f"👨‍💻 Devs: {self.devs}")
        self.rate_label.config(text=f"⚡ Growth Rate: +{self.growth_rate:.1f}/s")

    # -----------------------------
    def hire_dev(self):
        if self.money >= 500:
            self.money -= 500
            self.devs += 1
            self.growth_rate += 0.5
            self.log("You hired a new developer!")
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
        if random.random() < 0.05:  # 5% chance per tick
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
        self.log("Game saved!")

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
        self.log("Game loaded!")

# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = StartupSimulator(root)
    root.mainloop()
