import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game objects
class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Paddle(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 100, BLACK)
        self.speed = 5

    def move_up(self):
        self.rect.y -= self.speed
        if self.rect.top < 0:
            self.rect.top = 0

    def move_down(self):
        self.rect.y += self.speed
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Ball(GameObject):
    def __init__(self):
        super().__init__(WIDTH // 2, HEIGHT // 2, 10, 10, BLACK)
        self.speed_x = 5 * random.choice((1, -1))
        self.speed_y = 5 * random.choice((1, -1))

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = 5 * random.choice((1, -1))
        self.speed_y = 5 * random.choice((1, -1))

# Create game objects
player_paddle = Paddle(50, HEIGHT // 2 - 50)
computer_paddle = Paddle(WIDTH - 60, HEIGHT // 2 - 50)
ball = Ball()

all_sprites = pygame.sprite.Group(player_paddle, computer_paddle, ball)

# Game variables
clock = pygame.time.Clock()
player_score = 0
computer_score = 0
font = pygame.font.Font(None, 36)

def save_scores():
    with open("pong_scores.txt", "a") as file:
        file.write(f"Player: {player_score} | Computer: {computer_score}\n")

def reset_game():
    global player_score, computer_score
    player_score = 0
    computer_score = 0
    ball.reset()

def game_loop():
    global player_score, computer_score

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_paddle.move_up()
        if keys[pygame.K_DOWN]:
            player_paddle.move_down()
        if keys[pygame.K_ESCAPE]:
            end_screen()
            break

        # Computer AI
        if computer_paddle.rect.centery < ball.rect.centery:
            computer_paddle.move_down()
        elif computer_paddle.rect.centery > ball.rect.centery:
            computer_paddle.move_up()

        # Ball movement and collision
        ball.update()

        if pygame.sprite.collide_rect(ball, player_paddle) or pygame.sprite.collide_rect(ball, computer_paddle):
            ball.speed_x *= -1
            
        # Scoring
        if ball.rect.left <= 0 :
            computer_score += 1
            ball.reset()
            text = font.render(f"Computer Scored", True, BLACK)
            screen.blit(text,(WIDTH // 2 - 100, HEIGHT // 2 - 50))
            pygame.display.flip()
            clock.tick(60)

            time.sleep(1)
        elif ball.rect.right >= WIDTH :
            player_score += 1
            ball.reset()
            text = font.render(f"Player Scored", True, BLACK)
            screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
            pygame.display.flip()
            clock.tick(60)

            time.sleep(1)  # Delay after goal

        # Drawing
        screen.fill(WHITE)
        pygame.draw.circle(screen,BLACK,(WIDTH//2,HEIGHT//2),WIDTH//4,2)
        pygame.draw.line(screen,BLACK,(WIDTH//2,0),(WIDTH//2,HEIGHT))
        all_sprites.draw(screen)

        # Display scores
        player_text = font.render(f"{player_score}", True, BLACK)
        computer_text = font.render(f"{computer_score}", True, BLACK)
        screen.blit(player_text, (WIDTH//2 - 50, HEIGHT//2))
        screen.blit(computer_text, (WIDTH//2 + 50, HEIGHT//2))

        pygame.display.flip()
        clock.tick(60)

        # Check for game end
        if player_score >= 5 or computer_score >= 5:
            save_scores()
            end_screen()
            break

def end_screen():
    global player_score, computer_score

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return

        screen.fill(BLACK)
        winner_text = font.render("",True,WHITE)
        if player_score > computer_score:
            winner_text = font.render("You Win!", True, WHITE)
        elif computer_score > player_score:
            winner_text = font.render("Computer Wins!", True, WHITE)
        restart_text = font.render("Press 'R' to restart or 'Q' to quit", True, WHITE)
        screen.blit(winner_text, (WIDTH // 2 - 50, HEIGHT // 2 - 50))
        screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))
        pygame.display.flip()

if __name__ == "__main__":
    while True:
        game_loop()
        if not pygame.get_init():
            break

pygame.quit()
