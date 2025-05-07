import pygame
import os
import math

class Bullet:
    def __init__(self, x, y, target_pos):
        image_path = os.path.join("Assets/bumbu/bumbu dapurr1.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (55, 55))
        self.rect = self.image.get_rect(center=(x, y))

        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 15

        dx = target_pos[0] - x
        dy = target_pos[1] - y
        distance = math.hypot(dx, dy)
        if distance == 0:
            distance = 1
        self.velocity = (dx / distance * self.speed, dy / distance * self.speed)

        self.alive = True
        self.hit = False  # Tambahan: peluru hanya bisa hit sekali

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # Hilangkan peluru jika keluar layar
        if (self.rect.right < 0 or self.rect.left > 1920 or
                self.rect.bottom < 0 or self.rect.top > 1080):
            self.alive = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, enemy):
        if self.hit:
            return False  # Sudah menabrak musuh sebelumnya

        # Pastikan hanya musuh hidup yang bisa ditabrak
        if not enemy.alive:
            return False

        # Buat mask jika belum ada
        if not hasattr(enemy, 'mask'):
            enemy.mask = pygame.mask.from_surface(enemy.image)

        offset = (enemy.rect.x - self.rect.x, enemy.rect.y - self.rect.y)
        if self.mask.overlap(enemy.mask, offset):
            enemy.take_damage()
            self.hit = True      # Tandai peluru sudah kena target
            self.alive = False   # Hapus peluru setelah kena
            return True
        return False