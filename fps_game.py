"""
┌─────────────────────────────────────────────────────────┐
│   SECTOR ZERO  ·  First-Person Shooter                  │
│   Python + Pygame  ·  Raycasting Engine                 │
│   Controls: WASD移动  ←→旋转  鼠标左键/空格 射击          │
└─────────────────────────────────────────────────────────┘
"""

import pygame, math, sys, random, time

# ═══════════════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════════════
W, H        = 960, 600
HALF_H      = H // 2
FOV         = math.pi / 3          # 60°
HALF_FOV    = FOV / 2
NUM_RAYS    = 240                   # cast per frame
MAX_DEPTH   = 30
CELL        = 64                    # world tile size (logical)
MOVE_SPEED  = 2.8
ROT_SPEED   = 0.045
MINIMAP_S   = 6                     # pixels per cell in minimap

FPS         = 60
SHOOT_CD    = 1.0                   # seconds between shots
AI_SHOOT_CD = 1.0
HIT_CHANCE  = 0.30                  # enemy accuracy

# ── Colours ──────────────────────────────────────────────
C_SKY      = (18,  24,  42 )
C_FLOOR    = (28,  28,  34 )
C_WALL_L   = (90,  110, 130)        # light wall
C_WALL_D   = (55,  68,  80 )        # dark wall (E/W face)
C_ACCENT   = (0,   220, 200)
C_RED      = (220, 50,  50 )
C_YELLOW   = (240, 200, 60 )
C_WHITE    = (255, 255, 255)
C_GRAY     = (120, 120, 120)
C_BLACK    = (0,   0,   0  )
C_HURT     = (180, 0,   0,  90)
C_HIT_FX   = (255, 80,  0  )
C_ENEMY_C  = (220, 80,  60 )        # enemy sprite centre

# ═══════════════════════════════════════════════════════════
#  MAP  (0=open, 1=wall)  — 16×16, symmetric
# ═══════════════════════════════════════════════════════════
RAW_MAP = [
    "1111111111111111",
    "1000000110000001",
    "1011000110001101",
    "1010001001000101",
    "1000110000110001",
    "1001000000001001",
    "1100011001100011",  # ← corrected: was "110001100011001" (15 chars)
    "1000000110000001",
    "1000000110000001",
    "1100011001100011",
    "1001000000001001",
    "1000110000110001",
    "1010001001000101",
    "1011000110001101",
    "1000000110000001",
    "1111111111111111",
]

MAP_H = len(RAW_MAP)
MAP_W = len(RAW_MAP[0])

def cell(mx, my):
    if 0 <= my < MAP_H and 0 <= mx < MAP_W:
        return RAW_MAP[my][mx] == "1"
    return True

# Symmetric spawn pairs (player, enemy) in cell coords
SPAWN_PAIRS = [
    ((1.5, 1.5),  (14.5, 14.5)),
    ((1.5, 14.5), (14.5, 1.5)),
    ((3.5, 3.5),  (12.5, 12.5)),
    ((3.5, 12.5), (12.5, 3.5)),
]

# ═══════════════════════════════════════════════════════════
#  RAYCASTER
# ═══════════════════════════════════════════════════════════
def cast_ray(px, py, angle):
    """DDA ray cast. Returns (dist, is_vertical_hit)."""
    ra = angle % (2 * math.pi)
    sin_a = math.sin(ra); cos_a = math.cos(ra)

    # ── Horizontal grid hits ──
    h_dist = 1e9
    if sin_a != 0:
        step_y = -1 if sin_a > 0 else 1
        ry = (math.floor(py) if sin_a > 0 else math.ceil(py) - 1e-6)
        rx = px + (py - ry) * cos_a / (sin_a if sin_a != 0 else 1e-9)
        dx = -cos_a / sin_a * step_y
        for _ in range(MAX_DEPTH):
            mx = int(rx); my = int(ry)
            if cell(mx, my): h_dist = math.hypot(rx - px, ry - py); break
            rx += dx; ry += step_y

    # ── Vertical grid hits ──
    v_dist = 1e9
    if cos_a != 0:
        step_x = 1 if cos_a > 0 else -1
        rx = (math.ceil(px) if cos_a > 0 else math.floor(px))
        ry = py - (rx - px) * sin_a / (cos_a if cos_a != 0 else 1e-9)
        dy = sin_a / cos_a * step_x
        for _ in range(MAX_DEPTH):
            mx = int(rx - (1 if step_x < 0 else 0)); my = int(ry)
            if cell(mx, my): v_dist = math.hypot(rx - px, ry - py); break
            rx += step_x; ry += dy

    if v_dist < h_dist:
        return v_dist, True
    return h_dist, False

