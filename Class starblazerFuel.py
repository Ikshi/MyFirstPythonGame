# Pygame template - skeleton for a new pygame project
import pygame
import random
from os import path

img_file = path.join(path.dirname(__file__),'img')

WIDTH = 600
HEIGHT = 480
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Starblazer")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, False, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

def newenemy():
    e = enemies()
    all_sprites.add(e)
    Enemies.add(e)

def draw_shield_bar(surf,x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x,y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 40 * i
        img_rect.y = y
        surf.blit(img, img_rect)

fuel = 500
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(80,80))
        #self.image = pygame.transform.flip(player_img, True, False)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 25
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH - 560
        self.rect.bottom = HEIGHT / 2
        self.speedx = 0
        self.speedy = 0
        
        self.fuel = 3000
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        

    def update(self):
        #unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.center = (WIDTH - 560, HEIGHT/2)
        self.speedx = 0
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.speedx = -10
                    self.speedy = 0
                    
                if event.key == pygame.K_RIGHT:
                    self.speedx = 10
                    self.speedy = 0
                    
                self.rect.x += self.speedx
                if self.rect.right > WIDTH:
                    self.rect.right = WIDTH
                if self.rect.left < 0:
                    self.rect.left = 0
                if event.key == pygame.K_DOWN:
                    self.speedy = 10
                    self.speedx = 0
                    
                if event.key == pygame.K_UP:
                    self.speedy = -10
                    self.speedx = 0
                    
                self.rect.y += self.speedy
                if self.rect.bottom > HEIGHT:
                    self.rect.bottom = HEIGHT
                if self.rect.top < 55:
                    self.rect.top = 55

    def shoot(self):
        bullet = Bullet(self.rect.right, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def hide(self):
        #hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class enemies(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_img,(60,50))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(580,WIDTH)
        self.rect.y = random.randrange(60,400)
        self.speedx = random.randrange(1,5)


    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right < -900 :
            self.rect.x = random.randrange(580,WIDTH)
            self.rect.y = random.randrange(45,400)
            self.speedx = random.randrange(1,5)
     

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img,(30,15))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speedx = 10

    def update(self):
        self.rect.x += self.speedx
        #Kill if it moves off the right of the screen
        if self.rect.left > WIDTH:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 10 #How long we wait for the next frame to appear

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Plane(pygame.sprite.Sprite):
    def __init__(self):
         pygame.sprite.Sprite.__init__(self)
         self.image = pygame.transform.scale(plane_img,(45,30))
         self.image.set_colorkey(WHITE)
         self.rect = self.image.get_rect()
         self.rect.left = 0
         self.rect.top = 45
         #self.rect.x = random.randrange(0,1)
         #self.rect.y = random.randrange(45,46)
         self.speedx = 4

    def update(self):
        self.rect.x += self.speedx
        if self.rect.centerx ==  WIDTH / 2+10:
            self.refuel()
        if self.rect.left > 1200 :
            #self.rect.x = random.randrange(0,1)
            #self.rect.y = random.randrange(45,46)
            self.rect.left = 0
            self.rect.top = 45
            self.speedx = 4

    def refuel(self):
        para = Para(self.rect.centerx, self.rect.bottom)
        all_sprites.add(para)
        parachute.add(para)
        
class Para(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img,(30,15))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.top = y
        self.rect.centerx = x
        self.speedy = 5
        self.speedx = 2

    def update(self):
        self.rect.y += self.speedy
        self.rect.x -= self.speedx
        #Kill if it moves off the right of the screen
        if self.rect.top > HEIGHT - 50:
            self.kill()

def show_go_screen():
    draw_text(screen, "Starblazer", 64, WIDTH/2, HEIGHT /4)
    draw_text(screen, "Arrow keys to move, space to fire, b to bomb", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT* 3 /4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

            
# Load all game graphics
background = pygame.image.load(path.join(img_file,"bg.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_file,"player.png")).convert()
player_mini_img = pygame.transform.scale(player_img,(50, 30))
player_mini_img.set_colorkey(WHITE)
bullet_img = pygame.image.load(path.join(img_file,"bullet.png")).convert()
enemy_img = pygame.image.load(path.join(img_file,"Enemy.png")).convert()
plane_img = pygame.image.load(path.join(img_file,"plane.png")).convert()

#Explosion Effects
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(17):
    filename = '1_{}.png'.format(i)
    img = pygame.image.load(path.join(img_file, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (100,100))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (50,50))
    explosion_anim['sm'].append(img_sm)
    filename = 'B1_{}.png'.format(i)
    img = pygame.image.load(path.join(img_file, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)



    
##


#Score
score = 0

# Game loop
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        Enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        parachute = pygame.sprite.Group()
        plane = Plane()
        all_sprites.add(plane)
        for i in range(5):
            newenemy()
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
                player.speedy = 0
                player.speedx = 0
                

    # Update
    all_sprites.update()

    #Decrease Fuel
    if player.fuel > 0:
        
        player.fuel -= 1
        

    #Check fuel 
    elif player.fuel <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.fuel = 3000
    
    # check if a bullet hit an enemy
    hits = pygame.sprite.groupcollide(Enemies, bullets, True, True)
    for hit in hits:
        score += 1
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newenemy()
    
    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, Enemies, True, pygame.sprite.collide_circle)
    for hit in hits:
        
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newenemy()
        
        death_explosion = Explosion(player.rect.center, 'player')
        all_sprites.add(death_explosion)
            #player.kill() #kill remove it from any groups
        player.hide()
        player.lives -= 1
           
        newenemy()

           

    #check to see if player hit fuelbox
    hits = pygame.sprite.spritecollide(player, parachute, True, pygame.sprite.collide_circle)
    for hit in hits:
        if hit:
            player.fuel += 10

    
    #if the player died and the explosion has finished playing
    if player.lives == 0 and not death_explosion.alive():
        game_over = True
        #running = False
        

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str("Score:"), 30, 50, 10)
    draw_text(screen, str(score), 30, 100, 12)
    draw_text(screen, str("Fuel:"), 30, 150, 10)
    draw_text(screen, str(player.fuel), 30, 210, 12)
    
    draw_lives(screen, WIDTH - 150, 15, player.lives, player_mini_img)
    
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
