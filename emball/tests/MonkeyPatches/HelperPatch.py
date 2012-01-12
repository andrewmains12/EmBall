import pygame

"""Contains monkey patches for functions in Helpers.py"""


def load_image (img_path):
    """Patch load image to not call surface.convert"""
    try:
        surface = pygame.image.load(img_path)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%
                         (img_path, pygame.get_error()))
    return surface
