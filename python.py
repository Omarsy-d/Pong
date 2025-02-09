import pygame, asyncio
from pygame.locals import *

pygame.init()

#Clock
fpsclock=pygame.time.Clock()
fps=60

#Color
bg=(0,0,0)       #bg=(50,25,50)
green=(0,255,0)  #white=(255,255,255)

#Font
font=pygame.font.SysFont('constantia',30)

#Variables
live_ball=False
You_text_x_cor=500 
margin=50
AI_score=0
player_score=0
winner=0
speed_increase=0

#Screen
screen_width=600
screen_height=500

screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

#Score board
def draw_board():
    screen.fill(bg)

def draw_text(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    screen.blit(img,(x,y))

class paddle():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.rect=Rect(self.x,self.y,20,100)
        self.speed=5

    def move(self):
        key=pygame.key.get_pressed()
        if (key[pygame.K_w] or key[pygame.K_UP]) and self.rect.top>margin:
            self.rect.move_ip(0,-1*self.speed)
        if (key[pygame.K_s] or key[pygame.K_DOWN]) and self.rect.bottom<screen_height:
            self.rect.move_ip(0,self.speed)

    def draw(self):
        pygame.draw.rect(screen,green,self.rect)

    def ai(self):
        #Computer moves the paddle by itself
        if self.rect.centery<pong.rect.top and self.rect.bottom<screen_height:
            self.rect.move_ip(0,self.speed)
        if self.rect.centery>pong.rect.bottom and self.rect.top>margin:
            self.rect.move_ip(0,-1*self.speed)

class ball():
    def __init__(self,x,y):
        self.reset(x,y)

    def move(self):
        #Collision with top
        if self.rect.top<margin:
            self.speed_y*=-1

        #Collision with bottom
        if self.rect.bottom>screen_height:
            self.speed_y*=-1

        #Collision with paddles
        if self.rect.colliderect(player_paddle) or self.rect.colliderect(AI_paddle):
            self.speed_x*=-1

        #Check who won
        if self.rect.left<0:
            self.winner=1
        if self.rect.right>screen_width:
            self.winner=-1

        self.rect.x+=self.speed_x
        self.rect.y+=self.speed_y

        return self.winner

    def draw(self):
        pygame.draw.circle(screen,green,(self.rect.x+self.ball_rad,self.rect.y+self.ball_rad),self.ball_rad)

    def reset(self,x,y):
        self.x=x
        self.y=y
        self.ball_rad=8
        self.rect=Rect(self.x,self.y,self.ball_rad*2,self.ball_rad*2)
        self.speed_x=-4
        self.speed_y=4
        self.winner=0

#Paddles
player_paddle=paddle(screen_width-40,screen_height//2)
AI_paddle=paddle(20,screen_height//2)

#Pong ball
pong=ball(screen_width-60,screen_height//2+50)

async def main():
    global live_ball, winner, player_score, AI_score, speed_increase
    run=True
    while run:
        fpsclock.tick(fps)
        draw_board()
        draw_text('AI: ' +str(AI_score),font,green,20,15)
        draw_text('You: ' +str(player_score),font,green,screen_width-100,15)
        draw_text('BALL SPEED: ' +str(abs(pong.speed_x)),font,green,screen_width//2-100,15)
        pygame.draw.line(screen,green,(0,margin),(screen_width,margin),2)

        #Draw paddles and ball
        player_paddle.draw()
        AI_paddle.draw()

        if live_ball:
            winner=pong.move()
            if winner==0:
                player_paddle.move()
                AI_paddle.ai()
                pong.draw()
                speed_increase+=1
            else:
                live_ball=False
                if winner==1:
                    player_score+=1
                elif winner==-1:
                    AI_score+=1

        if speed_increase>500:  
            speed_increase=0
            if pong.speed_x < 0:
                pong.speed_x -= 1
            if pong.speed_x > 0:
                pong.speed_x += 1
            if pong.speed_y < 0:
                pong.speed_y -= 1
            if pong.speed_y > 0:
                pong.speed_y += 1

        #Player instructions
        if not live_ball:
            if winner==0:
                draw_text('Use "up/down" key or "W","S',font,green,100,screen_height//2-100)
                draw_text('to go up and down dont allow',font,green,100,200)
                draw_text('the ball slip behind your paddle.',font,green,100,250)
                draw_text('CLICK ANYWHERE TO START',font,green,100,300)
            elif winner==1:
                draw_text('YOU SCORED!',font,green,220,screen_height//2-100)
                draw_text('CLICK ANYWHERE TO START',font,green,100,screen_height//2-50)
            elif winner==-1:
                draw_text('AI SCORED!',font,green,220,screen_height//2-100)
                draw_text('CLICK ANYWHERE TO START',font,green,100,screen_height//2-50)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.MOUSEBUTTONDOWN and not live_ball:
                live_ball=True
                pong.reset(screen_width-60,screen_height//2+50)

        pygame.display.update()
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())