# ═══════════════════════════════════════════════════════════
#  ENTITY BASE
# ═══════════════════════════════════════════════════════════
class Entity:
    def __init__(self, x, y, angle=0.0, hp=3):
        self.x = x; self.y = y
        self.angle = angle % (2 * math.pi)
        self.hp  = hp
        self.max_hp = hp
        self.last_shot = 0.0
        self.alive = True
        self.shoot_cd = SHOOT_CD

    def move(self, dx, dy):
        nx = self.x + dx; ny = self.y + dy
        if not cell(int(nx), int(self.y)): self.x = nx
        if not cell(int(self.x), int(ny)): self.y = ny

    def try_shoot(self, now):
        if now - self.last_shot >= self.shoot_cd:
            self.last_shot = now
            return True
        return False

    def take_hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False
            return True
        return False

# ═══════════════════════════════════════════════════════════
#  AI ENEMY
# ═══════════════════════════════════════════════════════════
class Enemy(Entity):
    PATROL_SPEED = 1.2
    CHASE_SPEED  = 2.0
    SIGHT_RANGE  = 10.0
    SHOOT_RANGE  = 8.0

    def __init__(self, x, y):
        super().__init__(x, y, random.uniform(0, 2*math.pi), hp=3)
        self.shoot_cd = AI_SHOOT_CD
        self.state    = "patrol"
        self.patrol_timer = 0.0
        self.patrol_dir   = random.uniform(0, 2*math.pi)
        # Patrol waypoints: random wander when nothing found

    def can_see(self, px, py):
        """Line-of-sight check via short ray."""
        dx = px - self.x; dy = py - self.y
        dist = math.hypot(dx, dy)
        if dist > self.SIGHT_RANGE: return False, dist
        angle = math.atan2(dy, dx)
        # Check if sight is blocked
        steps = int(dist * 4)
        for i in range(1, steps):
            t = i / steps
            rx = self.x + dx * t; ry = self.y + dy * t
            if cell(int(rx), int(ry)): return False, dist
        return True, dist

    def update(self, px, py, now, dt):
        if not self.alive: return None

        visible, dist = self.can_see(px, py)
        shot_event = None

        if visible:
            self.state = "chase"
            # Face player
            target_a = math.atan2(py - self.y, px - self.x)
            diff = (target_a - self.angle + math.pi) % (2*math.pi) - math.pi
            self.angle += max(-2.5*dt, min(2.5*dt, diff))

            # Move toward player if far
            if dist > 2.5:
                self.move(math.cos(self.angle) * self.CHASE_SPEED * dt,
                          math.sin(self.angle) * self.CHASE_SPEED * dt)

            # Shoot
            if dist <= self.SHOOT_RANGE and self.try_shoot(now):
                shot_event = random.random() < HIT_CHANCE  # True=hit
        else:
            self.state = "patrol"
            self.patrol_timer -= dt
            if self.patrol_timer <= 0:
                self.patrol_dir  = random.uniform(0, 2*math.pi)
                self.patrol_timer = random.uniform(1.0, 3.0)

            # Walk in patrol direction, bounce off walls
            spd = self.PATROL_SPEED * dt
            nx = self.x + math.cos(self.patrol_dir) * spd
            ny = self.y + math.sin(self.patrol_dir) * spd
            moved = False
            if not cell(int(nx), int(self.y)): self.x = nx; moved = True
            if not cell(int(self.x), int(ny)): self.y = ny; moved = True
            if not moved: self.patrol_dir = random.uniform(0, 2*math.pi)
            self.angle = self.patrol_dir

        return shot_event   # None=no shot, True=hit player, False=missed

