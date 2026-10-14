import pygame
import sys
import math

# 1. Initialize Pygame Graphics Engine
pygame.init()

SCREEN_WIDTH = 540
SCREEN_HEIGHT = 960
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maa Kushmanda Divine Realtime Code")
clock = pygame.time.Clock()

def load_and_clean_weapon(image_path, size):
    try:
        img = pygame.image.load(image_path).convert_alpha()
        img = pygame.transform.smoothscale(img, size)
        clean_surf = pygame.Surface(img.get_size(), pygame.SRCALPHA)
        for x in range(img.get_width()):
            for y in range(img.get_height()):
                r, g, b, a = img.get_at((x, y))
                if r > 215 and g > 215 and b > 215:
                    clean_surf.set_at((x, y), (0, 0, 0, 0))
                else:
                    clean_surf.set_at((x, y), (r, g, b, a))
        return clean_surf
    except Exception as e:
        return pygame.transform.smoothscale(pygame.image.load(image_path).convert_alpha(), size)

# 2. Load Assets with Bigger Trishul Size
print("Processing images and injecting divine cosmic enhancements...")
try:
    bg_orig = pygame.image.load("bg_mandala.jpg").convert_alpha()
    trishul_image = load_and_clean_weapon("trishul.png", (180, 180))
    goddess_image = pygame.image.load("mata_cutout.png").convert_alpha()
    goddess_image = pygame.transform.smoothscale(goddess_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    weapons_raw = [
        load_and_clean_weapon("weapon_chakra.png", (95, 95)),
        load_and_clean_weapon("weapon_kamal.png", (95, 95)),
        load_and_clean_weapon("weapon_dhanush.png", (95, 95)),
        load_and_clean_weapon("weapon_gada.png", (95, 95)),
        load_and_clean_weapon("weapon_mala.png", (95, 95)),
        load_and_clean_weapon("weapon_kalash.png", (95, 95))
    ]
except pygame.error as e:
    print(f"Asset Loading Failed: {e}. Verify your filenames in the folder.")
    sys.exit()

bg_image = pygame.transform.smoothscale(bg_orig, (950, 950))

# 3. Time Vectors Configuration
frame_count = 0
fps = 60
bg_angle = 0
flash_opacity = 0
show_goddess = False
shake_timer = 0

T_RISE = 1.5 * fps
T_SPAWN = 3.5 * fps
T_TRISHUL_END = 5.5 * fps   
T_WEAPONS_ENTRY = 9.0 * fps 
T_ORBIT = 11.0 * fps         
T_IMPLODE = 12.2 * fps       
T_FLASH = 12.8 * fps         

def blit_rotate_center(surf, image, center_pos, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=center_pos)
    surf.blit(rotated_image, new_rect.topleft)

def draw_cosmic_rays(surf, center, num_rays, length, angle_offset, opacity):
    ray_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for i in range(num_rays):
        angle = math.radians(i * (360 / num_rays) + angle_offset)
        end_x = center[0] + length * math.cos(angle)
        end_y = center[1] + length * math.sin(angle)
        pygame.draw.line(ray_surf, (255, 140, 0, int(opacity)), center, (int(end_x), int(end_y)), 4)
    surf.blit(ray_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

# 4. Core Presentation Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame_count += 1
    current_time = frame_count

    offset_x, offset_y = 0, 0
    if shake_timer > 0:
        shake_timer -= 1
        offset_x = int(math.sin(frame_count * 3.5) * 12)
        offset_y = int(math.cos(frame_count * 3.5) * 12)

    center_x = SCREEN_WIDTH // 2 + offset_x
    center_y = SCREEN_HEIGHT // 2 + offset_y

    if not show_goddess:
        screen.fill((12, 3, 18))
        bg_angle = (bg_angle + 0.3) % 360
        bg_rect = bg_image.get_rect(center=(center_x, center_y))
        blit_rotate_center(screen, bg_image, bg_rect.center, bg_angle)

    if not show_goddess:
        if current_time < T_RISE:
            progress = current_time / T_RISE
            y_pos = int(SCREEN_HEIGHT + 150 - (SCREEN_HEIGHT / 2 + 150) * progress)
            blit_rotate_center(screen, trishul_image, (center_x, y_pos), 0)

        elif T_RISE <= current_time < T_SPAWN:
            progress = (current_time - T_RISE) / (T_SPAWN - T_RISE)
            draw_cosmic_rays(screen, (center_x, center_y), 16, 400, frame_count * 0.5, 60 * progress)
            distances = [-170 * progress, -85 * progress, 0, 85 * progress, 170 * progress]
            for i, x_off in enumerate(distances):
                rot_angle = (i - 2) * 12 * progress
                blit_rotate_center(screen, trishul_image, (center_x + x_off, center_y), rot_angle)

        elif T_SPAWN <= current_time < T_TRISHUL_END:
            spin_speed = (current_time - T_SPAWN) * 3.5
            draw_cosmic_rays(screen, (center_x, center_y), 24, 450, frame_count * 0.8, 90)
            for i in range(5):
                angle_rad = math.radians((i - 2) * 22 + spin_speed)
                radius = 120
                px = center_x + int(radius * math.cos(angle_rad))
                py = center_y + int(radius * math.sin(angle_rad))
                blit_rotate_center(screen, trishul_image, (px, py), spin_speed)

        elif T_TRISHUL_END <= current_time < T_WEAPONS_ENTRY:
            duration = T_WEAPONS_ENTRY - T_TRISHUL_END
            num_w = len(weapons_raw)
            for idx, w_img in enumerate(weapons_raw):
                w_delay = idx * (duration / num_w)
                w_progress = max(0.0, min(1.0, (current_time - T_TRISHUL_END - w_delay) / (duration / 2.5)))
                if w_progress > 0:
                    final_angle = math.radians(idx * (360 / num_w))
                    radius = 130
                    inverse = 1.0 - w_progress
                    sx = center_x + (math.cos(final_angle) * 400 * inverse)
                    sy = center_y + (math.sin(final_angle) * 400 * inverse)
                    blit_rotate_center(screen, w_img, (int(sx), int(sy)), current_time * 3)

        elif T_WEAPONS_ENTRY <= current_time < T_ORBIT:
            spin_offset = (current_time - T_WEAPONS_ENTRY) * 2.0
            num_w = len(weapons_raw)
            draw_cosmic_rays(screen, (center_x, center_y), 18, 420, frame_count * 0.4, 50)
            for idx, w_img in enumerate(weapons_raw):
                angle_rad = math.radians(idx * (360 / num_w) + spin_offset)
                radius = 130
                px = center_x + int(radius * math.cos(angle_rad))
                py = center_y + int(radius * math.sin(angle_rad))
                blit_rotate_center(screen, w_img, (px, py), spin_offset * 1.5)

        elif T_ORBIT <= current_time < T_IMPLODE:
            progress = (current_time - T_ORBIT) / (T_IMPLODE - T_ORBIT)
            inverse_progress = 1.0 - progress
            spin_offset = (T_ORBIT - T_WEAPONS_ENTRY) * 2.0 + (current_time - T_ORBIT) * 5.0
            num_w = len(weapons_raw)
            draw_cosmic_rays(screen, (center_x, center_y), 32, 500, frame_count * 1.5, int(150 * progress))
            for idx, w_img in enumerate(weapons_raw):
                angle_rad = math.radians(idx * (360 / num_w) + spin_offset)
                radius = int(130 * inverse_progress) 
                px = center_x + int(radius * math.cos(angle_rad))
                py = center_y + int(radius * math.sin(angle_rad))
                shrink_size = max(5, int(95 * inverse_progress))
                if shrink_size > 5:
                    shrunk_w = pygame.transform.smoothscale(w_img, (shrink_size, shrink_size))
                    blit_rotate_center(screen, shrunk_w, (px, py), spin_offset * 2)

        if current_time >= T_IMPLODE:
            show_goddess = True
            flash_opacity = 255
            shake_timer = 25
    else:
        breath_scale = 1.0 + 0.02 * math.sin(frame_count * 0.04)
        b_w = int(SCREEN_WIDTH * breath_scale)
        b_h = int(SCREEN_HEIGHT * breath_scale)
        scaled_goddess = pygame.transform.smoothscale(goddess_image, (b_w, b_h))
        g_rect = scaled_goddess.get_rect(center=(center_x, center_y))
        screen.blit(scaled_goddess, g_rect.topleft)

    if flash_opacity > 0:
        flash_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        flash_surf.fill((255, 240, 200)) 
        flash_surf.set_alpha(int(flash_opacity))
        screen.blit(flash_surf, (0, 0))
        flash_opacity -= 5.5

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()