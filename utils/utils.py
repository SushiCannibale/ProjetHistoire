import pygame as pg

def draw_text(surface, text, size, pos, color, align, fontname):
    """
    Draws text on a surface
    """
    font = pg.font.Font(fontname, size)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    if align in ['up', 'u']:
        text_rect.midtop = pos
    if align in ['down', 'd']:
        text_rect.midbottom = pos
    if align in ['left', 'l']:
        text_rect.midleft = pos
    if align in ['right', 'r']:
        text_rect.midright = pos

    if align in ['upleft', 'ul']:
        text_rect.topleft = pos
    if align in ['upright', 'ur']:
        text_rect.topright = pos
    if align in ['downleft', 'dl']:
        text_rect.bottomleft = pos
    if align in ['downright', 'dr']:
        text_rect.bottomright = pos

    if align in ['center', 'c']:
        text_rect.center = pos

    surface.blit(text_surf, text_rect)

def get_rect_from_text(text, size, fontname):
    return pg.font.Font(fontname, size).render(text, True, pg.Color("white")).get_rect()
