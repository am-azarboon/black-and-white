import pygame
import random
from time import sleep
import sys


#Load all pygame modules
pygame.init()

#Main colors
white_c = (255, 255, 255)
black_c = (0, 0, 0)

#Imgs
menu_screen = pygame.image.load("assets/imgs/s_menue.png")
gameOver_screen = pygame.image.load("assets/imgs/Game_over.png")
icon_img = pygame.image.load("assets/imgs/main.png")

#Dispaly width, height
display_width, display_height = 340, 600

#Create game display
g_display = pygame.display.set_mode((display_width, display_height))

#Set caption and icon
pygame.display.set_caption("Black And White", "guy")
pygame.display.set_icon(icon_img)

#Set game clock
game_clock = pygame.time.Clock()
#---------------------------------

#--Draw branch rects func--
def branch_generator(side):
    #Check for side
    if side == 0:
        return [0, -200, 70, 20] #Left-wall side
    elif side == 1:
        return [100, -200, 70, 20] #Left side
    elif side == 2:
        return [170, -200, 70, 20] #Right side
    else:
        return [270, -200, 70, 20] #Right wall side

#--Move branchs and count points--
def move_branch(branch_list, counter):
    #Check score to increase the speed(Just 2 times because of performance)
    if counter > 100:
        speed = 6
    elif counter > 200:
        speed = 7
    else:
        speed = 5

    #Move every branch that exist
    for branch in branch_list:
        branch[1] += speed

        if branch[1] > 600:
            counter += 1

    #Delete old branches from branch list
    new_branches = [branch for branch in branch_list if branch[1] <= 600]
    return new_branches, counter

#--Load branches--
def load_branch(branch_list):
    for branch in branch_list:
        #Check for side to choose color
        if branch[0] <= 100:
            pygame.draw.rect(g_display, black_c, tuple(branch))
        else:
            pygame.draw.rect(g_display, white_c, tuple(branch))

#--Check for colision
def colision_check(branch_list, guy_x):
    #Check for colision
    for branch in branch_list:
        if branch[1] + 20 >= 500 and branch[1] <= 522:
            if branch[0] + 70 > guy_x  and branch[0] < guy_x + 22:
                sleep(2)
                return True

#--Couting the scores
def score_counter(counter):
    font = pygame.font.Font("assets/font/Terono.ttf", 20)
    score_txt = font.render(str(int(counter / 2)), True, white_c, None)

    g_display.blit(score_txt, (310, 10))
    

#--Main Game def--
def main():
    #Start flag
    flag = False
    game_over = False

    #Guy position
    x_pos = 2
    guy_x = 170

    #Choice Branch side
    side = random.choice((0, 1))

    #Brachs
    branch_list = []

    #Score counter
    counter = 0

    #Set userEvent by timer to creat branches
    branch_creater1 = pygame.USEREVENT
    pygame.time.set_timer(branch_creater1, 600)

    branch_creater2 = pygame.USEREVENT
    pygame.time.set_timer(branch_creater2, 700)

    #Game loop
    while True:
        #Events Block
        for event in pygame.event.get():
            #Event quit
            if event.type == pygame.QUIT:
                #Quit game
                pygame.quit()
                sys.exit()
            
            #Event branch_creator1
            if event.type == branch_creater1 and flag:
                side = random.randint(0, 3)
                branch_list.append(branch_generator(side))

            # Event branch_creator2
            if event.type == branch_creater2 and flag:
                side = random.randint(0, 3)
                branch_list.append(branch_generator(side))
            
            #Event key donw
            if event.type == pygame.KEYDOWN:
                #Check for start menu
                if event.key == pygame.K_SPACE:
                    flag = True
                
                #Check for restart
                if event.key == pygame.K_r and game_over:
                    game_over = False
                    #Reset branch list and score
                    branch_list.clear()
                    counter = 0

                #Event Move left
                if event.key == pygame.K_LEFT and x_pos > 0:
                    x_pos -= 1

                #Event Move Right
                if event.key == pygame.K_RIGHT and x_pos < 3:
                    x_pos += 1

        #Draw white & Black side
        pygame.draw.rect(g_display, white_c, (0, 0, 170, 600))
        pygame.draw.rect(g_display, black_c, (170, 0, 170, 600))
        
        #Check if start flag is true
        if flag:
            if not game_over:
                #Check for valid position of guy
                if x_pos == 0:
                    guy_x = 0
                    pygame.draw.rect(g_display, black_c, (guy_x, 500, 22, 22))
                elif x_pos == 1:
                    guy_x = 148
                    pygame.draw.rect(g_display, black_c, (guy_x, 500, 22, 22))
                elif x_pos == 2:
                    guy_x = 170
                    pygame.draw.rect(g_display, white_c, (guy_x, 500, 22, 22))
                else:
                    guy_x = 318
                    pygame.draw.rect(g_display, white_c, (guy_x, 500, 22, 22))

                #Call to move branches
                branch_list, counter = move_branch(branch_list, counter)
                
                #Call to load new branches
                load_branch(branch_list)

                #Call to check collision
                game_over = colision_check(branch_list, guy_x)

                #Call to show score
                score_counter(counter)

            else: #ELSE display gameover screen
                g_display.blit(gameOver_screen, (0, 0))
                
                #Blit counter on gameover screen
                font = pygame.font.Font("assets/font/Terono.ttf", 24)
                score_txt = font.render(str(int(counter / 2)), True, white_c, None)
                g_display.blit(score_txt, (300, 14))

        else: #ELSE display start menu screen
            g_display.blit(menu_screen, (0, 0))
        
        #Update game display
        pygame.display.update()
        game_clock.tick(60) #Game tick(fps)

#Main game
if __name__ == "__main__":
    main()