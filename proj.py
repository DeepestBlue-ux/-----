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
    