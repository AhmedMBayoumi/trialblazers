import pygame
import random
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
bottom_panel = 150
screen_width = 1200 
screen_height = 600 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('TRAIL BLAZERS')


#define game variables
current_mage = 1
total_mages = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
potion_effect_wizard = 20
potion_effect_evvil_wizard = 10
clicked = False
game_over = 0


#define fonts
font = pygame.font.SysFont('Times New Roman', 26)

#define colours
red = (255, 0, 0)
green = (0, 255, 0)
#load music
music = pygame.mixer.music.load('medieval music.mp3')
#play music
pygame.mixer.music.play(-1)

#load images
#background image
background_img = pygame.image.load('assets/Background/background.png').convert_alpha()
background_img = pygame.transform.scale(background_img, (background_img.get_width()*(3/2), background_img.get_height()*(3/2)))
#panel image
panel_img = pygame.image.load('assets/Icons/panel.png').convert_alpha()
panel_img = pygame.transform.scale(panel_img, (panel_img.get_width()*(3/2), panel_img.get_height()))
#button images
potion_img = pygame.image.load('assets/Icons/potion.png').convert_alpha()
restart_img = pygame.image.load('assets/Icons/restart.png').convert_alpha()
#load victory and defeat images
victory_img = pygame.image.load('assets/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('assets/Icons/defeat.png').convert_alpha()
#sword image
sword_img = pygame.image.load('assets/Icons/sword.png').convert_alpha()


#create function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#function for drawing background
def draw_bg():
    screen.blit(background_img, (0, 0))


#function for drawing panel
def draw_panel():
    #draw panel rectangle
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    #show Wizard stats
    draw_text(f'{Wizard.name} HP: {Wizard.hp}', font, red, 100, screen_height - bottom_panel + 10)
    for count, i in enumerate(Evil_wizard_list):
        #show name and health
        draw_text(f'{i.name} HP: {i.hp}', font, red, 825, (screen_height - bottom_panel + 10) + count * 60)




#mage class
class mage():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0#0:idle, 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()
        #load idle images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'assets/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'assets/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load hurt images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'assets/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load death images
        temp_list = []
        for i in range(7):
            img = pygame.image.load(f'assets/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def animate(self):
        animation_cooldown = 100
        #handle animation
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out then reset back to the start
        if self.frame_index == len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()


    
    def idle(self):
        #set variables to idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def attack(self, target):
        #deal damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        #run enemy hurt animation
        target.hurt()
        #check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)
        #set variables to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        #set variables to hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        #set variables to death animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def reset (self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()


    def draw(self):
        screen.blit(self.image, self.rect)



class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp


    def draw(self, hp):
        #update with new health
        self.hp = hp
        #calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))



class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0


    def update(self):
        #move damage text up
        self.rect.y -= 1
        #delete the text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()



damage_text_group = pygame.sprite.Group()


Wizard = mage(170, 425, 'Wizard', 40, 8, 3)
Evil_wizard1 = mage(570, 400, 'Evil Wizard', 20, 6, 1)
Evil_wizard2 = mage(1075, 450, 'Evil Wizard', 20, 6, 1)

Evil_wizard_list = []
Evil_wizard_list.append(Evil_wizard1)
Evil_wizard_list.append(Evil_wizard2)

Wizard_health_bar = HealthBar(100, screen_height - bottom_panel + 40, Wizard.hp, Wizard.max_hp)
Evil_wizard1_health_bar = HealthBar(825, screen_height - bottom_panel + 40, Evil_wizard1.hp, Evil_wizard1.max_hp)
Evil_wizard2_health_bar = HealthBar(825, screen_height - bottom_panel + 100, Evil_wizard2.hp, Evil_wizard2.max_hp)  

#create buttons
potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = button.Button(screen, 550, 120, restart_img, 120, 30)

run = True
while run:

    clock.tick(fps)

    #draw background
    draw_bg()

    #draw panel
    draw_panel()
    Wizard_health_bar.draw(Wizard.hp)
    Evil_wizard1_health_bar.draw(Evil_wizard1.hp)
    Evil_wizard2_health_bar.draw(Evil_wizard2.hp)

    #draw mages
    Wizard.animate()
    Wizard.draw()
    for Evil_wizard in Evil_wizard_list:
        Evil_wizard.animate()
        Evil_wizard.draw()

    #draw the damage text
    damage_text_group.update()
    damage_text_group.draw(screen)

    #control player actions
    #reset action variables
    attack = False
    potion = False
    target = None
    #make sure mouse is visible
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, Evil_wizard in enumerate(Evil_wizard_list):
        if Evil_wizard.rect.collidepoint(pos):
            #hide mouse
            pygame.mouse.set_visible(False)
            #show sword in place of mouse cursor
            screen.blit(sword_img, pos)
            if clicked == True and Evil_wizard.alive == True:
                attack = True
                target = Evil_wizard_list[count]
    if potion_button.draw():
        potion = True
    #show number of potions remaining
    draw_text(str(Wizard.potions), font, red, 150, screen_height - bottom_panel + 70)


    if game_over == 0:
        #player action
        if Wizard.alive == True:
            if current_mage == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    #look for player action
                    #attack
                    if attack == True and target != None:
                        Wizard.attack(target)
                        current_mage += 1
                        action_cooldown = 0
                    #potion
                    if potion == True:
                        if Wizard.potions > 0:
                            #check if the potion would heal the player beyond max health
                            if Wizard.max_hp - Wizard.hp > potion_effect_wizard:
                                heal_amount = potion_effect_wizard
                            else:
                                heal_amount = Wizard.max_hp - Wizard.hp
                            Wizard.hp += heal_amount
                            Wizard.potions -= 1
                            damage_text = DamageText(Wizard.rect.centerx, Wizard.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_mage += 1
                            action_cooldown = 0
        else:
            game_over = -1


        #enemy action
        for count, Evil_wizard in enumerate(Evil_wizard_list):
            if current_mage == 2 + count:
                if Evil_wizard.alive == True:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        #check if Evil_wizard needs to heal first
                        if (Evil_wizard.hp / Evil_wizard.max_hp) < 0.5 and Evil_wizard.potions > 0:
                            #check if the potion would heal the Evil_wizard beyond max health
                            if Evil_wizard.max_hp - Evil_wizard.hp > potion_effect_evvil_wizard:
                                heal_amount = potion_effect_evvil_wizard
                            else:
                                heal_amount = Evil_wizard.max_hp - Evil_wizard.hp
                            Evil_wizard.hp += heal_amount
                            Evil_wizard.potions -= 1
                            damage_text = DamageText(Evil_wizard.rect.centerx, Evil_wizard.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_mage += 1
                            action_cooldown = 0
                        #attack
                        else:
                            Evil_wizard.attack(Wizard)
                            current_mage += 1
                            action_cooldown = 0
                else:
                    current_mage += 1

        #if all mages have had a turn then reset
        if current_mage > total_mages:
            current_mage = 1


    #check if all Evil_wizards are dead
    alive_Evil_wizard = 0
    for Evil_wizard in Evil_wizard_list:
        if Evil_wizard.alive == True:
            alive_Evil_wizard += 1
    if alive_Evil_wizard == 0:
        game_over = 1


    #check if game is over
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (470, 50))
        if game_over == -1:
            screen.blit(defeat_img, (500, 50))
        if restart_button.draw():
            Wizard.reset()
            for Evil_wizard in Evil_wizard_list:
                Evil_wizard.reset()
            current_mage = 1
            action_cooldown
            game_over = 0



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()