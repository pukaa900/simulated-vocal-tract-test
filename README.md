# Simulated Vocal Tract

This repository contains a small Pygame application that demonstrates a simple vocal tract simulation using chained formant filters.

## Requirements
- Python 3.12+
- pygame
- numpy

Install dependencies:

```bash
pip install pygame numpy
```

## Running

Set the SDL audio driver to `dummy` if your environment lacks audio hardware:

```bash
SDL_AUDIODRIVER=dummy python3 vocal_tract.py
```

Use the arrow keys to change the vowel and pitch:
- Left/Right: cycle through vowels `a, e, i, o, u`
- Up/Down: raise or lower the pitch
- ESC: quit the program
