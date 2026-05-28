import pygame
import random
import sys
import time

# ── 初始化 ──────────────────────────────────────────────────────────────────
pygame.init()
pygame.display.set_caption("🚀 星际防卫 · Space Defender")

WIDTH, HEIGHT = 800, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ── 颜色 ─────────────────────────────────────────────────────────────────────
BLACK       = (0,   0,   0  )
WHITE       = (255, 255, 255)
CYAN        = (0,   220, 255)
ORANGE      = (255, 140, 0  )
RED         = (255, 50,  50 )
GREEN       = (50,  255, 100)
YELLOW      = (255, 230, 0  )
DARK_BLUE   = (5,   10,  30 )
PURPLE      = (160, 0,   255)
GRAY        = (120, 120, 120)
LIGHT_GRAY  = (200, 200, 200)

# ── 字体 ─────────────────────────────────────────────────────────────────────
font_big   = pygame.font.SysFont("Arial", 48, bold=True)
font_med   = pygame.font.SysFont("Arial", 28, bold=True)
font_small = pygame.font.SysFont("Arial", 20)

# ── 星星背景 ──────────────────────────────────────────────────────────────────
STARS = [(random.randint(0, WIDTH), random.randint(0, HEIGHT),
          random.choice([1, 1, 1, 2, 2, 3])) for _ in range(200)]

def draw_stars():
    for x, y, size in STARS:
        brightness = random.randint(180, 255)
        c = (brightness, brightness, brightness)
        pygame.draw.circle(screen, c, (x, y), size)

# ── 粒子特效 ──────────────────────────────────────────────────────────────────
particles = []

def spawn_explosion(x, y, color, count=18):
    for _ in range(count):
        angle = random.uniform(0, 6.28)
        speed = random.uniform(1.5, 5)
        particles.append({
            "x": x, "y": y,
            "vx": speed * __import__("math").cos(angle),
            "vy": speed * __import__("math").sin(angle),
            "life": random.randint(20, 45),
            "color": color,
            "size": random.randint(2, 5)
        })

