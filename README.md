# 🐍 Neon Snake Game

A classic Snake game with a retro neon arcade aesthetic built with Python and Pygame.

## Features

- **Start Menu**: Welcome screen with game instructions and neon styling
- **Animated Intro**: "Get Ready" sequence with countdown before gameplay
- **Classic Snake Gameplay**: Control a snake that grows as it eats food
- **Neon Arcade Styling**: Bright blue and pink colors with glowing effects
- **Sound Effects**: Eating sounds, game over audio, and menu interaction sounds
- **Collision Detection**: Game ends when hitting walls or the snake's own body
- **Scoring System**: Earn 10 points for each food item consumed
- **Game Over Screen**: Shows final score with restart and menu options
- **Smooth Controls**: Use arrow keys or WASD for movement

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

1. Run the game:
   ```bash
   python snake_game.py
   ```

2. **Start Menu Controls**:
   - SPACE to start the game
   - ESC to quit

3. **Game Controls**:
   - Arrow keys or WASD to move the snake
   - Any key to skip intro sequence
   - SPACE to restart after game over
   - M to return to main menu from game over
   - ESC to quit anytime

4. **Objective**: 
   - Eat the white food squares to grow your snake and increase your score
   - Avoid hitting the walls or your own body
   - Try to achieve the highest score possible!

## Game Flow

1. **Start Menu**: Displays game title, instructions, and controls
2. **Intro Sequence**: Animated "Get Ready" screen with 3-second countdown
3. **Gameplay**: Classic snake action with neon visual effects
4. **Game Over**: Shows final score with options to restart or return to menu

## Game Elements

- **Snake Head**: Bright blue with glow effect
- **Snake Body**: Bright green segments
- **Food**: White squares with pink glow
- **Border**: Neon blue with outer glow effect
- **UI**: Neon-styled text with glow effects
- **Menus**: Animated borders and glowing text elements

## Technical Details

- Built with Python and Pygame
- 800x600 window resolution
- 20x20 pixel grid cells
- 10 FPS game speed for classic feel
- Neon color palette for retro arcade aesthetic
- State-based game management (menu, intro, playing, game over)

Enjoy the game! 🎮✨
