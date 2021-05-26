# import pygame library
import pygame
from pygame.constants import QUIT
import requests

screen = pygame.display.set_mode((800, 600))
level = "easy"

response = requests.get("https://sugoku.herokuapp.com/board?difficulty="+level)
grid = response.json()['board']
grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]

# Total window
#screen = pygame.display.set_mode((500, 600))
dif = 500/9
buffer= 2
#pygame.draw.line(screen, (5, 1, 1), (1 * dif-3, (1 + 1)*dif), (1 * dif + dif + 3, (1 + 1)*dif), 7)
def isEmpty(num):
    if(num == 0):
        return True
    return False
def isValid(position,num):
    for i in range(0,len(grid[0])):
        if(grid[position[0]][i] == num):
            return False
    for i in range(0,len(grid[0])):
        if(grid[i][position[1]] == num):
            return False  
    x = position[0]//3*3
    y = position[1]//3*3

    for i in range(0,3):
        for j in range(0,3):
            if(grid[x+i][y+j] == num):
                return False
    return True
solved=0
def sudoku_solver(screen):
    myfont = pygame.font.SysFont('Comic Sans MS',35)

    for i in range(0,len(grid[0])):
        for j in range(0,len(grid[0])):
            if(isEmpty(grid[i][j])):
                for k in range(1,10):
                    if isValid((i,j),k):
                        grid[i][j]=k
                        pygame.draw.rect(screen, (250,250,250), ((j+1)*50 + buffer, (i+1)*50+ buffer,50 -2*buffer , 50 - 2*buffer))

                        value = myfont.render(str(k),True ,(0,0,128))
                        screen.blit(value, (((j+1)*50+15,(i+1)*50)))
                        pygame.display.update()
                        pygame.time.delay(25)
                        sudoku_solver(screen)
                        global solved 
                        if(solved ==1):
                            return


                        grid[i][j] = 0

                        pygame.draw.rect(screen, (250,250,250), ((j+1)*50 + buffer, (i+1)*50+ buffer,50 -2*buffer , 50 - 2*buffer))


                        pygame.display.update()
                return 
    solved=1

def insert(screen , position):
    i, j = position[1] , position[0]
    myfont = pygame.font.SysFont('Comic Sans MS',35)
    while True:
      for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            return
        if event.type == pygame.KEYDOWN:
            if (grid_original[i-1][j-1] != 0):
                return
            if(event.key == 48):
                grid[i-1][j-1] = event.key -48
                pygame.draw.rect(screen, (250,250,250), (position[0]*50 + buffer, position[1]*50+ buffer,50 -2*buffer , 50 - 2*buffer))
                pygame.display.update()
                return
            if(0 < event.key -48 <10):
                pygame.draw.rect(screen, (250,250,250), (position[0]*50 + buffer, position[1]*50+ buffer,50 -2*buffer , 50 - 2*buffer))

                value = myfont.render(str(event.key -48),True, (0,0,0))
                screen.blit(value , (position[0]*50+15, position[1]*50))
                grid[i-1][j-1]= event.key - 48
                pygame.display.update()
                return
            return


def main():
    pygame.init()
    myfont = pygame.font.SysFont('Comic Sans MS',35)
    pygame.display.set_caption('Sudoku Solver')
    
 
    
    screen.fill((250,250,250))
    
    for i in range(0,10):
        if i%3==0:
            pygame.draw.line(screen,(0,0,0),(50+50*i,50),(50+50*i,500),4)
            pygame.draw.line(screen,(0,0,0),(50,50+50*i),(500,50+50*i),4)
        pygame.draw.line(screen,(0,0,0),(50+50*i,50),(50+50*i,500),2)
        pygame.draw.line(screen,(0,0,0),(50,50+50*i),(500,50+50*i),2)
    pygame.display.update()

    for i in range(0,len(grid[0])):
        for j in range (0,len(grid[0])):
            if (0<grid[i][j]<10):
                value = myfont.render(str(grid[i][j]),True,(0,0,0))
                screen.blit(value,((j+1)*50+8,(i+1)*50))
    text = myfont.render('Sudoku Solver \n using \n Backtracking', True, (0,255,0))
    screen.blit(text, (300,600))
    pygame.display.update()

    sudoku_solver(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                insert(screen,(pos[0]//50,pos[1]//50))
            if event.type == pygame.QUIT:
                pygame.quit()
                return
main()