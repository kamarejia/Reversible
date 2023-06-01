import pygame
import random
import math
import time
import sys

"""
[
[(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7)],
[(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7)],
[(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7)],
[(3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7)],
[(4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7)],
[(5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7)],
[(6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7)],
[(7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7)],
]
"""

WIDTH=800
HEIGHT=800
FPS=60

#color
BLACK=(0,0,0)
WHITE=(220,220,220)
RED=(220,20,60)
GRAY=(105,105,105)
class Piece:
    def __init__(self,color):
        self.color=color

class Board:
    def __init__(self):
        self.board_status=[[None for i in range(8)] for j in range(8)]
        self.board_status[3][4]=Piece(RED)
        self.board_status[4][3]=Piece(RED)
        self.board_status[3][3]=Piece(WHITE)
        self.board_status[4][4]=Piece(WHITE)      

class GameSystem:
    def __init__(self):
        self.turn=0
        self.pass_count=0
        self.r=0
        self.w=0
        self.winlose=None
        
    def draw_gameboard(self):
        grid=WIDTH//8
        for i in range(0,9):
            for j in range(0,9):
                length=15
                angle=[0,90,180,270]
                center_x=j*grid
                center_y=i*grid
                for angle in angle:
                    end_x=center_x + length * math.cos(math.radians(angle))
                    end_y=center_y + length*math.sin(math.radians(angle))
                    pygame.draw.line(window,GRAY,(center_x,center_y),(end_x,end_y),3)
        pos_x=[1,3]
        pos_y=[1,3]
        for x in pos_x:
            for y in pos_y:
                center_x=x/4*WIDTH
                center_y=y/4*HEIGHT
                pygame.draw.circle(window,GRAY,(center_x,center_y),7,0)

    def draw_pieces(self):
        for i in range(0,8):
            for j in range(0,8):
                if board.board_status[i][j] != None:
                    color=board.board_status[i][j].color
                    pos_x,pos_y=(i,j)
                    center_x=(2*(pos_y+1)-1)/16*WIDTH
                    center_y=(2*(pos_x+1)-1)/16*HEIGHT
                    pygame.draw.circle(window,color,(center_x,center_y),30,0)

    def draw_placeable_squares(self,color):
        placeable_list=self.search_placeable_squares(color)
        for pos in placeable_list:            
            pos_x,pos_y=pos
            center_x=(2*(pos_y+1)-1)/16*WIDTH
            center_y=(2*(pos_x+1)-1)/16*HEIGHT
            pygame.draw.circle(window,GRAY,(center_x,center_y),25,2)

    def reverse(self,pos,color):
        center_x,center_y=pos
        directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        othercolor=other_color(color)
        for dx, dy in directions:
            i,j=center_x+dx,center_y+dy
            temp=[]
            while 0<=i<=7 and 0<=j<=7 and board.board_status[i][j] is not None and board.board_status[i][j].color==othercolor:
                temp.append((i,j))
                i,j=i+dx,j+dy
            if 0<=i<=7 and 0<=j<=7 and board.board_status[i][j] is not None and board.board_status[i][j].color==color:
                for x,y in temp:
                    board.board_status[x][y]=Piece(color)
        
    def search_placeable_squares(self,color):
        placeable_list=[]
        othercolor=other_color(color)
        directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        for i in range(0,8):
            for j in range(0,8):
                if board.board_status[i][j]==None:
                    for dx,dy in directions:
                        temp_i,temp_j=i+dx,j+dy
                        while 0<=temp_i<=7 and 0<=temp_j<=7 and board.board_status[temp_i][temp_j] is not None and board.board_status[temp_i][temp_j].color==othercolor:
                            if 0<=temp_i+dx<=7 and 0<=temp_j+dy<=7 and board.board_status[temp_i+dx][temp_j+dy] is not None and board.board_status[temp_i+dx][temp_j+dy].color==color:
                                placeable_list.append((i,j))
                                break
                            temp_i,temp_j=temp_i+dx,temp_j+dy
        return placeable_list
    
    def count_pieces(self):
        count_red=0
        count_white=0
        count_none=0
        for i in range(8):
            for j in range(8):
                if board.board_status[i][j]==None:
                    count_none +=1
                elif board.board_status[i][j].color==RED:
                    count_red +=1
                elif board.board_status[i][j].color==WHITE:
                    count_white +=1
        return count_none,count_red,count_white

    def judgment(self):
        n,self.r,self.w=self.count_pieces()
        
        if n==0 or self.pass_count==2:
            if self.r>self.w:
                self.winlose="r"
            elif self.r<self.w:
                self.winlose="w"
            elif self.r==self.w:
                self.winlose="d"

            board.board_status = [[None for i in range(8)] for j in range(8)]
            for i in range(8):
                for j in range(8):
                    if self.r > 0:
                        board.board_status[i][j] = Piece(RED)
                        self.r -= 1
                    elif self.w > 0:
                        board.board_status[i][j] = Piece(WHITE)
                        self.w -= 1
                    else:
                        board.board_status[i][j]=None
            
            global flag
            flag="END"

    def draw_results(self):
        if self.winlose=="r":
            result="You Win!"
        elif self.winlose=="w":
            result="You Lose"
        elif self.winlose=="d":
            result="Draw"
        
        font = pygame.font.Font(None, 72)  
        text = font.render(result, True, (255, 255, 255))  
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  
        rounded_rect_surface = pygame.Surface((400, 200), pygame.SRCALPHA)
        pygame.draw.rect(rounded_rect_surface, (0, 0, 255, 128), (0, 0, 400, 200), border_radius=20)
        rounded_rect_rect = rounded_rect_surface.get_rect(center=(WIDTH // 2, HEIGHT//2))
        window.blit(rounded_rect_surface, rounded_rect_rect)
        window.blit(text, text_rect)
             

class Player:
    def __init__(self):
        self.myturn=0
    def play(self,events):
        if self.myturn==game.turn:
            placeable_list=game.search_placeable_squares(RED)
            if len(placeable_list) > 0:
                for event in events:
                    if event.type==pygame.MOUSEBUTTONDOWN:
                        grid_width = WIDTH // 8
                        grid_height = HEIGHT // 8
                        mouse_x,mouse_y = pygame.mouse.get_pos()

                        for i in range(8):
                            for j in range(8):
                                if mouse_x>i*grid_width and mouse_x < (i + 1) * grid_width and mouse_y>j*grid_height and mouse_y < (j + 1) * grid_height:
                                    if (j,i) in placeable_list:
                                        board.board_status[j][i]=Piece(RED)
                                        game.reverse((j,i),RED)
                                        game.turn=0.5
                                        game.pass_count=0
                                        global timer
                                        timer=time.time()
            else:
                game.pass_count +=1                        

class NPC:
    def __init__(self):
        self.myturn=1
    def play(self):
        if self.myturn==game.turn:
            
            placeable_list=game.search_placeable_squares(WHITE)
            if len(placeable_list) > 0:  
                move=random.choice(placeable_list)
                x,y=move
                board.board_status[x][y]=Piece(WHITE)
                game.reverse((x,y),WHITE)
                game.turn=0
                game.pass_count=0
            else:  
                game.pass_count +=1
                

def other_color(color):
    if color==RED:
        return WHITE
    elif color==WHITE:
        return RED
board=Board()
game=GameSystem()
player=Player()
npc=NPC()
timer=time.time()
pygame.init()
pygame.display.set_caption("Reversible")
window=pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
flag="GAME"
def main():
    while True:
        events=pygame.event.get()
        for event in events:
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        if flag=="GAME":
            window.fill(BLACK)
            game.draw_gameboard()
            game.draw_pieces()
            game.draw_placeable_squares(RED)
            player.play(events)
            npc.play()
            #遅延処理
            if game.turn==0.5:
                global timer
                if time.time()-timer>0.5:
                    game.turn=1
            game.judgment()
            pygame.display.flip()
            clock.tick(FPS)
        elif flag=="END":
            window.fill(BLACK)
            game.draw_gameboard()
            game.draw_pieces()
            game.draw_results()
            pygame.display.flip()
            
if __name__ == "__main__":
    main()