# ═══════════════════════════════════════════════════════════
#  SPRITE PROJECTION (enemy on screen)
# ═══════════════════════════════════════════════════════════
def project_sprite(player, enemy, z_buffer):
    """Returns draw rect + distance or None if behind/blocked."""
    dx = enemy.x - player.x; dy = enemy.y - player.y
    dist = math.hypot(dx, dy)
    if dist < 0.3: return None, None

    sprite_angle = math.atan2(dy, dx)
    angle_diff = (sprite_angle - player.angle + math.pi) % (2*math.pi) - math.pi
    if abs(angle_diff) > HALF_FOV + 0.2: return None, None

    # Check occlusion: average z_buffer across sprite width
    screen_x = int((angle_diff / FOV + 0.5) * W)
    proj_h   = min(H, int(CELL / (dist + 0.001) * (W / FOV) * 0.6))
    w2       = proj_h // 2
    top      = HALF_H - proj_h // 2
    col_l    = max(0, screen_x - w2)
    col_r    = min(W - 1, screen_x + w2)
    if col_r <= col_l: return None, None

    # Is sprite closer than average wall?
    avg_z = sum(z_buffer[c] for c in range(col_l, col_r)) / max(1, col_r - col_l)
    if dist > avg_z: return None, None

    return pygame.Rect(col_l, top, col_r - col_l, proj_h), dist