def update_particles():
    for p in particles[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["life"] -= 1
        p["vy"] += 0.08  # 重力感
        if p["life"] <= 0:
            particles.remove(p)

def draw_particles():
    for p in particles:
        alpha = max(0, int(255 * p["life"] / 45))
        c = tuple(min(255, v) for v in p["color"])
        s = p["size"]
        pygame.draw.circle(screen, c, (int(p["x"]), int(p["y"])), s)

# ── 飞船绘制 ──────────────────────────────────────────────────────────────────
def draw_player_ship(surface, x, y, w=44, h=54):
    """绘制玩家飞船（朝上）"""
    cx = x + w // 2
    # 主机身
    body = [(cx, y), (cx - w//2, y + h - 10), (cx - w//4, y + h), (cx + w//4, y + h), (cx + w//2, y + h - 10)]
    pygame.draw.polygon(surface, CYAN, body)
    pygame.draw.polygon(surface, WHITE, body, 2)
    # 驾驶舱
    cockpit = [(cx, y + 8), (cx - 10, y + 26), (cx + 10, y + 26)]
    pygame.draw.polygon(surface, (30, 180, 220), cockpit)
    # 发动机喷焰（随机闪烁）
    if random.random() > 0.4:
        flame_h = random.randint(10, 22)
        flame_pts = [(cx - 10, y + h), (cx + 10, y + h), (cx, y + h + flame_h)]
        pygame.draw.polygon(surface, ORANGE, flame_pts)
        inner_pts = [(cx - 5, y + h), (cx + 5, y + h), (cx, y + h + flame_h - 6)]
        pygame.draw.polygon(surface, YELLOW, inner_pts)

def draw_enemy_ship(surface, x, y, color, w=40, h=30):
    """绘制外星人飞船（朝下）"""
    cx = x + w // 2
    cy = y + h // 2
    # 碟形
    pygame.draw.ellipse(surface, color, (x + 4, cy - 6, w - 8, 14))
    # 穹顶
    dome_rect = pygame.Rect(cx - 10, y, 20, 16)
    pygame.draw.ellipse(surface, (200, 255, 200), dome_rect)
    pygame.draw.ellipse(surface, WHITE, dome_rect, 1)
    # 光束指示灯
    pygame.draw.circle(surface, (255, 50, 50), (cx - 10, cy + 2), 3)
    pygame.draw.circle(surface, (255, 50, 50), (cx + 10, cy + 2), 3)
    pygame.draw.circle(surface, YELLOW, (cx, cy + 2), 3)

# ── 游戏对象 ──────────────────────────────────────────────────────────────────
class Player:
    W, H = 44, 54
    SPEED = 5

    def __init__(self):
        self.x = WIDTH // 2 - self.W // 2
        self.y = HEIGHT - self.H - 20
        self.lives = 3
        self.bullets = []
        self.last_shot = 0
        self.invincible = 0   # 受伤后无敌帧数
        self.score = 0

    @property
    def rect(self):
        return pygame.Rect(self.x + 6, self.y + 10, self.W - 12, self.H - 14)

    def move(self, keys):
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: self.x = max(0, self.x - self.SPEED)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.x = min(WIDTH - self.W, self.x + self.SPEED)
        if keys[pygame.K_UP]    or keys[pygame.K_w]: self.y = max(0, self.y - self.SPEED)
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: self.y = min(HEIGHT - self.H, self.y + self.SPEED)

    def try_shoot(self, now):
        if now - self.last_shot >= 1.0:
            cx = self.x + self.W // 2
            self.bullets.append({"x": cx, "y": self.y, "vy": -10})
            self.last_shot = now

    def update_bullets(self):
        self.bullets = [b for b in self.bullets if b["y"] > -10]
        for b in self.bullets:
            b["y"] += b["vy"]

    def draw(self, surface):
        # 无敌时闪烁
        if self.invincible > 0 and (self.invincible // 4) % 2 == 0:
            self.invincible -= 1
            return
        if self.invincible > 0:
            self.invincible -= 1
        draw_player_ship(surface, self.x, self.y, self.W, self.H)
        for b in self.bullets:
            # 子弹发光效果
            pygame.draw.rect(surface, (150, 255, 255), (b["x"] - 3, b["y"] - 8, 6, 16))
            pygame.draw.rect(surface, WHITE,            (b["x"] - 2, b["y"] - 8, 4, 16))

    def take_hit(self):
        if self.invincible > 0:
            return False
        self.lives -= 1
        self.invincible = 90
        spawn_explosion(self.x + self.W//2, self.y + self.H//2, RED, 30)
        return True


class Enemy:
    W, H = 40, 30
    COLORS = [(80, 220, 80), (220, 80, 220), (80, 180, 220), (220, 160, 40)]

    def __init__(self):
        self.x = random.randint(10, WIDTH - self.W - 10)
        self.y = random.randint(-80, -self.H)
        self.vy = random.uniform(0.8, 2.2)
        self.vx = random.uniform(-1.0, 1.0)
        self.color = random.choice(self.COLORS)
        self.last_shot = time.time() + random.uniform(0, 3)

    @property
    def rect(self):
        return pygame.Rect(self.x + 4, self.y + 6, self.W - 8, self.H - 8)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 or self.x > WIDTH - self.W:
            self.vx *= -1

    def try_shoot(self, now):
        if now - self.last_shot >= 5.0:
            self.last_shot = now
            cx = self.x + self.W // 2
            return {"x": cx, "y": self.y + self.H, "vy": 5}
        return None

    def draw(self, surface):
        draw_enemy_ship(surface, self.x, self.y, self.color, self.W, self.H)


# ── HUD ───────────────────────────────────────────────────────────────────────
def draw_hud(player, elapsed):
    # 顶部半透明栏
    bar = pygame.Surface((WIDTH, 44), pygame.SRCALPHA)
    bar.fill((0, 0, 20, 160))
    screen.blit(bar, (0, 0))

    # 生命值（心形图标）
    for i in range(3):
        color = RED if i < player.lives else GRAY
        hx = 18 + i * 36
        pygame.draw.circle(screen, color, (hx,     16), 8)
        pygame.draw.circle(screen, color, (hx + 14, 16), 8)
        pts = [(hx - 8, 20), (hx + 22, 20), (hx + 7, 34)]
        pygame.draw.polygon(screen, color, pts)

    # 分数
    score_txt = font_med.render(f"SCORE  {player.score:06d}", True, CYAN)
    screen.blit(score_txt, (WIDTH // 2 - score_txt.get_width() // 2, 8))

    # 计时
    time_txt = font_small.render(f"TIME  {int(elapsed)}s", True, LIGHT_GRAY)
    screen.blit(time_txt, (WIDTH - time_txt.get_width() - 14, 12))

def draw_controls():
    hints = ["WASD / ←↑↓→ 移动", "自动每秒射击"]
    y = HEIGHT - 48
    for h in hints:
        t = font_small.render(h, True, (100, 100, 140))
        screen.blit(t, (10, y))
        y += 22


# ── 屏幕：主菜单 ──────────────────────────────────────────────────────────────
def screen_start():
    while True:
        screen.fill(DARK_BLUE)
        draw_stars()

        title = font_big.render("🚀 SPACE DEFENDER", True, CYAN)
        sub   = font_med.render("星际防卫", True, YELLOW)
        hint  = font_small.render("按  ENTER  或  空格  开始游戏", True, LIGHT_GRAY)
        quit_hint = font_small.render("按 Q / ESC 退出", True, GRAY)

        screen.blit(title, (WIDTH//2 - title.get_width()//2, 180))
        screen.blit(sub,   (WIDTH//2 - sub.get_width()//2,   244))
        screen.blit(hint,  (WIDTH//2 - hint.get_width()//2,  340))
        screen.blit(quit_hint, (WIDTH//2 - quit_hint.get_width()//2, 374))

        rules = [
            "• WASD 或方向键移动飞船",
            "• 每秒自动发射一颗炮弹",
            "• 击落外星人得 100 分",
            "• 外星人每 5 秒射击一次",
            "• 共 3 条命，全部丢失游戏结束",
        ]
        for i, r in enumerate(rules):
            t = font_small.render(r, True, (160, 200, 180))
            screen.blit(t, (WIDTH//2 - 180, 430 + i * 26))

        pygame.display.flip()
        clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_RETURN, pygame.K_SPACE): return
                if ev.key in (pygame.K_q, pygame.K_ESCAPE): pygame.quit(); sys.exit()


# ── 屏幕：游戏结束 ────────────────────────────────────────────────────────────
def screen_game_over(score, elapsed):
    t0 = time.time()
    while True:
        screen.fill(DARK_BLUE)
        draw_stars()

        over  = font_big.render("GAME  OVER", True, RED)
        sc    = font_med.render(f"最终得分：{score:06d}", True, YELLOW)
        tm    = font_med.render(f"存活时间：{int(elapsed)} 秒", True, CYAN)
        again = font_small.render("按 R 重新开始    按 Q/ESC 退出", True, LIGHT_GRAY)

        screen.blit(over,  (WIDTH//2 - over.get_width()//2,  200))
        screen.blit(sc,    (WIDTH//2 - sc.get_width()//2,    290))
        screen.blit(tm,    (WIDTH//2 - tm.get_width()//2,    336))
        screen.blit(again, (WIDTH//2 - again.get_width()//2, 420))

        pygame.display.flip()
        clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r: return True
                if ev.key in (pygame.K_q, pygame.K_ESCAPE): return False


# ── 主游戏循环 ────────────────────────────────────────────────────────────────
def run_game():
    player = Player()
    enemies = []
    enemy_bullets = []  # {"x","y","vy"}
    last_enemy_spawn = time.time()
    start_time = time.time()

    while True:
        now = time.time()
        elapsed = now - start_time
        dt = clock.tick(60) / 1000.0

        # ── 事件 ──
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key in (pygame.K_q, pygame.K_ESCAPE): pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()

        # ── 逻辑 ──
        player.move(keys)
        player.try_shoot(now)
        player.update_bullets()

        # 每3秒生成一个外星人
        if now - last_enemy_spawn >= 3.0:
            enemies.append(Enemy())
            last_enemy_spawn = now

        # 外星人移动 & 射击
        for e in enemies:
            e.update()
            shot = e.try_shoot(now)
            if shot:
                enemy_bullets.append(shot)

        # 移除飞出屏幕的外星人
        enemies = [e for e in enemies if e.y < HEIGHT + 60]

        # 外星人子弹移动
        for b in enemy_bullets:
            b["y"] += b["vy"]
        enemy_bullets = [b for b in enemy_bullets if b["y"] < HEIGHT + 20]

        # ── 碰撞：玩家子弹 vs 外星人 ──
        for pb in player.bullets[:]:
            pb_rect = pygame.Rect(pb["x"] - 4, pb["y"] - 10, 8, 20)
            for e in enemies[:]:
                if pb_rect.colliderect(e.rect):
                    spawn_explosion(e.x + e.W//2, e.y + e.H//2, e.color, 22)
                    enemies.remove(e)
                    player.bullets.remove(pb)
                    player.score += 100
                    break

        # ── 碰撞：外星人子弹 vs 玩家 ──
        for eb in enemy_bullets[:]:
            eb_rect = pygame.Rect(eb["x"] - 4, eb["y"] - 4, 8, 8)
            if eb_rect.colliderect(player.rect):
                if player.take_hit():
                    enemy_bullets.remove(eb)

        # ── 碰撞：外星人 vs 玩家直接接触 ──
        for e in enemies[:]:
            if e.rect.colliderect(player.rect):
                if player.take_hit():
                    spawn_explosion(e.x + e.W//2, e.y + e.H//2, e.color, 20)
                    enemies.remove(e)
                    break

        update_particles()

        # ── 绘制 ──
        screen.fill(DARK_BLUE)
        draw_stars()
        draw_particles()

        for e in enemies:
            e.draw(screen)

        # 外星人子弹
        for b in enemy_bullets:
            pygame.draw.circle(screen, (50, 255, 50), (int(b["x"]), int(b["y"])), 5)
            pygame.draw.circle(screen, WHITE,          (int(b["x"]), int(b["y"])), 3)

        player.draw(screen)
        draw_hud(player, elapsed)
        draw_controls()

        pygame.display.flip()

        # ── 死亡判断 ──
        if player.lives <= 0:
            return player.score, elapsed


# ── 入口 ──────────────────────────────────────────────────────────────────────
def main():
    screen_start()
    while True:
        score, elapsed = run_game()
        play_again = screen_game_over(score, elapsed)
        if not play_again:
            break
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()