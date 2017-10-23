import pygame
import random as rd
import numpy as np
pygame.init()

white = (255,255,255)
black = (0,0,0)
bg_color = black
FLAG = False
FPS = 30
changes = 5
no_of_start_points = 5
gameDisplay = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
gameDisplay.fill(bg_color)
pixAr = pygame.PixelArray(gameDisplay) # get pixels array by handle

#turns arr of length 3 into a tuple
    
def to_tuple(arr):
    return (arr[0],arr[1],arr[2])
    
def find_coords_of_nearest_empty_px(x1,y1):
    nearest_x_coords = [x1-1,x1,x1+1]
    nearest_y_coords = [y1-1,y1,y1+1]
    empty_coords = []
    for x_element in nearest_x_coords:
        for y_element in nearest_y_coords:
            if x_element > 0 and x_element <800 and y_element>0 and y_element<600:
                if gameDisplay.get_at((x_element,y_element))[0:3] == bg_color:
                    empty_coords.append([x_element,y_element])
    global FLAG
    if not FLAG:
        print(empty_coords)
        FLAG = True
    return empty_coords
    
def Markov_Chain(x_n,y_n,x,y):
    changed = rd.randint(0,1000)
    changed_by = [np.random.normal(0, changes),np.random.normal(0, changes),np.random.normal(0, changes)]
    if changed > 998:
        color_tup = gameDisplay.get_at((x,y))
        r_val = color_tup[0]+changed_by[0]
        if r_val < 0:
            r_val = -r_val
        while r_val > 255:
            r_val = 255 - (r_val - 255)
        g_val = color_tup[1]+changed_by[1]
        if g_val < 0:
            g_val = -g_val
        while g_val > 255:
            g_val = 255 - (g_val - 255)
        b_val = color_tup[2]+changed_by[2]
        if b_val < 0:
            b_val = -b_val
        while b_val > 255:
            b_val = 255 -(b_val - 255)
        new_colour = (r_val,g_val,b_val,255)
        gameDisplay.set_at((x_n,y_n),new_colour)
    
def Main_Loop():
    for i in range(no_of_start_points):
        x = rd.randint(0,800)
        y = rd.randint(0,600)
        color_RGB = [255,255,255]
        for i in range(0,3):
            color_RGB[i] = rd.randint(0,255)
        pixAr[x][y] = to_tuple(color_RGB)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        pygame.display.update()
        clock.tick(FPS)
        pixels_to_change = []
        for i in range(0,800):
            for j in range(0,600):
                if gameDisplay.get_at((i,j)) != (0,0,0,255):
                    local_empties = find_coords_of_nearest_empty_px(i,j)
                    for element in local_empties:
                        pixels_to_change.append([element[0],element[1],i,j])
        for pix in pixels_to_change:
            if gameDisplay.get_at((pix[0],pix[1])) == (0,0,0,255):
                Markov_Chain(pix[0],pix[1],pix[2],pix[3])


Main_Loop()