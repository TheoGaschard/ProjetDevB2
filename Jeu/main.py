import random, os.path
import pygame
from pygame.locals import *
from Classes.Player import Player
from Classes.Alien import Alien
from Classes.Bomb import Bomb
from Classes.Explosion import Explosion
from Classes.Shot import Shot
from Utils.Constants import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")


def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'Data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs


def main(winstyle = 0):
    pygame.init()
    winstyle = 0
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    img = load_image('player1.gif')
    Player.images = [img, pygame.transform.flip(img, 1, 0)]
    img = load_image('explosion1.gif')
    Explosion.images = [img, pygame.transform.flip(img, 1, 1)]
    Alien.images = load_images('alien1.gif')
    Bomb.images = [load_image('bomb.gif')]
    Shot.images = [load_image('shot.gif')]

    icon = pygame.transform.scale(Alien.images[0], (32, 32))
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Pygame Aliens')
    pygame.mouse.set_visible(0)

    bgdtile = load_image('background.gif')
    background = pygame.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0,0))
    pygame.display.flip()

    aliens = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()
    lastalien = pygame.sprite.GroupSingle()

    Player.containers = all
    Alien.containers = aliens, all, lastalien
    Shot.containers = shots, all
    Bomb.containers = bombs, all
    Explosion.containers = all

    alienreload = ALIEN_RELOAD
    kills = 0
    clock = pygame.time.Clock()

    player = Player()
    Alien()


    while player.alive():

        #get input
        for event in pygame.event.get():
            if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
        keystate = pygame.key.get_pressed()

        # clear/erase the last drawn sprites
        all.clear(screen, background)

        #update all the sprites
        all.update()

        #handle player input
        direction = keystate[K_RIGHT] - keystate[K_LEFT]
        player.move(direction)
        firing = keystate[K_SPACE]
        if not player.reloading and firing and len(shots) < MAX_SHOTS:
            Shot(player.gunpos())
        player.reloading = firing

        # Create new alien
        if alienreload:
            alienreload = alienreload - 1
        elif not int(random.random() * ALIEN_ODDS):
            Alien()
            alienreload = ALIEN_RELOAD

        # Drop bombs
        if lastalien and not int(random.random() * BOMB_ODDS):
            Bomb(lastalien.sprite)

        # Detect collisions
        for alien in pygame.sprite.spritecollide(player, aliens, 1):
            Explosion(alien)
            Explosion(player)
            player.kill()

        for alien in pygame.sprite.groupcollide(shots, aliens, 1, 1).keys():
            Explosion(alien)

        for bomb in pygame.sprite.spritecollide(player, bombs, 1):
            Explosion(player)
            Explosion(bomb)
            player.kill()

        #draw the scene
        dirty = all.draw(screen)
        pygame.display.update(dirty)

        #cap the framerate
        clock.tick(40)

    if pygame.mixer:
        pygame.mixer.music.fadeout(1000)
    pygame.time.wait(1000)
    pygame.quit()



#call the "main" function if running this script
if __name__ == '__main__': main()