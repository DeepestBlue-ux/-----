import random
import tkinter as tk


WIDTH = 720
HEIGHT = 520
PLAYER_SPEED = 8
PLAYER_FIRE_MS = 1000
ENEMY_SPAWN_MS = 3000
ENEMY_FIRE_MS = 5000
FRAME_MS = 16


class AlienInvasionGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Alien Invasion")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#07111f", highlightthickness=0)
        self.canvas.pack()

        self.keys = set()
        self.player = None
        self.player_bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.lives = 3
        self.score = 0
        self.game_over = False
        self.running = True

        self.hud_text = None
        self.message_text = None

        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)

        self.setup_scene()
        self.schedule_player_fire()
        self.schedule_enemy_spawn()
        self.schedule_enemy_fire()
        self.game_loop()

    def setup_scene(self):
        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#07111f", outline="")
        for _ in range(80):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.choice((1, 1, 2))
            self.canvas.create_oval(x, y, x + size, y + size, fill="#d7e8ff", outline="")

        px = WIDTH // 2
        py = HEIGHT - 70
        self.player = self.canvas.create_polygon(
            px,
            py - 28,
            px - 22,
            py + 24,
            px,
            py + 12,
            px + 22,
            py + 24,
            fill="#58d5ff",
            outline="#dff8ff",
            width=2,
        )
        self.hud_text = self.canvas.create_text(
            16,
            16,
            anchor="nw",
            fill="#f7fbff",
            font=("Segoe UI", 15, "bold"),
            text="Lives: 3   Score: 0",
        )
        self.message_text = self.canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            fill="#ffffff",
            font=("Segoe UI", 28, "bold"),
            text="",
        )

    def on_key_press(self, event):
        self.keys.add(event.keysym)
        if self.game_over and event.keysym.lower() == "r":
            self.restart()

    def on_key_release(self, event):
        self.keys.discard(event.keysym)

    def restart(self):
        self.canvas.delete("all")
        self.keys.clear()
        self.player_bullets.clear()
        self.enemy_bullets.clear()
        self.enemies.clear()
        self.lives = 3
        self.score = 0
        self.game_over = False
        self.running = True
        self.setup_scene()

    def schedule_player_fire(self):
        if not self.game_over:
            self.fire_player_bullet()
        self.root.after(PLAYER_FIRE_MS, self.schedule_player_fire)

    def schedule_enemy_spawn(self):
        if not self.game_over:
            self.spawn_enemy()
        self.root.after(ENEMY_SPAWN_MS, self.schedule_enemy_spawn)

    def schedule_enemy_fire(self):
        if not self.game_over:
            self.fire_enemy_bullets()
        self.root.after(ENEMY_FIRE_MS, self.schedule_enemy_fire)

    def fire_player_bullet(self):
        if not self.player:
            return
        x1, y1, x2, y2 = self.canvas.bbox(self.player)
        x = (x1 + x2) // 2
        bullet = self.canvas.create_rectangle(x - 3, y1 - 18, x + 3, y1, fill="#ffe066", outline="")
        self.player_bullets.append(bullet)

    def spawn_enemy(self):
        x = random.randint(40, WIDTH - 40)
        enemy = self.canvas.create_oval(x - 24, 28, x + 24, 76, fill="#9bff6a", outline="#e7ffd9", width=2)
        eye_left = self.canvas.create_oval(x - 12, 44, x - 5, 51, fill="#101820", outline="")
        eye_right = self.canvas.create_oval(x + 5, 44, x + 12, 51, fill="#101820", outline="")
        self.enemies.append({"body": enemy, "parts": [enemy, eye_left, eye_right], "vx": random.choice((-1.5, -1, 1, 1.5))})

    def fire_enemy_bullets(self):
        for enemy in list(self.enemies):
            bbox = self.canvas.bbox(enemy["body"])
            if not bbox:
                continue
            x1, y1, x2, y2 = bbox
            x = (x1 + x2) // 2
            bullet = self.canvas.create_oval(x - 5, y2, x + 5, y2 + 14, fill="#ff6178", outline="")
            self.enemy_bullets.append(bullet)

    def game_loop(self):
        if not self.game_over:
            self.move_player()
            self.move_player_bullets()
            self.move_enemies()
            self.move_enemy_bullets()
            self.check_collisions()
            self.update_hud()
        self.root.after(FRAME_MS, self.game_loop)

    def move_player(self):
        dx = 0
        dy = 0
        if "Left" in self.keys or "a" in self.keys or "A" in self.keys:
            dx -= PLAYER_SPEED
        if "Right" in self.keys or "d" in self.keys or "D" in self.keys:
            dx += PLAYER_SPEED
        if "Up" in self.keys or "w" in self.keys or "W" in self.keys:
            dy -= PLAYER_SPEED
        if "Down" in self.keys or "s" in self.keys or "S" in self.keys:
            dy += PLAYER_SPEED

        if dx == 0 and dy == 0:
            return

        x1, y1, x2, y2 = self.canvas.bbox(self.player)
        if x1 + dx < 0 or x2 + dx > WIDTH:
            dx = 0
        if y1 + dy < HEIGHT // 2 or y2 + dy > HEIGHT:
            dy = 0
        self.canvas.move(self.player, dx, dy)

    def move_player_bullets(self):
        for bullet in list(self.player_bullets):
            self.canvas.move(bullet, 0, -9)
            bbox = self.canvas.bbox(bullet)
            if not bbox or bbox[3] < 0:
                self.remove_item(bullet, self.player_bullets)

    def move_enemies(self):
        for enemy in list(self.enemies):
            bbox = self.canvas.bbox(enemy["body"])
            if not bbox:
                self.remove_enemy(enemy)
                continue
            x1, y1, x2, y2 = bbox
            vx = enemy["vx"]
            if x1 + vx < 0 or x2 + vx > WIDTH:
                enemy["vx"] *= -1
                vx = enemy["vx"]
            for part in enemy["parts"]:
                self.canvas.move(part, vx, 0.45)
            if y2 > HEIGHT:
                self.remove_enemy(enemy)

    def move_enemy_bullets(self):
        for bullet in list(self.enemy_bullets): 
            
            self.canvas.move(bullet, 0, 5)
            bbox = self.canvas.bbox(bullet)
            if not bbox or bbox[1] > HEIGHT:
                self.remove_item(bullet, self.enemy_bullets)

    def check_collisions(self):
        for bullet in list(self.player_bullets):
            bullet_box = self.canvas.bbox(bullet)
            if not bullet_box:
                continue
            for enemy in list(self.enemies):
                enemy_box = self.canvas.bbox(enemy["body"])
                if enemy_box and self.overlaps(bullet_box, enemy_box):
                    self.remove_item(bullet, self.player_bullets)
                    self.remove_enemy(enemy)
                    self.score += 1
                    break

        player_box = self.canvas.bbox(self.player)
        for bullet in list(self.enemy_bullets):
            bullet_box = self.canvas.bbox(bullet)
            if player_box and bullet_box and self.overlaps(player_box, bullet_box):
                self.remove_item(bullet, self.enemy_bullets)
                self.lives -= 1
                self.flash_player()
                if self.lives <= 0:
                    self.end_game()
                break

        player_box = self.canvas.bbox(self.player)
        for enemy in list(self.enemies):
            enemy_box = self.canvas.bbox(enemy["body"])
            if player_box and enemy_box and self.overlaps(player_box, enemy_box):
                self.remove_enemy(enemy)
                self.lives -= 1
                self.flash_player()
                if self.lives <= 0:
                    self.end_game()
                break

    def flash_player(self):
        self.canvas.itemconfig(self.player, fill="#ffffff")
        self.root.after(120, lambda: self.canvas.itemconfig(self.player, fill="#58d5ff") if self.player else None)

    def end_game(self):
        self.game_over = True
        self.canvas.itemconfig(
            self.message_text,
            text=f"GAME OVER\nScore: {self.score}\nPress R to restart",
            justify="center",
        )

    def update_hud(self):
        self.canvas.itemconfig(self.hud_text, text=f"Lives: {self.lives}   Score: {self.score}")

    def remove_enemy(self, enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)
        for part in enemy["parts"]:
            self.canvas.delete(part)

    def remove_item(self, item, collection):
        if item in collection:
            collection.remove(item)
        self.canvas.delete(item)

    @staticmethod
    def overlaps(a, b):
        return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]


if __name__ == "__main__":
    app = tk.Tk()
    AlienInvasionGame(app)
    app.mainloop()
    #游戏结束
print("end the game")