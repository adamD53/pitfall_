from pygame import Vector2
import os

from image import Image

class Barrel(Image):
    def __init__(self, x: float, y: float) -> None:
        path = os.path.join("Sprites","Environment","Barrel","1.png")
        super().__init__(path, Vector2(x, y))
