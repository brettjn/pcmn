#!/usr/bin/env python3
"""
PCMN - A Pacman Clone
Use arrow keys to control Pacman and collect all dots while avoiding ghosts!
"""

import pygame
import random
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 20
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 184, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 184, 82)
DARK_BLUE = (0, 0, 150)

# Direction enum
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

# Maze layout (1 = wall, 0 = dot, 2 = power pellet, 3 = empty space)
MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 2, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 2, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 3, 1, 1, 3, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 3, 1, 1, 3, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 3, 1, 1, 1, 3, 3, 1, 1, 1, 3, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 3, 1, 3, 3, 3, 3, 3, 3, 1, 3, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 3, 1, 3, 3, 3, 3, 3, 3, 1, 3, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 2, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 2, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class Pacman:
    """The player character"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.speed = 0.15
        self.mouth_open = 0
        self.mouth_direction = 1
        
    def update(self, maze):
        # Try to change direction
        new_x = self.x + self.next_direction.value[0] * self.speed
        new_y = self.y + self.next_direction.value[1] * self.speed
        
        if not self.is_wall(new_x, new_y, maze):
            self.direction = self.next_direction
        
        # Move in current direction
        new_x = self.x + self.direction.value[0] * self.speed
        new_y = self.y + self.direction.value[1] * self.speed
        
        if not self.is_wall(new_x, new_y, maze):
            self.x = new_x
            self.y = new_y
        
        # Animate mouth
        self.mouth_open += self.mouth_direction * 5
        if self.mouth_open >= 45:
            self.mouth_direction = -1
        elif self.mouth_open <= 0:
            self.mouth_direction = 1
    
    def is_wall(self, x, y, maze):
        # Check if position collides with wall
        tile_x = int(x)
        tile_y = int(y)
        
        # Check corners of pacman's hitbox
        corners = [
            (tile_x, tile_y),
            (int(x + 0.4), tile_y),
            (tile_x, int(y + 0.4)),
            (int(x + 0.4), int(y + 0.4))
        ]
        
        for cx, cy in corners:
            if cy < 0 or cy >= len(maze) or cx < 0 or cx >= len(maze[0]):
                return True
            if maze[cy][cx] == 1:
                return True
        return False
    
    def draw(self, screen):
        pixel_x = int(self.x * TILE_SIZE)
        pixel_y = int(self.y * TILE_SIZE)
        radius = TILE_SIZE // 2
        
        # Draw Pacman as a circle with mouth
        pygame.draw.circle(screen, YELLOW, (pixel_x + radius, pixel_y + radius), radius)
        
        # Draw mouth based on direction
        angle_offset = {
            Direction.RIGHT: 0,
            Direction.DOWN: 90,
            Direction.LEFT: 180,
            Direction.UP: 270
        }
        offset = angle_offset[self.direction]
        
        # Draw black triangles for mouth
        mouth_angle = self.mouth_open
        if mouth_angle > 0:
            center = (pixel_x + radius, pixel_y + radius)
            import math
            angle1 = math.radians(offset + mouth_angle)
            angle2 = math.radians(offset - mouth_angle)
            
            p1 = center
            p2 = (center[0] + radius * math.cos(angle1), center[1] + radius * math.sin(angle1))
            p3 = (center[0] + radius * math.cos(angle2), center[1] + radius * math.sin(angle2))
            
            pygame.draw.polygon(screen, BLACK, [p1, p2, p3])


class Ghost:
    """Enemy ghost character"""
    def __init__(self, x, y, color, personality):
        self.x = x
        self.y = y
        self.color = color
        self.direction = random.choice(list(Direction))
        self.speed = 0.08
        self.personality = personality  # Affects movement behavior
        self.scared = False
        self.scared_timer = 0
        
    def update(self, maze, pacman_x, pacman_y):
        if self.scared:
            self.scared_timer -= 1
            if self.scared_timer <= 0:
                self.scared = False
        
        # Choose direction based on personality
        if random.randint(0, 20) == 0 or self.is_wall(
            self.x + self.direction.value[0] * self.speed,
            self.y + self.direction.value[1] * self.speed,
            maze
        ):
            self.choose_direction(maze, pacman_x, pacman_y)
        
        # Move
        new_x = self.x + self.direction.value[0] * self.speed
        new_y = self.y + self.direction.value[1] * self.speed
        
        if not self.is_wall(new_x, new_y, maze):
            self.x = new_x
            self.y = new_y
    
    def choose_direction(self, maze, pacman_x, pacman_y):
        possible_directions = []
        
        for direction in Direction:
            new_x = self.x + direction.value[0] * self.speed * 2
            new_y = self.y + direction.value[1] * self.speed * 2
            if not self.is_wall(new_x, new_y, maze):
                possible_directions.append(direction)
        
        if not possible_directions:
            return
        
        if self.scared:
            # Run away from Pacman
            self.direction = random.choice(possible_directions)
        elif random.randint(0, 100) < self.personality:
            # Chase Pacman
            distances = []
            for direction in possible_directions:
                new_x = self.x + direction.value[0]
                new_y = self.y + direction.value[1]
                dist = ((new_x - pacman_x) ** 2 + (new_y - pacman_y) ** 2) ** 0.5
                distances.append((dist, direction))
            
            distances.sort(key=lambda x: x[0])
            self.direction = distances[0][1]
        else:
            # Random movement
            self.direction = random.choice(possible_directions)
    
    def is_wall(self, x, y, maze):
        tile_x = int(x)
        tile_y = int(y)
        
        corners = [
            (tile_x, tile_y),
            (int(x + 0.4), tile_y),
            (tile_x, int(y + 0.4)),
            (int(x + 0.4), int(y + 0.4))
        ]
        
        for cx, cy in corners:
            if cy < 0 or cy >= len(maze) or cx < 0 or cx >= len(maze[0]):
                return True
            if maze[cy][cx] == 1:
                return True
        return False
    
    def draw(self, screen):
        pixel_x = int(self.x * TILE_SIZE)
        pixel_y = int(self.y * TILE_SIZE)
        radius = TILE_SIZE // 2
        
        color = BLUE if self.scared else self.color
        
        # Body
        pygame.draw.circle(screen, color, (pixel_x + radius, pixel_y + radius), radius)
        pygame.draw.rect(screen, color, (pixel_x, pixel_y + radius, TILE_SIZE, radius))
        
        # Wavy bottom
        for i in range(4):
            x = pixel_x + i * (TILE_SIZE // 4)
            y = pixel_y + TILE_SIZE
            pygame.draw.circle(screen, color, (x + TILE_SIZE // 8, y), TILE_SIZE // 8)
        
        # Eyes
        eye_color = WHITE
        pupil_color = BLACK if not self.scared else RED
        
        pygame.draw.circle(screen, eye_color, (pixel_x + 6, pixel_y + 8), 3)
        pygame.draw.circle(screen, eye_color, (pixel_x + 14, pixel_y + 8), 3)
        pygame.draw.circle(screen, pupil_color, (pixel_x + 6, pixel_y + 8), 2)
        pygame.draw.circle(screen, pupil_color, (pixel_x + 14, pixel_y + 8), 2)


class Game:
    """Main game class"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PCMN - Pacman Clone")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.reset_game()
    
    def reset_game(self):
        self.maze = [row[:] for row in MAZE]  # Deep copy
        self.pacman = Pacman(14, 23)
        self.ghosts = [
            Ghost(12, 14, RED, 80),      # Aggressive (Blinky)
            Ghost(14, 14, PINK, 60),     # Moderate (Pinky)
            Ghost(13, 14, CYAN, 40),     # Less aggressive (Inky)
            Ghost(15, 14, ORANGE, 50),   # Mixed (Clyde)
        ]
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.win = False
        self.dots_remaining = sum(row.count(0) + row.count(2) for row in self.maze)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.pacman.next_direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.pacman.next_direction = Direction.DOWN
                elif event.key == pygame.K_LEFT:
                    self.pacman.next_direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.pacman.next_direction = Direction.RIGHT
                elif event.key == pygame.K_r and (self.game_over or self.win):
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        if self.game_over or self.win:
            return
        
        # Update Pacman
        self.pacman.update(self.maze)
        
        # Check dot collection
        tile_x = int(self.pacman.x + 0.2)
        tile_y = int(self.pacman.y + 0.2)
        
        if 0 <= tile_y < len(self.maze) and 0 <= tile_x < len(self.maze[0]):
            if self.maze[tile_y][tile_x] == 0:
                self.maze[tile_y][tile_x] = 3
                self.score += 10
                self.dots_remaining -= 1
            elif self.maze[tile_y][tile_x] == 2:
                self.maze[tile_y][tile_x] = 3
                self.score += 50
                self.dots_remaining -= 1
                # Make ghosts scared
                for ghost in self.ghosts:
                    ghost.scared = True
                    ghost.scared_timer = 300
        
        # Check win condition
        if self.dots_remaining == 0:
            self.win = True
        
        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(self.maze, self.pacman.x, self.pacman.y)
            
            # Check collision with Pacman
            dist = ((ghost.x - self.pacman.x) ** 2 + (ghost.y - self.pacman.y) ** 2) ** 0.5
            if dist < 0.5:
                if ghost.scared:
                    # Eat ghost
                    ghost.x = 14
                    ghost.y = 14
                    ghost.scared = False
                    self.score += 200
                else:
                    # Lose life
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                    else:
                        # Reset positions
                        self.pacman.x = 14
                        self.pacman.y = 23
                        for i, g in enumerate(self.ghosts):
                            g.x = 12 + i
                            g.y = 14
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw maze
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                pixel_x = x * TILE_SIZE
                pixel_y = y * TILE_SIZE
                
                if cell == 1:  # Wall
                    pygame.draw.rect(self.screen, BLUE, (pixel_x, pixel_y, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(self.screen, DARK_BLUE, (pixel_x + 2, pixel_y + 2, TILE_SIZE - 4, TILE_SIZE - 4))
                elif cell == 0:  # Dot
                    pygame.draw.circle(self.screen, WHITE, (pixel_x + TILE_SIZE // 2, pixel_y + TILE_SIZE // 2), 2)
                elif cell == 2:  # Power pellet
                    pygame.draw.circle(self.screen, WHITE, (pixel_x + TILE_SIZE // 2, pixel_y + TILE_SIZE // 2), 5)
        
        # Draw ghosts
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        
        # Draw Pacman
        self.pacman.draw(self.screen)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, SCREEN_HEIGHT - 40))
        
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (200, SCREEN_HEIGHT - 40))
        
        # Draw game over or win message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, RED)
            restart_text = self.small_font.render("Press R to restart or ESC to quit", True, WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 20))
        
        if self.win:
            win_text = self.font.render("YOU WIN!", True, YELLOW)
            restart_text = self.small_font.render("Press R to restart or ESC to quit", True, WHITE)
            self.screen.blit(win_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 20))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 20))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
