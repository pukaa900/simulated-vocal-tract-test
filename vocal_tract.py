import math
import numpy as np
import pygame

# Fa'amatalaga o le fa'ata'ita'iga
SAMPLE_RATE = 44100
CHUNK_SIZE = 512

# Fa'amaumauga o foliga o le gutu mo voka fa'avae
VOWELS = {
    'a': [700, 1100, 2500, 3500],
    'e': [500, 2000, 2600, 3500],
    'i': [300, 2500, 3200, 3500],
    'o': [400,  800, 2600, 3500],
    'u': [350,  700, 2600, 3500],
}
BANDWIDTH = 100

class FormantFilter:
    def __init__(self, freq):
        r = math.exp(-math.pi * BANDWIDTH / SAMPLE_RATE)
        theta = 2 * math.pi * freq / SAMPLE_RATE
        self.a0 = 1 - r
        self.b1 = 2 * r * math.cos(theta)
        self.b2 = -r * r
        self.s1 = 0.0
        self.s2 = 0.0

    def process(self, x):
        y = np.empty_like(x)
        s1 = self.s1
        s2 = self.s2
        for i, sample in enumerate(x):
            y[i] = self.a0 * sample + self.b1 * s1 + self.b2 * s2
            s2 = s1
            s1 = y[i]
        self.s1 = s1
        self.s2 = s2
        return y

def generate_glottal(num_samples, freq, phase):
    t = (phase + freq / SAMPLE_RATE * np.arange(num_samples)) % 1.0
    out = 2.0 * t - 1.0
    phase = (phase + freq / SAMPLE_RATE * num_samples) % 1.0
    return out, phase

def create_filters(vowel_key):
    freqs = VOWELS[vowel_key]
    return [FormantFilter(f) for f in freqs]

pygame.mixer.pre_init(SAMPLE_RATE, size=-16, channels=1, buffer=CHUNK_SIZE)
pygame.init()

screen = pygame.display.set_mode((600, 200))
pygame.display.set_caption('Faataitaiga Leo')
font = pygame.font.SysFont(None, 24)

pitch = 120.0
vowel = 'a'
phase = 0.0
filters = create_filters(vowel)
channel = pygame.mixer.Channel(0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                pitch += 10
            elif event.key == pygame.K_DOWN:
                pitch = max(50, pitch - 10)
            elif event.key == pygame.K_RIGHT:
                keys = list(VOWELS.keys())
                vowel = keys[(keys.index(vowel) + 1) % len(keys)]
                filters = create_filters(vowel)
            elif event.key == pygame.K_LEFT:
                keys = list(VOWELS.keys())
                vowel = keys[(keys.index(vowel) - 1) % len(keys)]
                filters = create_filters(vowel)

    # Fausia se vaega fou o leo
    glottal, phase = generate_glottal(CHUNK_SIZE, pitch, phase)
    y = glottal
    for f in filters:
        y = f.process(y)
    # fa'aitiitia ma fa'avasega le leo
    audio = np.int16(np.clip(y * 20000, -32768, 32767))
    sound = pygame.sndarray.make_sound(audio)
    if not channel.get_busy():
        channel.play(sound)
    else:
        channel.queue(sound)

    screen.fill((30, 30, 30))
    text = f'Voka: {vowel}  Fati: {int(pitch)} Hz'
    img = font.render(text, True, (255, 255, 255))
    screen.blit(img, (20, 80))
    info = 'Faaaoga ki arrow ma ESC e tapuni'
    img2 = font.render(info, True, (255, 255, 255))
    screen.blit(img2, (20, 110))
    pygame.display.flip()

pygame.quit()
