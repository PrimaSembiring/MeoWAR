import pygame
import sys
import random
from Game import Game
from button import Button
from meowchi import Meowchi
from enemy import TikusDapur, TikusPutih 

pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
WHITE = (255, 255, 255)
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("MeoWar")
clock = pygame.time.Clock()

title_font = pygame.font.SysFont("comicsansms", 72)
button_font = pygame.font.SysFont("comicsansms", 36)

menu_bg1 = pygame.image.load("Assets/Background/BG Level 1.png")
menu_bg2 = pygame.image.load("Assets/Background/background2.png")
menu_bg1 = pygame.transform.scale(menu_bg1, (WIDTH, HEIGHT))
menu_bg2 = pygame.transform.scale(menu_bg2, (WIDTH, HEIGHT))

class MainMenu:
    def __init__(self):
        self.buttons = [
            Button("Mulai Game", WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50, self.start_game),
            Button("Keluar", WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 50, self.quit_game)
        ]
        self.running = True
        self.bg_images = [menu_bg1, menu_bg2]
        self.current_bg_index = 0
        self.bg_x = 0
        self.scroll_speed = 1

    def start_game(self):
        game = GameManager(1)
        game.run()
        self.running = True

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def scroll_background(self):
        self.bg_x -= self.scroll_speed
        current_bg = self.bg_images[self.current_bg_index]
        next_bg = self.bg_images[(self.current_bg_index + 1) % len(self.bg_images)]
        
        screen.blit(current_bg, (self.bg_x, 0))
        screen.blit(next_bg, (self.bg_x + current_bg.get_width(), 0))
        
        if self.bg_x <= -current_bg.get_width():
            self.bg_x = 0
            self.current_bg_index = (self.current_bg_index + 1) % len(self.bg_images)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                for button in self.buttons:
                    button.handle_event(event)

            self.scroll_background()
            title = title_font.render("MeoWar", True, (255, 105, 180))
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
            for button in self.buttons:
                button.draw(screen)

            pygame.display.flip()
            clock.tick(60)

class GameManager: #noteeedd
    def __init__(self, level=1):
        self.level = level
        self.score = 0
        self.bg_image = pygame.image.load("Assets/Background/BG Level 1.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))
        self.bg_x = 0
        self.bg_speed = 3
        self.meowchi = Meowchi(200, HEIGHT // 2)

        if self.level == 1:
            self.tikus_list = [TikusDapur(WIDTH, HEIGHT) for _ in range(3)] + [TikusPutih(WIDTH, HEIGHT) for _ in range(2)]
        #elif self.level == 2:
        #    self.tikus_list = [Anjing(WIDTH, HEIGHT) for _ in range(3)]
        #elif self.level == 3:
        #    self.tikus_list = [Boss(WIDTH, HEIGHT)]

        self.running = True
        self.next_button = Button("NEXT", WIDTH - 150, HEIGHT - 100, 120, 50, self.next_level)
        self.show_next_button = False

    def next_level(self):
        if self.level < 3:
            self.level += 1
            self.score = 0
            self.run()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if self.show_next_button:
                    self.next_button.handle_event(event)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    target_pos = (WIDTH + 100, self.meowchi.rect.centery)
                    self.meowchi.shoot(target_pos)

            if self.score >= 100:
                self.show_next_button = True
                pygame.mouse.set_visible(True)
            else:
                pygame.mouse.set_visible(False)

                # Update karakter dan musuh hanya jika belum menang
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.meowchi.follow_mouse(mouse_x, mouse_y)
                self.meowchi.update()

                for tikus in self.tikus_list:
                    tikus.update(self.meowchi)
                    for bullet in self.meowchi.bullets:
                        if bullet.check_collision(tikus):
                            self.score += 5
                            break

                self.tikus_list = [tikus for tikus in self.tikus_list if tikus.alive or tikus.death_timer > 0]

                if len(self.tikus_list) < 5:
                    if self.level == 1:
                        self.tikus_list.append(random.choice([TikusDapur, TikusPutih])(WIDTH, HEIGHT))
                    #elif self.level == 2:
                    #    self.tikus_list.append(Anjing(WIDTH, HEIGHT))
                    #elif self.level == 3:
                    #    self.tikus_list.append(Boss(WIDTH, HEIGHT))

                self.bg_x -= self.bg_speed
                if self.bg_x <= -WIDTH:
                    self.bg_x = 0

            screen.blit(self.bg_image, (self.bg_x, 0))
            screen.blit(self.bg_image, (self.bg_x + WIDTH, 0))

            self.meowchi.draw(screen)
            for tikus in self.tikus_list:
                tikus.draw(screen)

            score_text = pygame.font.SysFont("comicsansms", 36).render(f"Score: {self.score}", True, (255, 255, 255))
            screen.blit(score_text, (280, 30))

            if self.show_next_button:
                win_text = pygame.font.SysFont("comicsansms", 72).render("YOU WIN", True, (255, 255, 255))
                screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 100))
                self.next_button.draw(screen)

            pygame.display.flip()
            clock.tick(60)

def main():
    menu = MainMenu()
    menu.run()

if __name__ == "__main__":
    main()
