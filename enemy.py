import pygame
import os
import random

# Kelas Musuh Umum
class Enemy:
    def __init__(self, screen_width, screen_height, image_path, dead_image_path, hp):
        # Muat dan scale gambar musuh hidup
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.mask = pygame.mask.from_surface(self.image)

        # Muat dan scale gambar musuh mati
        self.dead_image = pygame.image.load(dead_image_path).convert_alpha()
        self.dead_image = pygame.transform.scale(self.dead_image, (300, 300))

        # Inisialisasi posisi
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(screen_width, screen_width + 300)
        self.rect.y = random.randint(0, screen_height - self.rect.height)

        self.speed = 5
        self.alive = True
        self.hp = hp  # HP yang ditentukan

        self.death_timer = 0
        self.DEATH_DURATION = 60  # 60 frame (~1 detik jika 60 FPS)
        self.score_awarded = False  # Tambahkan atribut ini
    def update(self, meowchi):
        if not self.alive:
            if self.death_timer > 0:
                self.death_timer -= 1
            return

        # Update posisi musuh, bergerak ke kiri
        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.alive = False
            self.death_timer = 0  # Langsung hilang jika keluar layar

    def draw(self, screen, debug=False):
        if self.alive:
            screen.blit(self.image, self.rect)
        elif self.death_timer > 0:
            screen.blit(self.dead_image, self.rect)

        if debug:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

    def take_damage(self):
        self.hp -= 1
        if self.hp <= 0 and self.alive:
            self.alive = False
            self.death_timer = self.DEATH_DURATION
            return True  # Musuh mati
            return False  # Musuh masih hidup

# Kelas Tikus
class TikusDapur(Enemy):
    def __init__(self, screen_width, screen_height):
        image_path = os.path.join("Assets/tikus/tikus.png")
        dead_image_path = os.path.join("Assets/tikus/tikus_mati.png")
        super().__init__(screen_width, screen_height, image_path, dead_image_path, hp=1)


class TikusPutih(Enemy):
    def __init__(self, screen_width, screen_height):
        image_path = os.path.join("Assets/tikus/tikusputih.png")
        dead_image_path = os.path.join("Assets/tikus/tikusputih_mati.png")
        super().__init__(screen_width, screen_height, image_path, dead_image_path, hp=2)