# ═══════════════════════════════════════════════════════════
#  RENDER FRAME
# ═══════════════════════════════════════════════════════════
def render(screen, player, enemy, fonts, state):
    # ── Sky & floor ──────────────────────────────────────
    screen.fill(C_SKY, (0, 0, W, HALF_H))
    screen.fill(C_FLOOR, (0, HALF_H, W, HALF_H))

    # ── Walls (raycasting) ───────────────────────────────
    ray_angle = player.angle - HALF_FOV
    step      = FOV / NUM_RAYS
    col_w     = W // NUM_RAYS
    z_buffer  = []

    for col in range(NUM_RAYS):
        dist, is_vert = cast_ray(player.x, player.y, ray_angle)
        dist = max(0.01, dist)
        # Fish-eye correction
        dist_fix = dist * math.cos(ray_angle - player.angle)
        z_buffer.append(dist_fix)

        proj_h = min(H, int(CELL / dist_fix * (W / FOV) * 0.55))
        top    = HALF_H - proj_h // 2
        shade  = max(0, 1 - dist_fix / MAX_DEPTH)

        base   = C_WALL_L if is_vert else C_WALL_D
        color  = tuple(int(c * shade * 1.1) for c in base)
        color  = tuple(min(255, c) for c in color)

        screen.fill(color, (col * col_w, top, col_w + 1, proj_h))

        # Floor shading strip
        flr_shade = max(20, int(50 * shade))
        floor_c   = (flr_shade, flr_shade, flr_shade + 6)
        screen.fill(floor_c, (col * col_w, top + proj_h, col_w + 1, max(1, HALF_H - top - proj_h + HALF_H)))

        ray_angle += step

    # ── Enemy sprite ─────────────────────────────────────
    if enemy.alive:
        sprite_rect, sdist = project_sprite(player, enemy, z_buffer)
        if sprite_rect:
            shade = max(0.15, 1 - sdist / MAX_DEPTH)
            body_c = tuple(int(c * shade) for c in C_ENEMY_C)
            # Body
            pygame.draw.ellipse(screen, body_c, sprite_rect)
            # Eye shine
            ex = sprite_rect.centerx; ey = sprite_rect.top + sprite_rect.h // 3
            er = max(2, sprite_rect.w // 6)
            pygame.draw.circle(screen, (240, 240, 60), (ex - er, ey), er)
            pygame.draw.circle(screen, (240, 240, 60), (ex + er, ey), er)
            # Alert glow if chasing
            if enemy.state == "chase":
                s = pygame.Surface((sprite_rect.w + 10, sprite_rect.h + 10), pygame.SRCALPHA)
                pygame.draw.ellipse(s, (255, 60, 60, 40),
                                    s.get_rect().inflate(-4, -4))
                screen.blit(s, (sprite_rect.x - 5, sprite_rect.y - 5))

    # ── HUD ──────────────────────────────────────────────
    _draw_hud(screen, player, enemy, fonts, state)

    # ── Minimap ──────────────────────────────────────────
    _draw_minimap(screen, player, enemy)

    # ── Crosshair ────────────────────────────────────────
    cx, cy = W // 2, H // 2
    pygame.draw.line(screen, C_ACCENT, (cx - 14, cy), (cx - 4, cy), 2)
    pygame.draw.line(screen, C_ACCENT, (cx + 4,  cy), (cx + 14, cy), 2)
    pygame.draw.line(screen, C_ACCENT, (cx, cy - 14), (cx, cy - 4), 2)
    pygame.draw.line(screen, C_ACCENT, (cx, cy + 4),  (cx, cy + 14), 2)
    pygame.draw.circle(screen, C_ACCENT, (cx, cy), 3, 1)

    # ── Hurt overlay ─────────────────────────────────────
    if state.get("hurt_flash", 0) > 0:
        hurt_surf = pygame.Surface((W, H), pygame.SRCALPHA)
        alpha = min(140, int(state["hurt_flash"] * 3.5))
        hurt_surf.fill((180, 0, 0, alpha))
        screen.blit(hurt_surf, (0, 0))
        state["hurt_flash"] -= 4

    # ── Shoot flash ──────────────────────────────────────
    if state.get("shoot_flash", 0) > 0:
        flash_surf = pygame.Surface((W, H), pygame.SRCALPHA)
        flash_surf.fill((255, 200, 80, state["shoot_flash"]))
        screen.blit(flash_surf, (0, 0))
        state["shoot_flash"] = max(0, state["shoot_flash"] - 8)

def _draw_hud(screen, player, enemy, fonts, state):
    f_big, f_med, f_sm = fonts
    now = time.time()

    # ── Ammo / cooldown bar ──────────────────────────────
    cd_frac = min(1.0, (now - player.last_shot) / SHOOT_CD)
    bar_w = 180
    pygame.draw.rect(screen, (40, 40, 50), (W - bar_w - 20, H - 36, bar_w, 16), border_radius=6)
    fill_c = C_ACCENT if cd_frac >= 1.0 else (180, 60, 60)
    pygame.draw.rect(screen, fill_c, (W - bar_w - 20, H - 36, int(bar_w * cd_frac), 16), border_radius=6)
    lbl = f_sm.render("READY" if cd_frac >= 1.0 else "RELOAD", True, C_WHITE)
    screen.blit(lbl, (W - bar_w - 20, H - 56))

    # ── Player HP ────────────────────────────────────────
    hp_lbl = f_med.render("HP", True, C_ACCENT)
    screen.blit(hp_lbl, (20, H - 60))
    for i in range(player.max_hp):
        color = C_RED if i < player.hp else (50, 50, 60)
        pygame.draw.rect(screen, color, (20 + i * 36, H - 36, 28, 22), border_radius=4)
        if i < player.hp:
            pygame.draw.rect(screen, (255, 120, 120), (22 + i * 36, H - 34, 8, 6), border_radius=2)

    # ── Enemy HP (small indicator top centre) ────────────
    if enemy.alive:
        ex_lbl = f_sm.render("ENEMY", True, (180, 80, 80))
        screen.blit(ex_lbl, (W // 2 - 30, 14))
        for i in range(enemy.max_hp):
            color = C_RED if i < enemy.hp else (50, 40, 40)
            pygame.draw.rect(screen, color, (W // 2 - 42 + i * 30, 34, 22, 14), border_radius=3)
    else:
        lbl = f_med.render("ENEMY DOWN", True, (80, 220, 80))
        screen.blit(lbl, (W // 2 - lbl.get_width() // 2, 14))

    # ── Hit marker ───────────────────────────────────────
    if state.get("hit_marker", 0) > 0:
        hm = state["hit_marker"]
        pygame.draw.line(screen, C_HIT_FX, (W//2-16, H//2-16), (W//2+16, H//2+16), 3)
        pygame.draw.line(screen, C_HIT_FX, (W//2+16, H//2-16), (W//2-16, H//2+16), 3)
        state["hit_marker"] = max(0, hm - 4)

    # ── AI state badge ───────────────────────────────────
    if enemy.alive:
        badge_c = (200, 50, 50) if enemy.state == "chase" else (60, 100, 60)
        badge_t = f_sm.render(f"AI: {enemy.state.upper()}", True, C_WHITE)
        pygame.draw.rect(screen, badge_c, (W - badge_t.get_width() - 28, 12, badge_t.get_width() + 16, 24), border_radius=4)
        screen.blit(badge_t, (W - badge_t.get_width() - 20, 15))

def _draw_minimap(screen, player, enemy):
    ox, oy = 14, 14
    # Map tiles
    for my in range(MAP_H):
        for mx in range(MAP_W):
            c = (55, 65, 80) if RAW_MAP[my][mx] == "1" else (20, 24, 32)
            pygame.draw.rect(screen, c, (ox + mx * MINIMAP_S, oy + my * MINIMAP_S, MINIMAP_S - 1, MINIMAP_S - 1))
    # Enemy dot
    if enemy.alive:
        ex = ox + int(enemy.x * MINIMAP_S); ey = oy + int(enemy.y * MINIMAP_S)
        pygame.draw.circle(screen, C_RED,    (ex, ey), 3)
    # Player dot + direction
    px = ox + int(player.x * MINIMAP_S); py = oy + int(player.y * MINIMAP_S)
    pygame.draw.circle(screen, C_ACCENT, (px, py), 3)
    dx = int(math.cos(player.angle) * 6); dy = int(math.sin(player.angle) * 6)
    pygame.draw.line(screen, C_YELLOW, (px, py), (px + dx, py + dy), 2)

# ═══════════════════════════════════════════════════════════
#  SCREENS
# ═══════════════════════════════════════════════════════════
def draw_menu(screen, fonts):
    f_big, f_med, f_sm = fonts
    screen.fill((8, 10, 22))
    # Grid lines for atmosphere
    for i in range(0, W, 40):
        pygame.draw.line(screen, (14, 18, 35), (i, 0), (i, H))
    for i in range(0, H, 40):
        pygame.draw.line(screen, (14, 18, 35), (0, i), (W, i))

    title = f_big.render("SECTOR ZERO", True, C_ACCENT)
    sub   = f_med.render("第一人称战术射击", True, C_YELLOW)
    screen.blit(title, (W//2 - title.get_width()//2, 130))
    screen.blit(sub,   (W//2 - sub.get_width()//2, 200))

    lines = [
        ("WASD",     "移动"),
        ("← →",     "左右旋转"),
        ("LMB / 空格", "射击"),
        ("R",        "重新开始"),
        ("ESC",      "退出"),
        ("",         ""),
        ("",         "─────────────────────"),
        ("规则",      "每人 3 滴血  · 冷却 1 秒/发"),
        ("",         "敌人命中率 30%  · 视线 AI"),
    ]
    y = 280
    for k, v in lines:
        if k == "":
            t = f_sm.render(v, True, (60, 70, 90))
        else:
            t = f_sm.render(f"  {k:15s} {v}", True, C_WHITE)
        screen.blit(t, (W//2 - 180, y)); y += 28

    start = f_med.render("按  ENTER  或  空格  开始", True, C_ACCENT)
    screen.blit(start, (W//2 - start.get_width()//2, y + 20))

def draw_endscreen(screen, fonts, won, player_hp, elapsed):
    f_big, f_med, f_sm = fonts
    screen.fill((6, 8, 18))
    msg_c = (80, 220, 80) if won else (220, 60, 60)
    msg   = "YOU WIN" if won else "YOU DIED"
    t  = f_big.render(msg, True, msg_c)
    t2 = f_med.render(f"생존 시간: {elapsed:.1f}s   남은 HP: {player_hp}", True, C_WHITE)
    t3 = f_sm.render("R 重新开始  ·  ESC 退出", True, C_GRAY)
    screen.blit(t,  (W//2 - t.get_width()//2,  200))
    screen.blit(t2, (W//2 - t2.get_width()//2, 290))
    screen.blit(t3, (W//2 - t3.get_width()//2, 360))

# ═══════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════
def make_entities():
    pair = random.choice(SPAWN_PAIRS)
    px, py = pair[0]; ex, ey = pair[1]
    player = Entity(px, py, angle=random.uniform(0, 2*math.pi), hp=3)
    enemy  = Enemy(ex, ey)
    return player, enemy

def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("SECTOR ZERO  ·  FPS")
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    f_big = pygame.font.SysFont("Courier New", 52, bold=True)
    f_med = pygame.font.SysFont("Courier New", 26, bold=True)
    f_sm  = pygame.font.SysFont("Courier New", 18)
    fonts = (f_big, f_med, f_sm)

    # ── Game state machine ──
    MODE = "menu"   # menu | play | end
    player = enemy = None
    state  = {}
    start_time = 0.0
    result_won = False
    prev_time  = time.time()

    while True:
        now = time.time()
        dt  = min(now - prev_time, 0.05)
        prev_time = now

        # ── Events ───────────────────────────────────────
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

                if MODE == "menu" and ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                    MODE = "play"
                    player, enemy = make_entities()
                    state = {"hurt_flash": 0, "hit_marker": 0, "shoot_flash": 0}
                    start_time = now

                if MODE == "end" and ev.key == pygame.K_r:
                    MODE = "play"
                    player, enemy = make_entities()
                    state = {"hurt_flash": 0, "hit_marker": 0, "shoot_flash": 0}
                    start_time = now

                if MODE == "play" and ev.key == pygame.K_r:
                    MODE = "play"
                    player, enemy = make_entities()
                    state = {"hurt_flash": 0, "hit_marker": 0, "shoot_flash": 0}
                    start_time = now

                # Shoot via Space
                if MODE == "play" and ev.key == pygame.K_SPACE:
                    if player.try_shoot(now):
                        state["shoot_flash"] = 60
                        # Line-of-sight hit check
                        if not enemy.alive:
                            pass
                        else:
                            dx = enemy.x - player.x; dy = enemy.y - player.y
                            dist = math.hypot(dx, dy)
                            a_to_enemy = math.atan2(dy, dx)
                            diff = abs((a_to_enemy - player.angle + math.pi) % (2*math.pi) - math.pi)
                            if diff < 0.15 and dist < MAX_DEPTH:
                                # Check LoS
                                blocked = False
                                steps = int(dist * 6)
                                for i in range(1, steps):
                                    t_ = i / steps
                                    rx = player.x + dx * t_; ry = player.y + dy * t_
                                    if cell(int(rx), int(ry)): blocked = True; break
                                if not blocked:
                                    enemy.take_hit()
                                    state["hit_marker"] = 40

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if MODE == "play":
                    if player.try_shoot(now):
                        state["shoot_flash"] = 60
                        if enemy.alive:
                            dx = enemy.x - player.x; dy = enemy.y - player.y
                            dist = math.hypot(dx, dy)
                            a_to_enemy = math.atan2(dy, dx)
                            diff = abs((a_to_enemy - player.angle + math.pi) % (2*math.pi) - math.pi)
                            if diff < 0.15 and dist < MAX_DEPTH:
                                blocked = False
                                steps = int(dist * 6)
                                for i in range(1, steps):
                                    t_ = i / steps
                                    rx = player.x + dx * t_; ry = player.y + dy * t_
                                    if cell(int(rx), int(ry)): blocked = True; break
                                if not blocked:
                                    enemy.take_hit()
                                    state["hit_marker"] = 40

        # ── Update ───────────────────────────────────────
        if MODE == "play":
            keys = pygame.key.get_pressed()

            # Player move
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.move(math.cos(player.angle) * MOVE_SPEED * dt,
                            math.sin(player.angle) * MOVE_SPEED * dt)
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.move(-math.cos(player.angle) * MOVE_SPEED * dt,
                            -math.sin(player.angle) * MOVE_SPEED * dt)
            if keys[pygame.K_a]:
                player.move(math.cos(player.angle - math.pi/2) * MOVE_SPEED * dt,
                            math.sin(player.angle - math.pi/2) * MOVE_SPEED * dt)
            if keys[pygame.K_d]:
                player.move(math.cos(player.angle + math.pi/2) * MOVE_SPEED * dt,
                            math.sin(player.angle + math.pi/2) * MOVE_SPEED * dt)
            if keys[pygame.K_LEFT]:
                player.angle -= ROT_SPEED
            if keys[pygame.K_RIGHT]:
                player.angle += ROT_SPEED

            # Mouse look
            rel = pygame.mouse.get_rel()
            player.angle += rel[0] * 0.003

            player.angle %= 2 * math.pi

            # AI update
            shot = enemy.update(player.x, player.y, now, dt)
            if shot is True:   # enemy hit player
                if player.take_hit():
                    pass
                state["hurt_flash"] = 140
            # shot == False: enemy shot but missed (no effect)

            # End conditions
            if not player.alive:
                result_won = False
                MODE = "end"
            elif not enemy.alive:
                result_won = True
                MODE = "end"
            else:
                # Render play frame
                render(screen, player, enemy, fonts, state)

        if MODE == "menu":
            draw_menu(screen, fonts)

        if MODE == "end":
            elapsed = now - start_time
            draw_endscreen(screen, fonts, result_won, player.hp if player.alive else 0, elapsed)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
