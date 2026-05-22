# my version of the chimp game, with a score system, a timer, and a difficulty selection at the start.


# Import Modules
import os
import pygame as pg

try:
    import pygame.examples.chimp
    main_dir = os.path.split(pygame.examples.chimp.__file__)[0]
except ImportError:
    main_dir = os.path.split(os.path.abspath(__file__))[0]

data_dir = os.path.join(main_dir, "data")

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")


def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    sound = pg.mixer.Sound(fullname)

    return sound


# FONCTIONNALITÉ 1 : SAUVEGARDE DU SCOREBOARD (Shahil Ahmed Rahman)
def save_score(score):
    with open("scores.txt", "a") as f:
        f.write(f"Score: {score}\n")
        
class Fist(pg.sprite.Sprite):
    

    def __init__(self):
        pg.sprite.Sprite.__init__(self) 
        self.image, self.rect = load_image("fist.png", -1)
        self.fist_offset = (-235, -80)
        self.punching = False

    def update(self):
       
        pos = pg.mouse.get_pos()
        self.rect.topleft = pos
        self.rect.move_ip(self.fist_offset)
        if self.punching:
            self.rect.move_ip(15, 25)

    def punch(self, target):
        
        if not self.punching:
            self.punching = True
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        self.punching = False


class Chimp(pg.sprite.Sprite):
    
    def __init__(self, speed=30):
        pg.sprite.Sprite.__init__(self) 
        self.image, self.rect = load_image("chimp.png", -1, 4)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 90
        self.move = speed  
        self.dizzy = False
        self.cooldown = 0   

    def _walk(self):
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pg.transform.flip(self.image, True, False)
        self.rect = newpos

    def _spin(self):
        newpos = self.rect.move((self.move, 0))
        if self.rect.left < self.area.left or self.rect.right > self.area.right:
            self.move = -self.move
            newpos = self.rect.move((self.move, 0))
        self.rect = newpos

        center = self.rect.center
        self.dizzy += 12
        if self.dizzy >= 360:
            self.dizzy = False
            self.image = self.original
            self.cooldown = 90         
        else:
            self.image = pg.transform.rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def punched(self):
        if not self.dizzy and self.cooldown == 0:  
            self.dizzy = True
            self.original = self.image


def main():
    speed_difficulty = {
        1: 15,
        2: 30,
        3: 55
    }
    
    MENU = """Veuillez choisir une difficulte :
    1. Facile
    2. Moyen
    3. Difficile
    """
    choice = input(MENU)
    while choice not in ["1", "2", "3"]:
        print("Choix invalide. Veuillez entrer 1, 2 ou 3.")
        choice = input(MENU)
    chimp_speed = speed_difficulty[int(choice)]
    pg.init()
    screen = pg.display.set_mode((1280, 480), pg.SCALED)
    pg.display.set_caption("Monkey Fever")
    pg.mouse.set_visible(False)
    
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((170, 238, 187))

    if pg.font:
        font = pg.font.Font(None, 64)
        text = font.render("Pummel The Chimp, And Win $$$", True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
        background.blit(text, textpos)

    screen.blit(background, (0, 0))
    pg.display.flip()

    whiff_sound = load_sound("whiff.wav")
    punch_sound = load_sound("punch.wav")
    chimp = Chimp(speed=chimp_speed)
    fist = Fist()
    allsprites = pg.sprite.RenderPlain((chimp, fist))
    clock = pg.time.Clock()

    GAME_DURATION = 60         
    start_ticks = pg.time.get_ticks()

    score_data = {"highest": 0}
    current_score = 0

    def check_high_score():
        if current_score > score_data["highest"]:
                score_data["highest"] = current_score

    going = True
    while going:
        clock.tick(60)

        elapsed = (pg.time.get_ticks() - start_ticks) / 1000
        time_left = max(0, GAME_DURATION - int(elapsed))
        if time_left == 0:
            check_high_score()
            save_score(score_data["highest"])
            going = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                check_high_score()
                save_score(score_data["highest"])
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                check_high_score()
                save_score(score_data["highest"])
                going = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play()  
                    chimp.punched()
                    current_score += 1 
                else:
                    whiff_sound.play() 
                    check_high_score()
                    current_score = 0
            elif event.type == pg.MOUSEBUTTONUP:
                fist.unpunch()

        allsprites.update()

    
        screen.blit(background, (0, 0))
        allsprites.draw(screen)

        
        if pg.font:
            score_font = pg.font.Font(None, 36)
            score_text = score_font.render(f"Current Score: {current_score}  |  High Score: {score_data['highest']}", True, (10, 10, 10))
            score_pos = score_text.get_rect(centerx=background.get_width() / 2, y=70)
            screen.blit(score_text, score_pos)

            timer_color = (200, 0, 0) if time_left <= 10 else (10, 10, 10)
            timer_font = pg.font.Font(None, 52)
            timer_text = timer_font.render(f"Time: {time_left}s", True, timer_color)
            timer_pos = timer_text.get_rect(centerx=background.get_width() / 2, y=420)
            screen.blit(timer_text, timer_pos)

        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()
