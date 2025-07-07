import pygame
import random
import sys
import numpy as np

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Game constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GAME_WIDTH = 720
GAME_HEIGHT = 520
CELL_SIZE = 20
BORDER_WIDTH = 40

# Neon colors
BLACK = (0, 0, 0)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 20, 147)
BRIGHT_GREEN = (57, 255, 20)
WHITE = (255, 255, 255)
DARK_BLUE = (0, 100, 150)
GLOW_BLUE = (100, 200, 255)

# Game variables
FPS = 10

class Snake:
    def __init__(self):
        self.positions = [(GAME_WIDTH // 2, GAME_HEIGHT // 2)]
        self.direction = (CELL_SIZE, 0)
        self.grow = False
        
    def move(self):
        head = self.positions[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.positions.insert(0, new_head)
        
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
    
    def change_direction(self, direction):
        # Prevent moving in opposite direction
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
    
    def check_collision(self):
        head = self.positions[0]
        
        # Wall collision
        if (head[0] < BORDER_WIDTH or head[0] >= GAME_WIDTH + BORDER_WIDTH - CELL_SIZE or
            head[1] < BORDER_WIDTH or head[1] >= GAME_HEIGHT + BORDER_WIDTH - CELL_SIZE):
            return True
        
        # Self collision
        if head in self.positions[1:]:
            return True
        
        return False
    
    def draw(self, screen):
        for i, pos in enumerate(self.positions):
            # Draw snake body with glow effect
            if i == 0:  # Head
                # Draw glow
                pygame.draw.rect(screen, GLOW_BLUE, 
                               (pos[0] - 2, pos[1] - 2, CELL_SIZE + 4, CELL_SIZE + 4))
                pygame.draw.rect(screen, NEON_BLUE, 
                               (pos[0], pos[1], CELL_SIZE, CELL_SIZE))
            else:  # Body
                pygame.draw.rect(screen, BRIGHT_GREEN, 
                               (pos[0], pos[1], CELL_SIZE, CELL_SIZE))

class Food:
    def __init__(self):
        self.position = self.generate_position()
    
    def generate_position(self):
        x = random.randint(BORDER_WIDTH, GAME_WIDTH + BORDER_WIDTH - CELL_SIZE)
        y = random.randint(BORDER_WIDTH, GAME_HEIGHT + BORDER_WIDTH - CELL_SIZE)
        # Align to grid
        x = (x // CELL_SIZE) * CELL_SIZE
        y = (y // CELL_SIZE) * CELL_SIZE
        return (x, y)
    
    def draw(self, screen):
        # Draw food with pulsing glow effect
        pygame.draw.rect(screen, NEON_PINK, 
                        (self.position[0] - 2, self.position[1] - 2, 
                         CELL_SIZE + 4, CELL_SIZE + 4))
        pygame.draw.rect(screen, WHITE, 
                        (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("NEON SNAKE")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 20)
        self.game_state = "start_menu"  # start_menu, intro, playing, game_over
        self.intro_timer = 0
        self.load_sounds()
        self.reset_game()
    
    def load_sounds(self):
        """Load or generate sound effects"""
        try:
            # Try to load sound files if they exist
            self.eat_sound = pygame.mixer.Sound("eat.wav")
            self.game_over_sound = pygame.mixer.Sound("game_over.wav")
            self.menu_sound = pygame.mixer.Sound("menu.wav")
        except (pygame.error, FileNotFoundError):
            # Generate synthetic sounds if files don't exist
            self.eat_sound = self.generate_eat_sound()
            self.game_over_sound = self.generate_game_over_sound()
            self.menu_sound = self.generate_menu_sound()
    
    def generate_eat_sound(self):
        """Generate a synthetic eating sound"""
        duration = 0.1
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Create a pleasant eating sound
        t = np.linspace(0, duration, frames, False)
        frequency = 800
        # Create a simple sine wave with decay
        wave = np.sin(frequency * 2 * np.pi * t) * np.exp(-t * 10)
        # Convert to 16-bit integers
        wave = (wave * 32767).astype(np.int16)
        # Make stereo and ensure C-contiguous
        stereo_wave = np.column_stack((wave, wave)).astype(np.int16)
        stereo_wave = np.ascontiguousarray(stereo_wave)
        
        sound = pygame.sndarray.make_sound(stereo_wave)
        return sound
    
    def generate_game_over_sound(self):
        """Generate a synthetic game over sound"""
        duration = 0.5
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Create a descending game over sound
        t = np.linspace(0, duration, frames, False)
        frequency = 400 - 300 * t / duration  # Descending from 400Hz to 100Hz
        wave = np.sin(frequency * 2 * np.pi * t) * np.exp(-t * 2)
        # Convert to 16-bit integers
        wave = (wave * 32767).astype(np.int16)
        # Make stereo and ensure C-contiguous
        stereo_wave = np.column_stack((wave, wave)).astype(np.int16)
        stereo_wave = np.ascontiguousarray(stereo_wave)
        
        sound = pygame.sndarray.make_sound(stereo_wave)
        return sound
    
    def generate_menu_sound(self):
        """Generate a synthetic menu selection sound"""
        duration = 0.05
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        # Create a short click sound
        t = np.linspace(0, duration, frames, False)
        frequency = 1200
        wave = np.sin(frequency * 2 * np.pi * t) * np.exp(-t * 20)
        # Convert to 16-bit integers
        wave = (wave * 32767).astype(np.int16)
        # Make stereo and ensure C-contiguous
        stereo_wave = np.column_stack((wave, wave)).astype(np.int16)
        stereo_wave = np.ascontiguousarray(stereo_wave)
        
        sound = pygame.sndarray.make_sound(stereo_wave)
        return sound
    
    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
    
    def draw_start_menu(self):
        # Clear screen with black background
        self.screen.fill(BLACK)
        
        # Draw animated border effect
        for i in range(8):
            color_intensity = 100 + (i * 20)
            glow_color = (0, color_intensity // 4, color_intensity)
            pygame.draw.rect(self.screen, glow_color, 
                           (50 - i * 3, 100 - i * 3,
                            WINDOW_WIDTH - 100 + i * 6, WINDOW_HEIGHT - 200 + i * 6), 2)
        
        # Main title with large glow effect
        title_text = pygame.font.Font(None, 72).render("NEON SNAKE", True, NEON_BLUE)
        title_glow = pygame.font.Font(None, 72).render("NEON SNAKE", True, GLOW_BLUE)
        
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        glow_rect = title_glow.get_rect(center=(WINDOW_WIDTH // 2 + 3, 153))
        
        self.screen.blit(title_glow, glow_rect)
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font_medium.render("Classic Arcade Experience", True, NEON_PINK)
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Menu options
        start_text = self.font_large.render("PRESS SPACE TO START", True, WHITE)
        start_glow = self.font_large.render("PRESS SPACE TO START", True, BRIGHT_GREEN)
        
        start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, 300))
        start_glow_rect = start_glow.get_rect(center=(WINDOW_WIDTH // 2 + 2, 302))
        
        self.screen.blit(start_glow, start_glow_rect)
        self.screen.blit(start_text, start_rect)
        
        # Instructions
        instructions = [
            "HOW TO PLAY:",
            "• Use ARROW KEYS or WASD to move",
            "• Eat white food to grow and score points",
            "• Avoid walls and your own body",
            "• Each food gives you 10 points"
        ]
        
        y_offset = 380
        for i, instruction in enumerate(instructions):
            if i == 0:
                text = self.font_medium.render(instruction, True, NEON_PINK)
            else:
                text = self.font_small.render(instruction, True, WHITE)
            
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30
        
        # Footer
        footer_text = self.font_tiny.render("Press ESC to quit anytime", True, DARK_BLUE)
        footer_rect = footer_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
        self.screen.blit(footer_text, footer_rect)
    
    def draw_intro(self):
        # Clear screen with black background
        self.screen.fill(BLACK)
        
        # Animated intro sequence
        progress = min(self.intro_timer / 180.0, 1.0)  # 3 seconds at 60fps
        
        if progress < 0.3:
            # Phase 1: Title appears
            alpha = int((progress / 0.3) * 255)
            title_text = pygame.font.Font(None, 64).render("GET READY", True, NEON_BLUE)
            title_text.set_alpha(alpha)
            title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(title_text, title_rect)
            
        elif progress < 0.6:
            # Phase 2: Instructions appear
            title_text = pygame.font.Font(None, 64).render("GET READY", True, NEON_BLUE)
            title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(title_text, title_rect)
            
            alpha = int(((progress - 0.3) / 0.3) * 255)
            instruction_text = self.font_medium.render("Control the neon snake", True, NEON_PINK)
            instruction_text.set_alpha(alpha)
            instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(instruction_text, instruction_rect)
            
        else:
            # Phase 3: Countdown
            title_text = pygame.font.Font(None, 64).render("GET READY", True, NEON_BLUE)
            title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(title_text, title_rect)
            
            instruction_text = self.font_medium.render("Control the neon snake", True, NEON_PINK)
            instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(instruction_text, instruction_rect)
            
            countdown_progress = (progress - 0.6) / 0.4
            countdown_number = 3 - int(countdown_progress * 3)
            if countdown_number > 0:
                countdown_text = pygame.font.Font(None, 96).render(str(countdown_number), True, WHITE)
                countdown_glow = pygame.font.Font(None, 96).render(str(countdown_number), True, BRIGHT_GREEN)
                
                countdown_rect = countdown_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
                glow_rect = countdown_glow.get_rect(center=(WINDOW_WIDTH // 2 + 3, WINDOW_HEIGHT // 2 + 63))
                
                self.screen.blit(countdown_glow, glow_rect)
                self.screen.blit(countdown_text, countdown_rect)
        
        # Draw border effect during intro
        for i in range(5):
            color_intensity = int(255 * progress) - (i * 40)
            if color_intensity > 0:
                glow_color = (0, color_intensity // 3, color_intensity)
                pygame.draw.rect(self.screen, glow_color, 
                               (20 - i, 20 - i,
                                WINDOW_WIDTH - 40 + (i * 2), WINDOW_HEIGHT - 40 + (i * 2)), 2)
        
        self.intro_timer += 1
        
        # Transition to game after intro
        if self.intro_timer >= 180:  # 3 seconds
            self.game_state = "playing"
            self.intro_timer = 0
    
    def draw_border(self):
        # Draw outer glow border
        for i in range(5):
            color_intensity = 255 - (i * 40)
            glow_color = (0, color_intensity // 3, color_intensity)
            pygame.draw.rect(self.screen, glow_color, 
                           (BORDER_WIDTH - 20 - i, BORDER_WIDTH - 20 - i,
                            GAME_WIDTH + 40 + (i * 2), GAME_HEIGHT + 40 + (i * 2)), 2)
        
        # Draw main border
        pygame.draw.rect(self.screen, NEON_BLUE, 
                        (BORDER_WIDTH - 10, BORDER_WIDTH - 10,
                         GAME_WIDTH + 20, GAME_HEIGHT + 20), 3)
        # Draw outer glow border
        for i in range(5):
            color_intensity = 255 - (i * 40)
            glow_color = (0, color_intensity // 3, color_intensity)
            pygame.draw.rect(self.screen, glow_color, 
                           (BORDER_WIDTH - 20 - i, BORDER_WIDTH - 20 - i,
                            GAME_WIDTH + 40 + (i * 2), GAME_HEIGHT + 40 + (i * 2)), 2)
        
        # Draw main border
        pygame.draw.rect(self.screen, NEON_BLUE, 
                        (BORDER_WIDTH - 10, BORDER_WIDTH - 10,
                         GAME_WIDTH + 20, GAME_HEIGHT + 20), 3)
    
    def draw_ui(self):
        # Draw score with glow effect
        score_text = self.font_medium.render(f"SCORE: {self.score}", True, NEON_PINK)
        score_glow = self.font_medium.render(f"SCORE: {self.score}", True, WHITE)
        
        # Draw glow first (offset)
        self.screen.blit(score_glow, (22, 22))
        self.screen.blit(score_text, (20, 20))
        
        # Draw game title
        title_text = self.font_large.render("NEON SNAKE", True, NEON_BLUE)
        title_glow = self.font_large.render("NEON SNAKE", True, GLOW_BLUE)
        
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 30))
        glow_rect = title_glow.get_rect(center=(WINDOW_WIDTH // 2 + 2, 32))
        
        self.screen.blit(title_glow, glow_rect)
        self.screen.blit(title_text, title_rect)
    
    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text with glow
        game_over_text = self.font_large.render("GAME OVER", True, NEON_PINK)
        game_over_glow = self.font_large.render("GAME OVER", True, WHITE)
        
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
        glow_rect = game_over_glow.get_rect(center=(WINDOW_WIDTH // 2 + 2, WINDOW_HEIGHT // 2 - 78))
        
        self.screen.blit(game_over_glow, glow_rect)
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        final_score_text = self.font_medium.render(f"FINAL SCORE: {self.score}", True, NEON_BLUE)
        final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        self.screen.blit(final_score_text, final_score_rect)
        
        # Instructions
        restart_text = self.font_small.render("SPACE - Play Again", True, BRIGHT_GREEN)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = self.font_small.render("M - Main Menu", True, WHITE)
        menu_rect = menu_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(menu_text, menu_rect)
        
        quit_text = self.font_small.render("ESC - Quit Game", True, DARK_BLUE)
        quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
        self.screen.blit(quit_text, quit_rect)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if self.game_state == "start_menu":
                    if event.key == pygame.K_SPACE:
                        self.menu_sound.play()
                        self.game_state = "intro"
                        self.intro_timer = 0
                
                elif self.game_state == "intro":
                    # Skip intro with any key
                    self.menu_sound.play()
                    self.game_state = "playing"
                    self.intro_timer = 0
                
                elif self.game_state == "playing":
                    if not self.game_over:
                        # Snake movement
                        if event.key == pygame.K_UP or event.key == pygame.K_w:
                            self.snake.change_direction((0, -CELL_SIZE))
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            self.snake.change_direction((0, CELL_SIZE))
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            self.snake.change_direction((-CELL_SIZE, 0))
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            self.snake.change_direction((CELL_SIZE, 0))
                    else:
                        if event.key == pygame.K_SPACE:
                            self.menu_sound.play()
                            self.reset_game()
                            self.game_state = "intro"
                        elif event.key == pygame.K_m:
                            self.menu_sound.play()
                            self.game_state = "start_menu"
        
        return True
    
    def update(self):
        if self.game_state == "playing" and not self.game_over:
            self.snake.move()
            
            # Check collision with food
            if self.snake.positions[0] == self.food.position:
                self.score += 10
                self.snake.grow = True
                self.eat_sound.play()  # Play eating sound
                self.food.position = self.food.generate_position()
                
                # Make sure food doesn't spawn on snake
                while self.food.position in self.snake.positions:
                    self.food.position = self.food.generate_position()
            
            # Check collisions
            if self.snake.check_collision():
                self.game_over = True
                self.game_over_sound.play()  # Play game over sound
    
    def draw(self):
        if self.game_state == "start_menu":
            self.draw_start_menu()
        elif self.game_state == "intro":
            self.draw_intro()
        elif self.game_state == "playing":
            # Clear screen with black background
            self.screen.fill(BLACK)
            
            # Draw border and UI
            self.draw_border()
            self.draw_ui()
            
            if not self.game_over:
                # Draw game objects
                self.snake.draw(self.screen)
                self.food.draw(self.screen)
            else:
                # Draw game over screen
                self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        running = True
        
        print("🐍 NEON SNAKE GAME 🐍")
        print("Welcome to the retro arcade experience!")
        print("\nGame Features:")
        print("- Classic snake gameplay with neon styling")
        print("- Glowing visual effects and smooth animations")
        print("- Start menu and intro sequence")
        print("- Score tracking and game over screen")
        print("\nStarting game...")
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
