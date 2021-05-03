# Dating App Popularity Monte Carlo Simulation
# March 31st, 2021

import os
import sys
import re
import math
import random
import pygame
from pygame.locals import *
import warnings
import PIL
from PIL import Image
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
warnings.filterwarnings('ignore')

# Global Variables
WINDOWWIDTH = 1000
WINDOWHEIGHT = 1200
XMARGIN_BOARD = 50
YMARGIN_BOARD = 200
XMARGIN_14 = WINDOWWIDTH / 4
XMARGIN_12 = WINDOWWIDTH / 2
XMARGIN_34 = WINDOWWIDTH / 4 * 3
XMARGIN_38 = WINDOWWIDTH / 8 * 3
XMARGIN_58 = WINDOWWIDTH / 8 * 5
XMARGIN_78 = WINDOWWIDTH / 8 * 7
YMARGIN_14 = WINDOWHEIGHT / 4
YMARGIN_12 = WINDOWHEIGHT / 2
YMARGIN_34 = WINDOWHEIGHT / 4 * 3
YMARGIN_38 = WINDOWHEIGHT / 8 * 3
YMARGIN_58 = WINDOWHEIGHT / 8 * 5
YMARGIN_78 = WINDOWHEIGHT / 8 * 7
BOXWIDTH = 4
BOXHEIGHT = 5
BOXSIZE = 80
GAPXSIZE = 10
GAPYSIZE = 30
IPHONEIMGLEFT = 150
IPHONEIMGTOP = 450
FPS = 60
FONT = 'Fonts/ShortBaby-Mg2w.ttf'
STARTBGIMG = 'Images/background.png'
COUNTIMG = 'Images/count.png'
TOTALIMG = 'Images/total.png'
BOYIMG = 'Images/boy.png'
GIRLIMG = 'Images/girl.png'
IPHONEIMG = 'Images/iphone.png'
ICONPATH = 'Icons/'

# Color
BLACK  = (0  , 0  , 0  )
WHITE  = (255, 255, 255)
RED    = (255, 0  , 0  )
GREEN  = (0  , 255, 0  )
BLUE   = (0  , 0  , 255)
YELLOW = (255, 255, 0  )
ORANGE = (255, 128, 0  )
PURPLE = (255, 0  , 255)
CYAN   = (0  , 255, 255)


