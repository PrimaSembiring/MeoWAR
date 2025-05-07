import pygame
import random
from meowchi import Meowchi
from enemy import TikusDapur, TikusPutih
from button import Button

class Game:
    def __init__(self, screen, WIDTH, HEIGHT):
        self.screen = screen
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.meowchi = Meowchi(200, 400)
        self.enemies = []
        self.spawn_delay = 60
        self.spawn_timer = 0

        self.score = 0
        self.font = pygame.font.SysFont(None, 72)
        self.win = False

        self.next_button = Button("NEXT", WIDTH - 160, HEIGHT - 80, 140, 50, self.next_level)
        self.next_level_callback = None  # Callback dari luar jika diperlukan

    def set_next_level_callback(self, callback):
        self.next_level_callback = callback

    def spawn_enemy(self):
        if random.random() < 0.7:
            enemy = TikusDapur(self.WIDTH, self.HEIGHT)
        else:
            enemy = TikusPutih(self.WIDTH, self.HEIGHT)
        self.enemies.append(enemy)

    def update(self):
        if self.win:
            return  # Tidak update game jika sudah menang

        # Update background scrolling
        self.bg_x -= self.bg_speed
        if self.bg_x <= -self.WIDTH:
            self.bg_x = 0

        # Update posisi dan aksi Meowchi
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.meowchi.follow_mouse(mouse_x, mouse_y)
        self.meowchi.update()

        # Spawn musuh secara periodik
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_timer = 0
            self.spawn_enemy()

        # Update pergerakan masing-masing musuh
        for enemy in self.enemies:
            enemy.update(self.meowchi)

        # Collision detection: cek setiap peluru untuk tiap musuh
        for bullet in self.meowchi.bullets[:]:
            for enemy in self.enemies:
                if enemy.alive and bullet.check_collision(enemy):
            # Berikan damage satu kali per hit
                    if enemy.take_damage():
                # Tambahkan skor hanya jika musuh mati
                        if not enemy.score_awarded:
                            self.score += 10
                        enemy.score_awarded = True
                    
            # Hapus peluru setelah mengenai musuh
            if bullet in self.meowchi.bullets:
                self.meowchi.bullets.remove(bullet)
            # Peluru hanya mengenai satu musuh
            break

        # Buang musuh yang sudah benar-benar tidak aktif kecuali jika masih dalam animasi kematian
        self.enemies = [e for e in self.enemies if e.alive or e.death_timer > 0]

        # Cek kondisi menang, misalnya jika skor mencapai 100
        if self.score >= 100 and not self.win:
            self.win = True

    def draw(self):
        # Gambar background dua kali untuk membuat efek scrolling
        self.screen.blit(self.background, (self.bg_x, 0))
        self.screen.blit(self.background, (self.bg_x + self.WIDTH, 0))

        # Gambar Meowchi
        self.meowchi.draw(self.screen)
        # Gambar semua musuh
        for enemy in self.enemies:
            enemy.draw(self.screen)

        # Tampilkan skor
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.WIDTH - 250, 30))

        # Jika menang, tampilkan pesan dan tombol level selanjutnya
        if self.win:
            win_text = self.font.render("YOU WIN", True, (255, 255, 0))
            text_rect = win_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            self.screen.blit(win_text, text_rect)
            self.next_button.draw(self.screen)

    def handle_event(self, event):
        if self.win:
            self.next_button.handle_event(event)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.meowchi.shoot(pygame.mouse.get_pos())

    def next_level(self):
        if self.next_level_callback:
            self.next_level_callback()