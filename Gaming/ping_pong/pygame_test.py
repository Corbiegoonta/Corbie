import pygame
import random

def ping_pong():

    pygame.init()
    screen_dimensions = (640, 480)
    ball_size = 10
    padel_size = (10, 60)
    pygame.display.set_caption("Ping Pong Game")
    screen = pygame.display.set_mode(screen_dimensions)
    clock = pygame.time.Clock()

    ball_pos = [0.5*screen_dimensions[0], 0.5*screen_dimensions[1]]
    ball_speed = [2, 2]

    player1_rect = pygame.Rect(screen_dimensions[0]-screen_dimensions[0], 200, padel_size[0], padel_size[1])
    player2_rect = pygame.Rect(screen_dimensions[0]-10, 200, padel_size[0], padel_size[1])

    player1_score = 0
    player2_score = 0

    bias_list = [-1, 1]
    running = True
    paused = True
    while running:
        # if if_continue is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with black
        screen.fill((0, 0, 0))

        my_font = pygame.font.SysFont('Comic Sans MS', 25)
        text_surface = my_font.render(f'Player1: {player1_score} | Player 2: {player2_score}', False, (255, 255, 255))
        screen.blit(text_surface, (screen_dimensions[0]*0.5-(text_surface.get_size()[0]*0.5),0))
        print(text_surface.get_size())

        # Draw the ball
        ball = pygame.draw.circle(screen, (255, 255, 255), (int(ball_pos[0]), int(ball_pos[1])), ball_size)
        player1 = pygame.draw.rect(screen, (255, 255, 255), player1_rect)
        player2 = pygame.draw.rect(screen, (255, 255, 255), player2_rect)
        ball_list = [ball]
        player_list = [player1, player2]

        pygame.display.update()
            
        keys = pygame.key.get_pressed()

        pygame.display.flip()
        clock.tick(60)

        if paused and (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_d] or keys[pygame.K_a]):
            print("Game Started!")
            paused = False
            bias = 0
            bias_applied0 = random.choice(bias_list)
            bias_applied1 = random.choice(bias_list)
        elif paused:
            ball_pos = [0.5*screen_dimensions[0], 0.5*screen_dimensions[1]]
            ball_speed = [2, 2]
            player1_rect = pygame.Rect(screen_dimensions[0]-screen_dimensions[0], 200, padel_size[0], padel_size[1])
            player2_rect = pygame.Rect(screen_dimensions[0]-10, 200, padel_size[0], padel_size[1])
            bias = 0
            bias_applied0 = random.choice(bias_list)
            bias_applied1 = random.choice(bias_list)
        else:
            if keys[pygame.K_RIGHT]:
                if player1_rect.y < screen_dimensions[1] - padel_size[1]:
                    player1_rect = player1.move(0, 10)
                else:
                    pass
            if keys[pygame.K_LEFT]:
                if player1_rect.y > 0:
                    player1_rect = player1.move(0, -10)
                else:
                    pass      
            if keys[pygame.K_d]:
                if player2_rect.y < screen_dimensions[1] - padel_size[1]:
                    player2_rect = player2.move(0, 10)
                else:
                    pass
            if keys[pygame.K_a]:
                if player2_rect.y > 0:
                    player2_rect = player2.move(0, -10)
                else:
                    pass                        

            # Update ball position
            if bias == 0:
                ball_pos[0] += ball_speed[0]*bias_applied0
                ball_pos[1] += ball_speed[1]*bias_applied1
            elif bias == 1:
                ball_pos[0] += ball_speed[0]
                ball_pos[1] += ball_speed[1]*random.choice(bias_list)
            elif bias == 2:
                ball_pos[0] += ball_speed[0]*bias_list[0]
                ball_pos[1] += ball_speed[1]*random.choice(bias_list)
            else:
                pass

            # Bounce off walls
            if ball_pos[0] <= 0 or ball_pos[0] >= screen_dimensions[0]:
                ball_speed[0] = -ball_speed[0]
            if ball_pos[1] <= 0 or ball_pos[1] >= screen_dimensions[1]:
                ball_speed[1] = -ball_speed[1]

            # Check for collisions
            for paddle in player_list:
                if ball.colliderect(paddle):
                    ball_speed[0] = -ball_speed[0]
                    # Optional: Adjust ball speed based on where it hit the paddle
                    offset = (ball.centery - paddle.centery) / (padel_size[1] / 2)
                    ball_speed[1] += offset * 2
            if ball_pos[0] <= 0:
                print("Player 2 Scores!")
                player2_score += 1
                bias = 2
                paused = True
                print(f"Player 1 Score: {player1_score} | Player 2 Score: {player2_score}")
                if player1_score > 0 and player2_score > 0:
                    player2_win_rate = player2_score / (player1_score + player2_score)
                    player1_win_rate = player1_score / (player1_score + player2_score)
                    print(f"Player 1 Win Rate: {player1_win_rate} | Player 2 Win Rate: {player2_win_rate}")
                    
            if ball_pos[0] >= screen_dimensions[0]:
                print("Player 1 Scores!")
                player1_score += 1
                bias = 1
                paused = True
                print(f"Player 1 Score: {player1_score} | Player 2 Score: {player2_score}")
                if player1_score > 0 and player2_score > 0:
                    player2_win_rate = player2_score / (player1_score + player2_score)
                    player1_win_rate = player1_score / (player1_score + player2_score)
                    print(f"Player 1 Win Rate: {player1_win_rate} | Player 2 Win Rate: {player2_win_rate}")
                    

            # Update the display
            

    pygame.quit()
        # else:
        #     pass
    
class pong:
    def __init__(self, player1_name, player2_name):

        game_start = ping_pong()
        self.player1 = pygame.Rect(50, 200, 10, 60)
        self.player2 = pygame.Rect(630, 200, 10, 60)

if __name__ == "__main__":
    ping_pong()