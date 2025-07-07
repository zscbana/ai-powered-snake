# 🐍 Neon Snake Game

A classic Snake game with a retro neon arcade aesthetic built with Python and Pygame, featuring modern UI elements and comprehensive audio-visual effects.

## Features

- **Start Menu**: Welcome screen with styled arcade buttons and neon effects
- **How to Play Screen**: Dedicated instructions screen with organized game rules
- **Animated Intro**: "Get Ready" sequence with countdown before gameplay
- **Classic Snake Gameplay**: Control a snake that grows as it eats food
- **Neon Arcade Styling**: Bright blue and pink colors with multi-layered glowing effects
- **Pause Menu**: In-game pause with resume, music toggle, and menu options
- **Background Music**: Arcade-style looping music with synthetic sound generation
- **Sound Effects**: Eating sounds, game over audio, and menu interaction sounds
- **Styled Button System**: Interactive buttons with hover effects and click animations
- **Mouse & Keyboard Support**: Full control via both input methods
- **Collision Detection**: Game ends when hitting walls or the snake's own body
- **Scoring System**: Earn 10 points for each food item consumed
- **Game Over Screen**: Shows final score with styled action buttons
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
   - Click "START GAME" button or press SPACE to begin
   - Click "HOW TO PLAY" button for detailed instructions
   - Click "QUIT" button or press ESC to exit

3. **Game Controls**:
   - Arrow keys or WASD to move the snake
   - P or SPACE to pause the game
   - Any key to skip intro sequence
   - ESC to quit anytime

4. **Pause Menu**:
   - Use UP/DOWN arrows to navigate options
   - SPACE to select: Resume Game, Toggle Music, or Main Menu
   - P to resume directly

5. **Game Over Options**:
   - Click "PLAY AGAIN" or press SPACE for new game
   - Click "MAIN MENU" or press R to return to start
   - Click "QUIT GAME" or press ESC to exit

6. **Objective**: 
   - Eat the white food squares to grow your snake and increase your score
   - Avoid hitting the walls or your own body
   - Try to achieve the highest score possible!

## Game Flow

1. **Start Menu**: Interactive buttons with hover effects and game title
2. **How to Play**: Comprehensive instructions with organized sections
3. **Intro Sequence**: Animated "Get Ready" screen with 3-second countdown
4. **Gameplay**: Classic snake action with neon visual and audio effects
5. **Pause Menu**: Optional pause with music controls and navigation
6. **Game Over**: Final score display with styled restart options

## Visual Elements

- **Snake Head**: Bright blue with outer glow effect
- **Snake Body**: Bright green segments
- **Food**: White squares with pulsing pink glow
- **Game Border**: Multi-layered neon blue glowing border
- **UI Elements**: Neon-styled text with glow effects throughout
- **Buttons**: Arcade-themed with hover animations and click feedback
- **Backgrounds**: Animated border effects and semi-transparent overlays

## Audio Features

- **Background Music**: 8-second looping arcade melody with bass and harmony
- **Eating Sound**: Pleasant 800Hz sine wave with decay
- **Game Over Sound**: Descending tone from 400Hz to 100Hz
- **Menu Sounds**: Short click sounds for all interactions
- **Music Control**: Toggle mute/unmute via pause menu
- **Synthetic Generation**: All sounds created programmatically

## Technical Details

- **Built with**: Python 3.6+ and Pygame 2.0+
- **Dependencies**: pygame, numpy (for sound generation)
- **Window Size**: 800x600 pixels
- **Game Grid**: 20x20 pixel cells
- **Frame Rate**: 10 FPS for classic arcade feel
- **Color Palette**: Neon blue (#00FFFF), neon pink (#FF1493), bright green (#39FF14)
- **State Management**: Menu → How-to-Play → Intro → Playing → Paused → Game Over
- **Input Support**: Full mouse and keyboard integration
- **Sound System**: Pygame mixer with synthetic audio generation

## Controls Reference

| Action | Keyboard | Mouse |
|--------|----------|-------|
| Start Game | SPACE | Click "START GAME" |
| How to Play | - | Click "HOW TO PLAY" |
| Move Snake | Arrow Keys / WASD | - |
| Pause Game | P or SPACE | - |
| Resume Game | P or SPACE | - |
| New Game | SPACE (game over) | Click "PLAY AGAIN" |
| Main Menu | R (game over) | Click "MAIN MENU" |
| Quit Game | ESC | Click "QUIT" buttons |

## File Structure

```
AWS-Game/
├── snake_game.py          # Main game file with all classes and logic
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Development Notes

- **Modular Design**: Button class for reusable UI elements
- **State-Based Architecture**: Clean separation of game states
- **Synthetic Audio**: No external audio files required
- **Responsive UI**: Hover effects and visual feedback
- **Error Handling**: Graceful fallbacks for missing resources
- **Cross-Platform**: Works on Windows, macOS, and Linux

Enjoy the complete arcade experience! 🎮✨🐍
