import pygame

class Button:
    def __init__(self, text, x, y, width, height, callback):
        # Pastikan x, y, width, height adalah nilai integer
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.default_color = (255, 182, 193)  # Warna default
        self.hover_color = (255, 105, 180)    # Warna ketika hover
        self.color = self.default_color

    def draw(self, surface):
        # Gambar tombol
        pygame.draw.rect(surface, self.color, self.rect, border_radius=12)
        
        # Render teks pada tombol
        font = pygame.font.SysFont("comicsansms", 36)
        text_render = font.render(self.text, True, (255, 255, 255))  # Teks putih
        text_rect = text_render.get_rect(center=self.rect.center)  # Posisi teks di tengah tombol
        surface.blit(text_render, text_rect)

    def handle_event(self, event):
        # Menangani event mouse
        mouse_pos = pygame.mouse.get_pos()
        
        # Cek apakah mouse berada di dalam tombol
        if self.rect.collidepoint(mouse_pos):
            self.color = self.hover_color  # Ganti warna ketika hover
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Ketika tombol kiri mouse diklik
                self.callback()  # Jalankan fungsi callback
        else:
            self.color = self.default_color  # Kembali ke warna default jika tidak hover
