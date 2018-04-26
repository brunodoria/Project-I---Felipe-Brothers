import pygame as pg
from .. import setup
from .. import constants as c


class Enemy(pg.sprite.Sprite):
    """Classe base para os inimigos"""
    def __init__(self):
        pg.sprite.Sprite.__init__(self)


    def setup_enemy(self, x, y, direction, name, setup_frames):
        """Inicializa algumas variaveis"""
        self.sprite_sheet = setup.GFX['smb_enemies_sheet']
        self.frames = []
        self.frame_index = 0
        self.animate_timer = 0
        self.death_timer = 0
        self.gravity = 1.5
        self.state = c.WALK

        self.name = name
        self.direction = direction
        setup_frames()

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.set_velocity()


    def set_velocity(self):
        """Velocidade de movimento"""
        if self.direction == c.LEFT:
            self.x_vel = -2
        else:
            self.x_vel = 2

        self.y_vel = 0


    def get_image(self, x, y, width, height):
        """Obtem as imagens das figuras maiores"""
        image = pg.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(c.BLACK)


        image = pg.transform.scale(image,
                                   (int(rect.width*c.SIZE_MULTIPLIER),
                                    int(rect.height*c.SIZE_MULTIPLIER)))
        return image


    def handle_state(self):
        """Estado dos inimigos"""
        if self.state == c.WALK:
            self.walking()
        elif self.state == c.FALL:
            self.falling()
        elif self.state == c.JUMPED_ON:
            self.jumped_on()
        elif self.state == c.SHELL_SLIDE:
            self.shell_sliding()
        elif self.state == c.DEATH_JUMP:
            self.death_jumping()


    def walking(self):
        """Movimento lateral"""
        if (self.current_time - self.animate_timer) > 125:
            if self.frame_index == 0:
                self.frame_index += 1
            elif self.frame_index == 1:
                self.frame_index = 0

            self.animate_timer = self.current_time


    def falling(self):
        """Movimento de queda"""
        if self.y_vel < 10:
            self.y_vel += self.gravity


    def jumped_on(self):
        """Indica inimigo derrotado"""
        pass


    def death_jumping(self):
        """Ainimacao para derrota"""
        self.rect.y += self.y_vel
        self.rect.x += self.x_vel
        self.y_vel += self.gravity

        if self.rect.y > 600:
            self.kill()


    def start_death_jump(self, direction):
        """Movimento de pulo na derrrota"""
        self.y_vel = -8
        if direction == c.RIGHT:
            self.x_vel = 2
        else:
            self.x_vel = -2
        self.gravity = .5
        self.frame_index = 3
        self.image = self.frames[self.frame_index]
        self.state = c.DEATH_JUMP


    def animation(self):
        """Figura para animacao"""
        self.image = self.frames[self.frame_index]


    def update(self, game_info, *args):
        """Atualiza estado"""
        self.current_time = game_info[c.CURRENT_TIME]
        self.handle_state()
        self.animation()




class Enemy1(Enemy):
# I's
    def __init__(self, y=c.GROUND_HEIGHT, x=0, direction=c.LEFT, name='enemy1_'):
        Enemy.__init__(self)
        self.setup_enemy(x, y, direction, name, self.setup_frames)


    def setup_frames(self):
        """Imagens correspondentes"""

        self.frames.append(
            self.get_image(0, 4, 16, 16))
        self.frames.append(
            self.get_image(30, 4, 16, 16))
        self.frames.append(
            self.get_image(61, 0, 16, 16))
        self.frames.append(pg.transform.flip(self.frames[1], False, True))


    def jumped_on(self):
        """Inimigo pisado"""
        self.frame_index = 2

        if (self.current_time - self.death_timer) > 500:
            self.kill()



class Enemy2(Enemy):
# D's
    def __init__(self, y=c.GROUND_HEIGHT, x=0, direction=c.LEFT, name='enemy2_'):
        Enemy.__init__(self)
        self.setup_enemy(x, y, direction, name, self.setup_frames)


    def setup_frames(self):
        """Imagens correspondentes"""
        self.frames.append(
            self.get_image(150, 0, 16, 24))
        self.frames.append(
            self.get_image(180, 0, 16, 24))
        self.frames.append(
            self.get_image(360, 5, 16, 15))
        self.frames.append(pg.transform.flip(self.frames[2], False, True))


    def jumped_on(self):
        """Inimigo derrotado parcialmente"""
        self.x_vel = 0
        self.frame_index = 2
        shell_y = self.rect.bottom
        shell_x = self.rect.x
        self.rect = self.frames[self.frame_index].get_rect()
        self.rect.x = shell_x
        self.rect.bottom = shell_y


    def shell_sliding(self):
        """Deslize do conceito"""
        if self.direction == c.RIGHT:
            self.x_vel = 10
        elif self.direction == c.LEFT:
            self.x_vel = -10
