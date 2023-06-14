import pygame

class Fighter():
    def __init__(self,player, x, y, flip, data, sprite_sheet, animation_steps):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
        self.frame_index = 0       
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attacking = False
        self.hit = False
        self.health = 100
        self.alive = True

    def load_images(self, sprite_sheet, animation_steps):
        #extract images from sprite sheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_image = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size) 
                temp_img_list.append(pygame.transform.scale(temp_image, (self.size*self.image_scale, self.size*self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list    


    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        #get keypress
        key = pygame.key.get_pressed()
        # can only do when not attacking
        if self.attacking == False and self.alive == True and round_over == False:
        #check player 1 control
            if self.player == 2:
            #movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True

                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True

                #jump
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                
                #attack
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(target)
                    #determine which attack was used
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2

        #check player 2 control
            if self.player == 1:
            #movement
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True

                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True

                #jump
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                
                #attack
                if key[pygame.K_f] or key[pygame.K_t]:
                    self.attack(target)
                    #determine which attack was used
                    if key[pygame.K_f]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2



        #apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y    


            #ensure player is on Screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left  
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right  
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom 

        # ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True      

        # apply attack cooldown
        if self.attack_cooldown >0:
            self.attack_cooldown -= 1
        #update player position    
        self.rect.x += dx
        self.rect.y += dy


    #handle animation updates
    def update(self):
        #Check what action player is performing
        if self.health <= 0:
            self.health == 0
            self.alive = False
            self.update_action(6)
        elif self.hit == True :
            self.update_action(5)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)#3:attack1
            elif self.attack_type == 2:
                self.update_action(4)#4:attack2      
        elif self.jump == True :
            self.update_action(2) #jump  
        elif self.running == True :
            self.update_action(1)#1:run
        else:
            self.update_action(0)#0:idle

        animation_cooldown = 50 
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            #check if animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            #if player is dead animation ends
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0   
                #check if attacking is used
                if self.action == 3 or self.action == 4:
                    self.attacking = False 
                    self.attack_cooldown = 20

                #check if Damage is dealt
                if self.action == 5:
                    self.hit = False
                #if palyer in middle of attack,attacking is stopped
                    self.attacking = False
                    self.attack_cooldown = 20 

    def attack(self, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(self.rect.centerx - (2* self.rect.width * self.flip), self.rect.y, 2* self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True    

    def update_action(self, new_action):
        #check if the new acrion is different than previous one 
        if new_action != self.action:
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)    
        surface.blit(img, (self.rect.x - (self.offset[0]* self.image_scale), self.rect.y - (self.offset[1]*self.image_scale)))