def main():
    global FPSCLOCK, DISPLAYSURF, BOARD, COUNT, CUSTOMER_TOTAL, CUSTOMER_NOW
    BOARD = []
    COUNT = 0
    IDX = 0
    CUSTOMER_TOTAL = 1000
    CUSTOMER_NOW = 0
    print('Generating Simulation..........')
    # Gender
    gender_df = DataFrame({'Gender' : [1, 0], 'Probability' : [0.4852, 0.5148]})

    # Population Density
    random.seed(99)
    population_img = Image.open(r'./Distribution/City of Chicago population density circa 2010.jpg')
    population_image_sequence = population_img.getdata()
    population_image_array = np.array(population_image_sequence)
    population_image_series = Series(population_image_array.tolist()).map(lambda x : ', '.join(list(map(str, x))))
    population_image_series_vc = population_image_series.value_counts()
    population_image_series_vc = population_image_series_vc.iloc[1:]
    population_image_series_vc = population_image_series_vc[population_image_series_vc > 100]
    population_p  = population_image_series_vc / population_image_series_vc.sum()
    population_p = population_p.values.tolist()
    x = 30000
    num_bins = len(population_p)
    lower_ls = list(map(min, np.array_split(range(x), num_bins)))
    upper_ls = list(map(max, np.array_split(range(x), num_bins)))
    range_ls = list(zip(lower_ls, upper_ls))
    random.shuffle(range_ls)
    population_df = DataFrame({'Population Density Range' : range_ls, 'Probability' : population_p})

    # Income
    random.seed(20)
    income_img = Image.open(r'./Distribution/Chicago-Median-Household-Income.png')
    income_image_sequence = income_img.getdata()
    income_image_array = np.array(income_image_sequence)
    income_image_series = Series(income_image_array.tolist()).map(lambda x : ', '.join(list(map(str, x))))
    income_image_series_vc = income_image_series.value_counts()
    income_image_series_vc = income_image_series_vc.iloc[1:]
    income_image_series_vc = income_image_series_vc[income_image_series_vc > 100]
    income_p  = income_image_series_vc / income_image_series_vc.sum()
    income_p = income_p.values.tolist()
    x = 300000
    num_bins = len(income_p)
    lower_ls = list(map(min, np.array_split(range(x), num_bins)))
    upper_ls = list(map(max, np.array_split(range(x), num_bins)))
    range_ls = list(zip(lower_ls, upper_ls))
    random.shuffle(range_ls)
    income_df = DataFrame({'Income Range' : range_ls, 'Probability' : income_p})

    # Age
    age = [(0, 4), (5, 9), (10, 14), (15, 19), (20, 24), (25, 29), (30, 34), (35, 39), (40, 44), (45, 49), (50, 54), (55, 59), (60, 64), (65, 69), (70, 74), (75, 79), (80, 84), (85, 100)]
    pct = [3.8, 3.5, 3.3, 3.5, 3.6, 4.8, 4.0, 3.5, 3.3, 3.4, 3.3, 2.8, 2.3, 1.6, 1.2, 0.9, 0.7, 0.5]
    pct = list(map(lambda x : x * 0.02, pct))
    age_df = DataFrame({'Age Range' : age, 'Probability' : pct})

    # preference
    preference_df = DataFrame({'Preference' : ['Dating', 'Shopping', 'News', 'Social'], 'Probability' : [0.4, 0.3, 0.2, 0.1]})

    CHOICE = generateCustomerGroup(CUSTOMER_TOTAL, gender_df, age_df, income_df, population_df, preference_df)
    print('Finish Generating Simulation.')
    # Basic Settings
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF =  pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Dating App Popularity MC Simulation')

    generateBoard()

    # Local Variables Settings
    game_start = False
    mouse_x = 0
    mouse_y = 0
    start_highlight = False
    exit_highlight = False

    while True:
        if game_start == False:
            startRectObj, exitRectObj = drawStartPage(start_highlight, exit_highlight)
            for event in pygame.event.get():
                if (event.type == QUIT) or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                    if startRectObj.collidepoint(mouse_x, mouse_y):
                        start_highlight = True
                        drawStartPage(start_highlight, exit_highlight)
                    elif exitRectObj.collidepoint(mouse_x, mouse_y):
                        exit_highlight = True
                        drawStartPage(start_highlight, exit_highlight)
                    else:
                        start_highlight = False
                        exit_highlight = False
                elif event.type == MOUSEBUTTONUP:
                    mouse_x, mouse_y = event.pos
                    if startRectObj.collidepoint(mouse_x, mouse_y):
                        game_start = True
                    elif exitRectObj.collidepoint(mouse_x, mouse_y):
                        pygame.quit()
                        sys.exit()
        else:
            drawStartPage(None, None)
            drawBoard()
            if CUSTOMER_NOW < CUSTOMER_TOTAL:
                CUSTOMER_NOW += 1
                if CHOICE[IDX] == 1:
                    drawHightlight()
                    COUNT += 1
                IDX += 1
            for event in pygame.event.get():
                if (event.type == QUIT) or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def generateBoard():
    xorder = [1, 2, 3, 4]
    yorder = ['dating', 'shop', 'fun', 'social', 'bottom']
    for x in xorder:
        BOARD.append(list(map(lambda y : ICONPATH + y + str(x) + '.png', yorder)))

