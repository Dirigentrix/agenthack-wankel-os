import pygame
import math
import random
import time
from typing import List, Dict, Any, Callable

# --- CONFIGURATION & CONSTANTS ---
WIDTH, HEIGHT = 1280, 720
FPS = 60
COLOR_BG = (5, 5, 10)
COLOR_GRID = (20, 20, 40)
COLOR_CORE = (100, 200, 255)
COLOR_ORBIT = (50, 100, 150)
COLOR_TEXT = (200, 230, 255)
COLOR_CLONE = (0, 255, 200)

# Memory Management Config
MAX_LOG_LINES = 500
DISPLAY_LOG_LINES = 10
MAX_PARTICLES = 150

class CommandHandler:
    """Modular and extensible handler for GX commands."""
    def __init__(self, vis: 'Sonia_v6_3'):
        self.vis = vis
        self.commands: Dict[str, Callable[[Dict[str, Any]], None]] = {
            "PING": self._handle_ping,
            "RESONANCE_SET": self._handle_resonance_set,
            "LOG_CLEAR": self._handle_log_clear,
            "EMERGENCY_STOP": self._handle_emergency_stop,
            "SYNC_CLONE": self._handle_sync_clone
        }

    def execute(self, cmd_type: str, data: Dict[str, Any] = None):
        handler = self.commands.get(cmd_type)
        if handler:
            handler(data or {})
        else:
            self.vis.add_status_message(f"UNKNOWN GX_COMMAND: {cmd_type}")

    def register_command(self, cmd_type: str, handler: Callable[[Dict[str, Any]], None]):
        self.commands[cmd_type] = handler

    def _handle_ping(self, data):
        self.vis.add_status_message("PONG - SYSTEM ALIVE")

    def _handle_resonance_set(self, data):
        val = data.get("value", 156.0)
        self.vis.resonance = float(val)
        self.vis.add_status_message(f"RESONANCE OVERRIDE: {val} Hz")

    def _handle_log_clear(self, data):
        self.vis.status_log = ["LOG CLEARED"]

    def _handle_emergency_stop(self, data):
        self.vis.running = False

    def _handle_sync_clone(self, data):
        intencja = data.get("intencja", "NEUTRAL")
        self.vis.clone_sync(intencja)

