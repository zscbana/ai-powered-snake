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

class Button:
    def __init__(self, x, y, width, height, text, font, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.hovered = False
        self.clicked = False
    
    def handle_event(self, event, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                self.clicked = True
                return True
        return False
    
    def draw(self, screen):
        # Button colors based on state
        if self.clicked:
            border_color = WHITE
            text_color = NEON_PINK
            glow_intensity = 8
        elif self.hovered:
            border_color = NEON_PINK
            text_color = WHITE
            glow_intensity = 6
        else:
            border_color = NEON_BLUE
            text_color = NEON_BLUE
            glow_intensity = 4
        
        # Draw glowing border effect
        for i in range(glow_intensity):
            intensity = 255 - (i * 30)
            if intensity > 0:
                glow_color = (border_color[0] * intensity // 255, 
                             border_color[1] * intensity // 255, 
                             border_color[2] * intensity // 255)
                pygame.draw.rect(screen, glow_color, 
                               (self.rect.x - i, self.rect.y - i,
                                self.rect.width + i * 2, self.rect.height + i * 2), 2)
        
        # Draw button background
        pygame.draw.rect(screen, BLACK, self.rect)
        pygame.draw.rect(screen, border_color, self.rect, 3)
        
        # Draw text with glow effect
        text_surface = self.font.render(self.text, True, text_color)
        if self.hovered or self.clicked:
            glow_surface = self.font.render(self.text, True, WHITE)
            glow_rect = glow_surface.get_rect(center=(self.rect.centerx + 1, self.rect.centery + 1))
            screen.blit(glow_surface, glow_rect)
        
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
        # Reset clicked state
        if self.clicked:
            self.clicked = False

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
        self.game_state = "start_menu"  # start_menu, intro, playing, paused, game_over, how_to_play
        self.intro_timer = 0
        self.music_muted = False
        self.pause_menu_selection = 0  # 0: Resume, 1: Mute/Unmute, 2: Main Menu
        self.mouse_pos = (0, 0)
        self.buttons = []
        self.load_sounds()
        self.start_background_music()
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
    
    def generate_background_music(self):
        """Generate arcade-style background music"""
        duration = 8.0  # 8 seconds loop
        sample_rate = 22050
        frames = int(duration * sample_rate)
        
        t = np.linspace(0, duration, frames, False)
        
        # Create a simple arcade melody with multiple harmonics
        # Main melody line
        melody_freq = 220  # A3 base frequency
        melody = np.sin(melody_freq * 2 * np.pi * t)
        
        # Add some variation - simple arpeggio pattern
        pattern_length = duration / 8  # 8 notes in the loop
        for i in range(8):
            start_time = i * pattern_length
            end_time = (i + 1) * pattern_length
            
            # Create frequency pattern: A, C, E, G, A, G, E, C
            frequencies = [220, 261.63, 329.63, 392, 440, 392, 329.63, 261.63]
            freq = frequencies[i]
            
            # Apply frequency to the time segment
            mask = (t >= start_time) & (t < end_time)
            melody[mask] = np.sin(freq * 2 * np.pi * t[mask]) * np.exp(-(t[mask] - start_time) * 2)
        
        # Add bass line
        bass_freq = 110  # A2
        bass = 0.3 * np.sin(bass_freq * 2 * np.pi * t)
        
        # Add some harmony
        harmony = 0.2 * np.sin(330 * 2 * np.pi * t)  # E4
        
        # Combine all parts
        music = 0.4 * melody + bass + harmony
        
        # Apply overall envelope to make it less harsh
        envelope = 0.8 + 0.2 * np.sin(0.5 * 2 * np.pi * t)
        music = music * envelope
        
        # Normalize and convert to 16-bit
        music = music / np.max(np.abs(music)) * 0.3  # Keep volume moderate
        music = (music * 32767).astype(np.int16)
        
        # Make stereo and ensure C-contiguous
        stereo_music = np.column_stack((music, music)).astype(np.int16)
        stereo_music = np.ascontiguousarray(stereo_music)
        
        return stereo_music
    
    def start_background_music(self):
        """Start playing background music"""
        try:
            # Try to load external music file first
            pygame.mixer.music.load("background_music.ogg")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            self.using_pygame_music = True
        except (pygame.error, FileNotFoundError):
            # Generate and play synthetic background music
            music_array = self.generate_background_music()
            music_sound = pygame.sndarray.make_sound(music_array)
            
            # Use a dedicated channel for looping the generated sound
            self.music_channel = pygame.mixer.Channel(7)  # Use channel 7 for music
            self.background_music_sound = music_sound
            self.music_channel.play(music_sound, loops=-1)
            self.music_channel.set_volume(0.3)
            self.using_pygame_music = False
    
    def toggle_music(self):
        """Toggle background music on/off"""
        self.music_muted = not self.music_muted
        
        if self.music_muted:
            # Stop/mute the music
            if hasattr(self, 'using_pygame_music') and self.using_pygame_music:
                pygame.mixer.music.set_volume(0)
            elif hasattr(self, 'music_channel'):
                self.music_channel.set_volume(0)
        else:
            # Resume/unmute the music
            if hasattr(self, 'using_pygame_music') and self.using_pygame_music:
                pygame.mixer.music.set_volume(0.3)
            elif hasattr(self, 'music_channel'):
                self.music_channel.set_volume(0.3)
    
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
        
        # Create buttons if they don't exist
        if not self.buttons:
            self.buttons = [
                Button(WINDOW_WIDTH // 2 - 100, 280, 200, 50, "START GAME", self.font_medium, "start"),
                Button(WINDOW_WIDTH // 2 - 100, 350, 200, 50, "HOW TO PLAY", self.font_medium, "how_to_play"),
                Button(WINDOW_WIDTH // 2 - 100, 420, 200, 50, "QUIT", self.font_medium, "quit")
            ]
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
        
        # Footer
        footer_text = self.font_tiny.render("Use mouse to click buttons or press ESC to quit", True, DARK_BLUE)
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
    
    def draw_pause_menu(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw border around pause menu
        menu_width = 400
        menu_height = 300
        menu_x = (WINDOW_WIDTH - menu_width) // 2
        menu_y = (WINDOW_HEIGHT - menu_height) // 2
        
        # Draw glowing border
        for i in range(5):
            color_intensity = 255 - (i * 40)
            glow_color = (0, color_intensity // 3, color_intensity)
            pygame.draw.rect(self.screen, glow_color, 
                           (menu_x - 10 - i, menu_y - 10 - i,
                            menu_width + 20 + (i * 2), menu_height + 20 + (i * 2)), 2)
        
        # Pause title
        pause_text = self.font_large.render("GAME PAUSED", True, NEON_BLUE)
        pause_glow = self.font_large.render("GAME PAUSED", True, GLOW_BLUE)
        
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, menu_y + 50))
        glow_rect = pause_glow.get_rect(center=(WINDOW_WIDTH // 2 + 2, menu_y + 52))
        
        self.screen.blit(pause_glow, glow_rect)
        self.screen.blit(pause_text, pause_rect)
        
        # Menu options
        menu_options = [
            "RESUME GAME",
            f"MUSIC: {'OFF' if self.music_muted else 'ON'}",
            "MAIN MENU"
        ]
        
        colors = [WHITE, WHITE, WHITE]
        colors[self.pause_menu_selection] = NEON_PINK  # Highlight selected option
        
        for i, (option, color) in enumerate(zip(menu_options, colors)):
            y_pos = menu_y + 120 + (i * 40)
            
            # Draw selection indicator
            if i == self.pause_menu_selection:
                indicator_text = self.font_medium.render(">", True, BRIGHT_GREEN)
                self.screen.blit(indicator_text, (menu_x + 50, y_pos))
                
                # Add glow effect to selected option
                option_glow = self.font_medium.render(option, True, WHITE)
                option_rect = option_glow.get_rect(center=(WINDOW_WIDTH // 2 + 2, y_pos + 2))
                self.screen.blit(option_glow, option_rect)
            
            option_text = self.font_medium.render(option, True, color)
            option_rect = option_text.get_rect(center=(WINDOW_WIDTH // 2, y_pos))
            self.screen.blit(option_text, option_rect)
        
        # Instructions
        instruction_text = self.font_small.render("Use UP/DOWN arrows and SPACE to select", True, DARK_BLUE)
        instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH // 2, menu_y + menu_height - 30))
        self.screen.blit(instruction_text, instruction_rect)
    
    def draw_how_to_play(self):
        # Clear screen with black background
        self.screen.fill(BLACK)
        
        # Draw border effect
        for i in range(5):
            color_intensity = 255 - (i * 40)
            glow_color = (0, color_intensity // 3, color_intensity)
            pygame.draw.rect(self.screen, glow_color, 
                           (30 - i, 30 - i,
                            WINDOW_WIDTH - 60 + (i * 2), WINDOW_HEIGHT - 60 + (i * 2)), 2)
        
        # Title
        title_text = self.font_large.render("HOW TO PLAY", True, NEON_BLUE)
        title_glow = self.font_large.render("HOW TO PLAY", True, GLOW_BLUE)
        
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
        glow_rect = title_glow.get_rect(center=(WINDOW_WIDTH // 2 + 2, 82))
        
        self.screen.blit(title_glow, glow_rect)
        self.screen.blit(title_text, title_rect)
        
        # Instructions sections
        sections = [
            ("OBJECTIVE:", NEON_PINK, [
                "• Control the neon snake to eat food and grow",
                "• Each food item gives you 10 points",
                "• Try to achieve the highest score possible!"
            ]),
            ("CONTROLS:", NEON_BLUE, [
                "• Arrow Keys or WASD - Move the snake",
                "• P or SPACE - Pause the game",
                "• ESC - Quit anytime"
            ]),
            ("RULES:", BRIGHT_GREEN, [
                "• Avoid hitting the walls",
                "• Don't run into your own body",
                "• Snake grows longer with each food eaten",
                "• Game gets harder as you grow!"
            ])
        ]
        
        y_offset = 140
        for section_title, title_color, items in sections:
            # Section title
            section_text = self.font_medium.render(section_title, True, title_color)
            section_rect = section_text.get_rect(x=100, y=y_offset)
            self.screen.blit(section_text, section_rect)
            y_offset += 40
            
            # Section items
            for item in items:
                item_text = self.font_small.render(item, True, WHITE)
                item_rect = item_text.get_rect(x=120, y=y_offset)
                self.screen.blit(item_text, item_rect)
                y_offset += 25
            
            y_offset += 15  # Extra space between sections
        
        # Back button
        if not hasattr(self, 'back_button'):
            self.back_button = Button(WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT - 100, 150, 40, "BACK TO MENU", self.font_small, "back")
        
        self.back_button.draw(self.screen)
    
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
        
        # Draw pause instruction
        pause_text = self.font_tiny.render("P: PAUSE", True, DARK_BLUE)
        self.screen.blit(pause_text, (WINDOW_WIDTH - 80, 20))
    
    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text with glow
        game_over_text = self.font_large.render("GAME OVER", True, NEON_PINK)
        game_over_glow = self.font_large.render("GAME OVER", True, WHITE)
        
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 120))
        glow_rect = game_over_glow.get_rect(center=(WINDOW_WIDTH // 2 + 2, WINDOW_HEIGHT // 2 - 118))
        
        self.screen.blit(game_over_glow, glow_rect)
        self.screen.blit(game_over_text, game_over_rect)
        
        # Final score
        final_score_text = self.font_medium.render(f"FINAL SCORE: {self.score}", True, NEON_BLUE)
        final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 70))
        self.screen.blit(final_score_text, final_score_rect)
        
        # Create game over buttons if they don't exist
        if not hasattr(self, 'game_over_buttons'):
            self.game_over_buttons = [
                Button(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 20, 200, 45, "PLAY AGAIN", self.font_medium, "play_again"),
                Button(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 40, 200, 45, "MAIN MENU", self.font_medium, "main_menu"),
                Button(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 100, 200, 45, "QUIT GAME", self.font_medium, "quit")
            ]
        
        # Draw buttons
        for button in self.game_over_buttons:
            button.draw(self.screen)
    
    def handle_events(self):
        self.mouse_pos = pygame.mouse.get_pos()
        
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
                
                elif self.game_state == "how_to_play":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.menu_sound.play()
                        self.game_state = "start_menu"
                        self.buttons = []  # Reset buttons
                
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
                        elif event.key == pygame.K_p or event.key == pygame.K_SPACE:
                            self.game_state = "paused"
                            self.pause_menu_selection = 0
                    else:
                        # Game over keyboard shortcuts
                        if event.key == pygame.K_SPACE:
                            self.menu_sound.play()
                            self.reset_game()
                            self.game_state = "intro"
                        elif event.key == pygame.K_r:
                            self.menu_sound.play()
                            self.game_state = "start_menu"
                            self.buttons = []  # Reset buttons
                
                elif self.game_state == "paused":
                    if event.key == pygame.K_UP:
                        self.pause_menu_selection = (self.pause_menu_selection - 1) % 3
                        self.menu_sound.play()
                    elif event.key == pygame.K_DOWN:
                        self.pause_menu_selection = (self.pause_menu_selection + 1) % 3
                        self.menu_sound.play()
                    elif event.key == pygame.K_SPACE:
                        if self.pause_menu_selection == 0:  # Resume
                            self.game_state = "playing"
                            self.menu_sound.play()
                        elif self.pause_menu_selection == 1:  # Toggle Music
                            self.toggle_music()
                            self.menu_sound.play()
                        elif self.pause_menu_selection == 2:  # Main Menu
                            self.game_state = "start_menu"
                            self.buttons = []  # Reset buttons
                            self.menu_sound.play()
                    elif event.key == pygame.K_p:
                        self.game_state = "playing"
            
            # Handle mouse clicks for buttons
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == "start_menu" and self.buttons:
                    for button in self.buttons:
                        if button.handle_event(event, self.mouse_pos):
                            self.menu_sound.play()
                            if button.action == "start":
                                self.game_state = "intro"
                                self.intro_timer = 0
                            elif button.action == "how_to_play":
                                self.game_state = "how_to_play"
                            elif button.action == "quit":
                                return False
                
                elif self.game_state == "how_to_play":
                    if hasattr(self, 'back_button') and self.back_button.handle_event(event, self.mouse_pos):
                        self.menu_sound.play()
                        self.game_state = "start_menu"
                        self.buttons = []  # Reset buttons
                
                elif self.game_state == "playing" and self.game_over:
                    if hasattr(self, 'game_over_buttons'):
                        for button in self.game_over_buttons:
                            if button.handle_event(event, self.mouse_pos):
                                self.menu_sound.play()
                                if button.action == "play_again":
                                    self.reset_game()
                                    self.game_state = "intro"
                                elif button.action == "main_menu":
                                    self.game_state = "start_menu"
                                    self.buttons = []  # Reset buttons
                                elif button.action == "quit":
                                    return False
        
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
            # Update button hover states
            if self.buttons:
                for button in self.buttons:
                    button.hovered = button.rect.collidepoint(self.mouse_pos)
        elif self.game_state == "how_to_play":
            self.draw_how_to_play()
            # Update back button hover state
            if hasattr(self, 'back_button'):
                self.back_button.hovered = self.back_button.rect.collidepoint(self.mouse_pos)
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
                # Update game over button hover states
                if hasattr(self, 'game_over_buttons'):
                    for button in self.game_over_buttons:
                        button.hovered = button.rect.collidepoint(self.mouse_pos)
        elif self.game_state == "paused":
            # Draw the game in background (frozen)
            self.screen.fill(BLACK)
            self.draw_border()
            self.draw_ui()
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            
            # Draw pause menu overlay
            self.draw_pause_menu()
        
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
        print("- Arcade-style background music (Press M to mute/unmute)")
        print("- Sound effects for eating, game over, and menu interactions")
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