def drawStartPage(start_highlight = False, exit_highlight = False):
    DISPLAYSURF.fill(BLACK)
    if (start_highlight != None) & (exit_highlight != None):
        startimgSurfaceObj = pygame.image.load(STARTBGIMG)
        startimgRectObj = startimgSurfaceObj.get_rect()
        startimgRectObj.center = (XMARGIN_12, YMARGIN_12)
        DISPLAYSURF.blit(startimgSurfaceObj, startimgRectObj)
    # Title
    fontTitle = pygame.font.Font(FONT, 64)
    titleSurfaceObj = fontTitle.render('Tinder Popularity Simulation', True, YELLOW)
    titleRectObj = titleSurfaceObj.get_rect()
    titleRectObj.center = (XMARGIN_12, 50)
    DISPLAYSURF.blit(titleSurfaceObj, titleRectObj)
    # Author
    fontAuthor = pygame.font.Font(FONT, 32)
    authorSurfaceObj = fontAuthor.render('By Siyuan Zhao & Xiaolei Shao', True, YELLOW)
    authorRectObj = authorSurfaceObj.get_rect()
    authorRectObj.center = (XMARGIN_12, 150)
    DISPLAYSURF.blit(authorSurfaceObj, authorRectObj)
    # Option
    if start_highlight == True:
        startRectObj = drawOption('START', 64, YELLOW, (XMARGIN_78, YMARGIN_38))
        exitRectObj = drawOption('EXIT', 48, YELLOW, (XMARGIN_78, YMARGIN_58))
    elif exit_highlight == True:
        startRectObj = drawOption('START', 48, YELLOW, (XMARGIN_78, YMARGIN_38))
        exitRectObj = drawOption('EXIT', 64, YELLOW, (XMARGIN_78, YMARGIN_58))
    elif (start_highlight != None) & (exit_highlight != None):
        startRectObj = drawOption('START', 48, YELLOW, (XMARGIN_78, YMARGIN_38))
        exitRectObj = drawOption('EXIT', 48, YELLOW, (XMARGIN_78, YMARGIN_58))
    else:
        startRectObj, exitRectObj = None, None
    return startRectObj, exitRectObj

def drawOption(text, size, color, center):
    # Option
    fontOption = pygame.font.Font(FONT, size)
    textSurfaceObj = fontOption.render(text, True, color)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = center
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    return textRectObj

def drawBoard():
    # Draw Iphone Image
    iphoneSurfaceObj = pygame.image.load(IPHONEIMG)
    iphonewidth, iphoneheight = int(WINDOWWIDTH - XMARGIN_BOARD), int(WINDOWHEIGHT - YMARGIN_BOARD)
    iphoneSurfaceObj = pygame.transform.scale(iphoneSurfaceObj, ((iphonewidth, iphoneheight)))
    iphoneRecObj = iphoneSurfaceObj.get_rect()
    iphoneRecObj.topleft = (XMARGIN_BOARD - 200, YMARGIN_BOARD)
    DISPLAYSURF.blit(iphoneSurfaceObj, iphoneRecObj)
    # Draw Countboard Image
    countSurfaceObj = pygame.image.load(COUNTIMG)
    countSurfaceObj = pygame.transform.scale(countSurfaceObj, (BOXSIZE * 2, BOXSIZE * 2))
    countRecObj = countSurfaceObj.get_rect()
    countRecObj.topleft = (XMARGIN_78 - 50, YMARGIN_14)
    DISPLAYSURF.blit(countSurfaceObj, countRecObj)
    # Draw Total Image
    totalSurfaceObj = pygame.image.load(TOTALIMG)
    totalSurfaceObj = pygame.transform.scale(totalSurfaceObj, (BOXSIZE * 2, BOXSIZE * 2))
    totalRecObj = totalSurfaceObj.get_rect()
    totalRecObj.topleft = (XMARGIN_78 - 50, YMARGIN_12)
    DISPLAYSURF.blit(totalSurfaceObj, totalRecObj)
    # Draw Font
    fontCount = pygame.font.Font(FONT, 32)
    fontSurfaceObj1 = fontCount.render(str(COUNT), True, YELLOW)
    fontRectObj1 = fontSurfaceObj1.get_rect()
    fontRectObj1.center = countRecObj.center[0] - 200, countRecObj.center[1]
    fontSurfaceObj2 = fontCount.render(str(CUSTOMER_NOW), True, YELLOW)
    fontRectObj2 = fontSurfaceObj2.get_rect()
    fontRectObj2.center = totalRecObj.center[0] - 200, totalRecObj.center[1]
    DISPLAYSURF.blit(fontSurfaceObj1, fontRectObj1)
    DISPLAYSURF.blit(fontSurfaceObj2, fontRectObj2)

    # Draw Icons
    for boxx in range(BOXWIDTH):
        for boxy in range(BOXHEIGHT):
            iconSurfaceObj = pygame.image.load(BOARD[boxx][boxy])
            if 'dating1' in BOARD[boxx][boxy]:
                iconSurfaceObj = pygame.transform.scale(iconSurfaceObj, (BOXSIZE * 2, BOXSIZE * 2))
                left, top = box2PixelCoordinate(boxx, boxy)
                iconRecObj = iconSurfaceObj.get_rect()
                iconRecObj.topleft = (left - 40, top - 40)
                # pygame.draw.rect(DISPLAYSURF, RED, (iconRecObj.left + 38, iconRecObj.top + 35, BOXSIZE + 12, BOXSIZE + 12), 5)
            elif 'bottom' in BOARD[boxx][boxy]:
                iconSurfaceObj = pygame.transform.scale(iconSurfaceObj, (BOXSIZE, BOXSIZE))
                left, top = box2PixelCoordinate(boxx, boxy)
                iconRecObj = iconSurfaceObj.get_rect()
                iconRecObj.topleft = (left, top + 50)
            else:
                iconSurfaceObj = pygame.transform.scale(iconSurfaceObj, (BOXSIZE, BOXSIZE))
                left, top = box2PixelCoordinate(boxx, boxy)
                iconRecObj = iconSurfaceObj.get_rect()
                iconRecObj.topleft = (left, top)
            DISPLAYSURF.blit(iconSurfaceObj, iconRecObj)