class Sonia_v6_3:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("SONIA v6.3 - CLONE ROBOTIC SYNC - AGENTHACK WANKEL OS")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("monospace", 14)
        
        # Core State
        self.particles: List[Dict[str, Any]] = []
        self.status_log: List[str] = ["SYSTEM READY", "SONIA v6.3 INITIALIZED"]
        self.resonance = 156.0
        self.clone_status = "IDLE"
        self.sync_level = 0.0
        
        self.start_time = time.time()
        self.gx_handler = CommandHandler(self)

    def add_status_message(self, msg: str):
        """Adds message with auto-pruning to prevent memory leaks."""
        timestamp = time.strftime('%H:%M:%S')
        self.status_log.append(f"[{timestamp}] {msg}")
        if len(self.status_log) > MAX_LOG_LINES:
            self.status_log = self.status_log[-MAX_LOG_LINES:]

    def clone_sync(self, intencja: str):
        """Implements Clone Robotic sync logic."""
        self.clone_status = f"SYNCING: {intencja}"
        self.sync_level = random.uniform(85.0, 99.9)
        self.add_status_message(f"CLONE SYNC INITIATED: {intencja} ({self.sync_level:.2f}%)")

    def robotic_pulse(self):
        """Calculates micro-drift resonance (156 Hz + fluctuation)."""
        drift = random.uniform(-0.5, 0.5)
        self.resonance = 156.0 + drift
        
        # Visual pulse effect
        if random.random() < 0.02:
            self.add_status_message(f"ROBOTIC PULSE: {self.resonance:.3f} Hz")

    def draw_background_grid(self):
        for x in range(0, WIDTH, 40):
            pygame.draw.line(self.screen, COLOR_GRID, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, 40):
            pygame.draw.line(self.screen, COLOR_GRID, (0, y), (WIDTH, y))

    def draw_central_core(self):
        center = (WIDTH // 2, HEIGHT // 2)
        # Pulse based on resonance
        pulse_factor = math.sin(time.time() * (self.resonance / 20.0)) * 15
        pygame.draw.circle(self.screen, COLOR_CORE, center, 50 + int(pulse_factor), 2)
        
        # Clone Status indicator
        if "SYNCING" in self.clone_status:
            pygame.draw.circle(self.screen, COLOR_CLONE, center, 20 + int(pulse_factor/2), 0)
        else:
            pygame.draw.circle(self.screen, COLOR_CORE, center, 10, 0)

    def draw_systems_orbit(self):
        center = (WIDTH // 2, HEIGHT // 2)
        t = time.time()
        for i in range(3):
            angle = t + (i * (2 * math.pi / 3))
            dist = 150 + (10 * math.sin(t * 2))
            x = center[0] + math.cos(angle) * dist
            y = center[1] + math.sin(angle) * dist
            pygame.draw.circle(self.screen, COLOR_ORBIT, (int(x), int(y)), 8, 1)

    def draw_resonance_waves(self):
        center = (WIDTH // 2, HEIGHT // 2)
        for i in range(1, 4):
            radius = (int(time.time() * (self.resonance / 3)) % 400) + (i * 60)
            if radius < 500:
                alpha = max(0, 200 - (radius // 2))
                s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                pygame.draw.circle(s, (100, 200, 255, alpha), center, radius, 1)
                self.screen.blit(s, (0,0))

    def draw_particles(self):
        for p in self.particles:
            pygame.draw.circle(self.screen, p['color'], (int(p['x']), int(p['y'])), 2)

    def draw_ui_panel(self):
        rect = pygame.Rect(20, 20, 320, 240)
        pygame.draw.rect(self.screen, (10, 10, 30), rect)
        pygame.draw.rect(self.screen, COLOR_ORBIT, rect, 1)
        
        elapsed = int(time.time() - self.start_time)
        texts = [
            f"OS: WANKEL-OS",
            f"CORE: SONIA v6.3",
            f"RESONANCE: {self.resonance:.3f} Hz",
            f"CLONE STATUS: {self.clone_status}",
            f"SYNC LEVEL: {self.sync_level:.2f}%",
            f"UPTIME: {elapsed}s",
            f"LOG_SIZE: {len(self.status_log)}"
        ]
        for i, t in enumerate(texts):
            color = COLOR_CLONE if "CLONE" in t or "SYNC" in t else COLOR_TEXT
            img = self.font.render(t, True, color)
            self.screen.blit(img, (30, 35 + i * 25))

    def draw_status_log(self):
        display_subset = self.status_log[-DISPLAY_LOG_LINES:]
        for i, msg in enumerate(display_subset):
            img = self.font.render(f"> {msg}", True, (0, 255, 150))
            self.screen.blit(img, (20, HEIGHT - 220 + i * 20))

    def update_particles(self):
        if len(self.particles) < MAX_PARTICLES:
            self.particles.append({
                'x': WIDTH // 2,
                'y': HEIGHT // 2,
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 2),
                'color': COLOR_CLONE if "SYNCING" in self.clone_status else (100, 150, 255),
                'life': 100
            })
        for p in self.particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 1
            if p['life'] <= 0:
                self.particles.remove(p)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.gx_handler.execute("SYNC_CLONE", {"intencja": "REPAIR"})
                    if event.key == pygame.K_p:
                        self.gx_handler.execute("PING")

            self.robotic_pulse()
            self.update_particles()

            self.screen.fill(COLOR_BG)
            self.draw_background_grid()
            self.draw_resonance_waves()
            self.draw_central_core()
            self.draw_systems_orbit()
            self.draw_particles()
            self.draw_ui_panel()
            self.draw_status_log()

            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    print("Sonia_v6_3 (Clone Robotic Sync) initialized.")