def box2PixelCoordinate(boxx, boxy):
    left = IPHONEIMGLEFT + (BOXSIZE + GAPXSIZE) * boxx
    top = IPHONEIMGTOP + (BOXSIZE + GAPYSIZE) * boxy
    return (left, top)

def generateCustomerGroup(customer_number, gender_df, age_df, income_df, population_df, preference_df):
    gender_arr = np.random.choice(gender_df['Gender'], p = gender_df['Probability'].values.tolist(), size = customer_number)
    age_ls = np.random.choice(age_df['Age Range'], p = age_df['Probability'].values.tolist(), size = customer_number).tolist()
    age_arr = np.array(list(map(lambda x : np.random.uniform(low = x[0], high = [1]).tolist()[0], age_ls)))
    income_ls = np.random.choice(income_df['Income Range'], p = income_df['Probability'].values.tolist(), size = customer_number).tolist()
    income_arr = np.array(list(map(lambda x : np.random.uniform(low = x[0], high = [1]).tolist()[0], income_ls)))
    population_ls = np.random.choice(population_df['Population Density Range'], p = population_df['Probability'].values.tolist(), size = customer_number).tolist()
    population_arr = np.array(list(map(lambda x : np.random.uniform(low = x[0], high = [1]).tolist()[0], population_ls)))
    preference_arr = np.random.normal(loc = 1, scale = 0.5, size = customer_number)
    t = (0.05 * np.cbrt(population_arr) - 2.4 * np.log(income_arr) + 0.03 * gender_arr + 0.013 * np.exp(preference_arr)) / (0.08 * np.exp(np.sqrt(age_arr)))
    prob = np.round(1 / (1 + np.exp(-t)), 3)
    choice = list(map(lambda x : np.random.choice([1, 0], p = [x, 1 - x]), prob.tolist()))
    # print(prob)
    # print(choice)
    return choice

def drawHightlight():
    left, top = box2PixelCoordinate(0, 0)
    pygame.draw.rect(DISPLAYSURF, RED, (left - 2, top -5, BOXSIZE + 12, BOXSIZE + 12), 5)

if __name__ == '__main__':

    main()
