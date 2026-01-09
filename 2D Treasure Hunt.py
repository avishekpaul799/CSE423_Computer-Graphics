# Author: Avishek Paul
# Course / Project: CSE423-Computer Graphics
# Description: 2D OpenGL mining game using midpoint algorithms



from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random

W_Width, W_Height = 800,800
brick = []
brick_dict = {}
tool = {'drill': [[-400,245],[-390,245],[-360,245],[-350,245],[-390,250],[-390,240],[-360,240],[-360,250],[-385,240],[-385,222],[-365,222],
         [-365,240],[-385,222],[-380,218],[-370,218],[-365,222],[-380,218],[-380,210],[-370,210],[-370,218],[-382,210],[-375,200],
         [-368,210],[-382,210]],
        'hammer': ''}

pause = 0
tool_flag = 0
tool_pos = -16
p_flag = 1
direction_flag = '0000'
bomb = []
score = [0,2]

def midpoint_line(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    if dx >= 0 and dy >= 0:
        if abs(dx) > abs(dy):
            zone = 0
        else:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            zone = 1

    elif dx <= 0 and dy >= 0:
        if abs(dx) < abs(dy):
            x0, y0 = y0, -x0
            x1, y1 = y1, -x1
            zone = 2
        else:
            x0, y0 = -x0, y0
            x1, y1 = -x1, y1
            zone = 3

    elif dx <= 0 and dy <= 0:
        if abs(dx) > abs(dy):
            x0, y0 = -x0, -y0
            x1, y1 = -x1, -y1
            zone = 4
        else:
            x0, y0 = -y0, -x0
            x1, y1 = -y1, -x1
            zone = 5

    elif dx >= 0 and dy <= 0:
        if abs(dx) < abs(dy):
            x0, y0 = -y0, x0
            x1, y1 = -y1, x1
            zone = 6
        else:
            x0, y0 = x0, -y0
            x1, y1 = x1, -y1
            zone = 7

    draw_line(x0, y0, x1, y1, zone)


def draw_line(x0, y0, x1, y1, zone):
    dx = x1 - x0
    dy = y1 - y0
    d = 2 * dy - dx
    E = 2 * dy
    NE = 2 * (dy - dx)
    x = x0
    y = y0
    l_points = [[x, y]]
    while x < x1:
        if d <= 0:
            d += E
            x += 1
        else:
            d += NE
            x += 1
            y += 1
        l_points.append([x, y])

    if zone == 1:
        for i in l_points:
            i[0], i[1] = i[1], i[0]
    elif zone == 2:
        for i in l_points:
            i[0], i[1] = -i[1], i[0]
    elif zone == 3:
        for i in l_points:
            i[0], i[1] = -i[0], i[1]
    elif zone == 4:
        for i in l_points:
            i[0], i[1] = -i[0], -i[1]
    elif zone == 5:
        for i in l_points:
            i[0], i[1] = -i[1], -i[0]
    elif zone == 6:
        for i in l_points:
            i[0], i[1] = i[1], -i[0]
    elif zone == 7:
        for i in l_points:
            i[0], i[1] = i[0], -i[1]

    for i in l_points:
        glBegin(GL_POINTS)
        glVertex2f(i[0], i[1])
        glEnd()

def midpoint_circle(c, r):
    global checker
    glColor3f(1.0, 0.0, 0.0)
    glPointSize(3)

    d = 1 - r
    x = 0
    y = r
    points = [[x, y]]
    while x < y:
        if d >= 0:
            d += (2 * x - 2 * y + 5)
            x += 1
            y -= 1
        else:
            d += (2 * x + 3)
            x += 1
        points.append([x, y])

    temp = []
    for i in points:
        temp.extend([[i[1], i[0]], [-i[0], i[1]], [-i[1], i[0]], [-i[1], -i[0]], [-i[0], -i[1]], [i[0], -i[1]], [i[1], -i[0]]])
    points += temp

    for i in points:
        i[0] += c[0]
        i[1] += c[1]

    for i in points:
        glBegin(GL_POINTS)
        glVertex2f(i[0], i[1])
        glEnd()

def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y
    return a,b


def score_display(sc):
    glPointSize(30)
    glColor3f(1.0, 0.97, 0.0039)
    glBegin(GL_POINTS)
    glVertex2f(-175, 375)
    glEnd()
    glPointSize(15)
    glColor3f(0.8, 0.8, 0.8)
    glBegin(GL_POINTS)
    glVertex2f(-175, 375)
    glEnd()

    glPointSize(3)
    glColor3f(1.0, 1.0, 1.0)
    midpoint_line(-150,375,-140,375)
    if len(sc) == 1:
        sc = '0' + sc
    for i in range(len(sc)):
        if i == 0:
            s1, s2, p1, p2, p3 = -110, -130, 390, 360, 375
        else:
            s1, s2, p1, p2, p3 = -80, -100, 390, 360, 375

        if sc[i] == '0':
            midpoint_line(s2, p1, s1, p1)
            midpoint_line(s2, p1, s2, p2)
            midpoint_line(s2, p2, s1, p2)
            midpoint_line(s1, p1, s1, p2)

        elif sc[i] == '1':
            midpoint_line(s1, p1, s1, p2)

        elif sc[i] == '2':
            midpoint_line(s2, p1, s1, p1)
            midpoint_line(s1, p1, s1, p3)
            midpoint_line(s1, p3, s2, p3)
            midpoint_line(s2, p2, s1, p2)
            midpoint_line(s2, p3, s2, p2)

        elif sc[i] == '3':
            midpoint_line(s2, p1, s1, p1)
            midpoint_line(s1, p1, s1, p2)
            midpoint_line(s1, p3, s2, p3)
            midpoint_line(s2, p2, s1, p2)

        elif sc[i] == '4':
            midpoint_line(s1, p1, s1, p2)
            midpoint_line(s2, p1, s2, p3)
            midpoint_line(s2, p3, s1, p3)

        elif sc[i] == '5':
            midpoint_line(s2, p1, s1, p1)
            midpoint_line(s2, p1, s2, p3)
            midpoint_line(s2, p2, s1, p2)
            midpoint_line(s1, p3, s1, p2)
            midpoint_line(s2, p3, s1, p3)

        elif sc[i] == '6':
            midpoint_line(s2, p1, s1, p1)
            midpoint_line(s2, p1, s2, p2)
            midpoint_line(s2, p2, s1, p2)
            midpoint_line(s1, p3, s1, p2)
            midpoint_line(s2, p3, s1, p3)

        elif sc[i] == '7':
            midpoint_line(s2, p1, s1, p1)
            midpoint_line(s1, p1, s2, p2)

def life_display(sc):
    glPointSize(30)
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_POINTS)
    glVertex2f(95, 375)
    glEnd()

    glPointSize(3)
    glColor3f(1.0, 1.0, 1.0)
    midpoint_line(120, 375, 130, 375)

    s1, s2, p1, p2, p3 = 160, 140, 390, 360, 375

    if sc == '0':
        midpoint_line(s2, p1, s1, p1)
        midpoint_line(s2, p1, s2, p2)
        midpoint_line(s2, p2, s1, p2)
        midpoint_line(s1, p1, s1, p2)

    elif sc == '1':
        midpoint_line(s1, p1, s1, p2)

    elif sc == '2':
        midpoint_line(s2, p1, s1, p1)
        midpoint_line(s1, p1, s1, p3)
        midpoint_line(s1, p3, s2, p3)
        midpoint_line(s2, p2, s1, p2)
        midpoint_line(s2, p3, s2, p2)

    elif sc == '3':
        midpoint_line(s2, p1, s1, p1)
        midpoint_line(s1, p1, s1, p2)
        midpoint_line(s1, p3, s2, p3)
        midpoint_line(s2, p2, s1, p2)

def button_display():

    #back button
    glPointSize(3)
    glColor3f(0.0, 0.0, 0.8)
    midpoint_line(-390,375,-360,375)
    midpoint_line(-360,375,-372,390)
    midpoint_line(-360,375,-372,360)

    #cross_button
    glColor3f(0.8, 0.0, 0.0)
    midpoint_line(390,390,360,360)
    midpoint_line(360,390,390,360)


def brick_create():
    r = 0
    for j in range(200, -400, -50):
        for i in range(-400, 400, 50):
            temp = [[i, j], [i, j - 50], [i + 50, j - 50], [i + 50, j]]
            key = (i,j)
            brick_dict[key] = r
            r += 1
            brick.append(temp)
    #print(brick)
    #print(brick_dict)
brick_create()

def bomb_prize_create():
    temp = []
    c = 0
    while c <= 5:
        x = random.randint(0,191)
        x = [x, brick[x][0][0], brick[x][0][1], 5, True]
        if x not in temp:
            temp.append(x)
            c += 1
    bomb.append(temp)

    c = 0
    temp = []
    while c < 5:
        x = random.randint(0,191)
        x = [x, brick[x][0][0], brick[x][0][1], 5, True]
        if x not in bomb[0] and x not in temp:
            temp.append(x)
            c += 1
    bomb.append(temp)

    c = 0
    temp = []
    while c < 5:
        x = random.randint(0, 191)
        x = [x, brick[x][0][0], brick[x][0][1], 5, True]
        if x not in bomb[0] and x not in bomb[1] and x not in temp:
            temp.append(x)
            c += 1
    bomb.append(temp)

    c = 0
    temp = []
    while c < 1:
        x = random.randint(0, 191)
        x = [x, brick[x][0][0], brick[x][0][1], 5, True]
        if x not in bomb[0] and x not in bomb[1] and x not in bomb[2] and x not in temp:
            temp.append(x)
            c += 1
    bomb.append(temp)
    #print(bomb)

bomb_prize_create()

def bomb_prize_display():
    global tool_pos, pause

    for i in range(6):
        if brick[bomb[0][i][0]] == None and score[1] != 0 and pause != 1:
            if bomb[0][i][3] <= 75:
                x = bomb[0][i][1]
                y = bomb[0][i][2]
                glColor3f(1.0, 0.0, 0.0)
                midpoint_circle([x+25,y-25], bomb[0][i][3])
                if pause !=  1:
                    bomb[0][i][3] += 6
            elif bomb[0][i][4] == True:
                bomb[0][i][4] = False
                ind = bomb[0][i][0]
                if ind in [15, 31, 47, 63, 79, 95, 111, 127, 143, 159, 175, 191]:
                    t = [ind - 17, ind - 16, ind - 1, ind, ind + 15, ind + 16]
                elif ind % 16 == 0:
                    t = [ind - 16, ind - 15, ind, ind + 1, ind + 16, ind + 17]
                else:
                    t = [ind-17,ind-16,ind-15,ind-1, ind, ind+1,ind+15,ind+16,ind+17]

                for j in t:
                    if 0 <= j <= 191:
                        brick[j] = None
                if tool_pos in t:
                    score[1] -= 1
                    if score[1] != 0:
                        print(f'Life lost. {score[1]} life remaining.')
                    else:
                        print('Game Over')


    for i in range(5):
        if brick[bomb[1][i][0]] == None and score[1] != 0 and pause != 1:
            if bomb[1][i][3] <= 45:
                x = bomb[1][i][1]
                y = bomb[1][i][2]
                glColor3f(1.0, 0.97, 0.0039)
                glPointSize(bomb[1][i][3])
                glBegin(GL_POINTS)
                glVertex2f(x+25, y-25)
                glEnd()
                if pause != 1:
                    bomb[1][i][3] += 3
            elif bomb[1][i][4] == True:
                bomb[1][i][4] = False
                score[0] += 10
                print(f'Gold block found. Ten points added.\nCurrent score: {score[0]}')
                if score[0] == 75:
                    print('Congratulation! All tressures collected!')
                    score[1] = 0


    for i in range(5):
        x = bomb[2][i][1]
        y = bomb[2][i][2]
        if brick[bomb[2][i][0]] == None and score[1] != 0 and pause != 1:
            if bomb[2][i][3] <= 45:
                glColor3f(0.8, 0.8, 0.8)
                glPointSize(bomb[2][i][3])
                glBegin(GL_POINTS)
                glVertex2f(x+25, y-25)
                glEnd()
                if pause != 1:
                    bomb[2][i][3] += 3
            elif bomb[2][i][4] == True:
                bomb[2][i][4] = False
                score[0] += 5
                print(f'Silver block found. Five points added.\nCurrent score: {score[0]}')
                if score[0] == 75:
                    print('Congratulation! All tressures collected!')
                    score[1] = 0

    if brick[bomb[3][0][0]] == None and score[1] != 0 and pause != 1:
        x = bomb[3][0][1]
        y = bomb[3][0][2]
        if bomb[3][0][3] <= 45:
            glColor3f(0.0, 1.0, 0.0)
            glPointSize(bomb[3][0][3])
            glBegin(GL_POINTS)
            glVertex2f(x + 25, y - 25)
            glEnd()
            if pause != 1:
                bomb[3][0][3] += 3
        elif bomb[3][0][4] == True:
            bomb[3][0][4] = False
            score[1] += 1
            print(f'Extra life found. {score[1]} life remaining.')


def drill_display():
    drill = tool['drill']
    glPointSize(4)
    glColor3f(1.0, 1.0, 1.0)
    midpoint_line(drill[0][0], drill[0][1], drill[1][0], drill[1][1])
    midpoint_line(drill[2][0], drill[2][1], drill[3][0], drill[3][1])

    for i in range(4,len(drill),4):
        glPointSize(2)
        glColor3f(1.0, 1.0, 0.0)
        midpoint_line(drill[i][0], drill[i][1], drill[i+1][0], drill[i+1][1])
        midpoint_line(drill[i+1][0], drill[i+1][1], drill[i+2][0], drill[i+2][1])
        midpoint_line(drill[i+2][0], drill[i+2][1], drill[i+3][0], drill[i+3][1])
        midpoint_line(drill[i+3][0], drill[i+3][1], drill[i][0], drill[i][1])

def hammer_display():
    hammer = tool['hammer']
    glPointSize(2)
    glColor3f(1.0, 1.0, 1.0)
    midpoint_line(hammer[-1][0], hammer[-1][1], hammer[-2][0], hammer[-2][1])
    midpoint_line(hammer[-3][0], hammer[-3][1], hammer[-4][0], hammer[-4][1])

    for i in range(0, len(hammer)-4 , 4):
        glPointSize(2)
        glColor3f(0.0, 0.5, 1.0)
        midpoint_line(hammer[i][0], hammer[i][1], hammer[i + 1][0], hammer[i + 1][1])
        midpoint_line(hammer[i + 1][0], hammer[i + 1][1], hammer[i + 2][0], hammer[i + 2][1])
        midpoint_line(hammer[i + 2][0], hammer[i + 2][1], hammer[i + 3][0], hammer[i + 3][1])
        midpoint_line(hammer[i + 3][0], hammer[i + 3][1], hammer[i][0], hammer[i][1])

def brick_display():
    for i in brick:
        if i != None:
            glColor3f(0.6, 0.298, 0.0)
            glPointSize(4)
            midpoint_line(i[0][0],i[0][1],i[1][0],i[1][1])
            midpoint_line(i[1][0],i[1][1],i[2][0],i[2][1])
            midpoint_line(i[2][0],i[2][1],i[3][0],i[3][1])
            midpoint_line(i[3][0],i[3][1],i[0][0],i[0][1])

def brick_checker():
    global direction_flag

    l = None
    if direction_flag == '1000':
        add = -1
        l = (tool['hammer'][0][0]-50, tool['hammer'][0][1]+5)
    elif direction_flag == '0100':
        add = 1
        l = (tool['hammer'][0][0]+50, tool['hammer'][0][1]+5)
    elif direction_flag == '0010':
        add = -16
        l = (tool['drill'][0][0], tool['drill'][0][1]+55)
    elif direction_flag == '0001':
        add = 16
        l = (tool['drill'][0][0], tool['drill'][0][1]-45)


    if l != None:
        if l not in brick_dict:
            return [l, 'Move', add]
        elif brick_dict[l] == None or brick[brick_dict[l]] == None:
            return [l, 'Move', add]
        else:
            return [l, 'Stop']
    else:
        return [None, None, "Stop", None]

def mouseListener(button, state, x, y):
    global pause,tool_flag, tool_pos, p_flag, direction_flag, bomb, brick, brick_dict, tool, score

    if button == GLUT_LEFT_BUTTON:
        if(state == GLUT_DOWN):
            cx, cy = convert_coordinate(x, y)
            if cx >= -390 and cy >= 360 and cx <= -360 and cy <= 390:
                print(f'Restarting Game\n .............\n .............\n .............')
                brick = []
                brick_dict = {}
                tool = {'drill': [[-400, 245], [-390, 245], [-360, 245], [-350, 245], [-390, 250], [-390, 240], [-360, 240],
                              [-360, 250], [-385, 240], [-385, 222], [-365, 222],
                              [-365, 240], [-385, 222], [-380, 218], [-370, 218], [-365, 222], [-380, 218], [-380, 210],
                              [-370, 210], [-370, 218], [-382, 210], [-375, 200],
                              [-368, 210], [-382, 210]], 'hammer': ''}

                pause = 0
                tool_flag = 0
                tool_pos = -16
                p_flag = 1
                direction_flag = '0000'
                bomb = []
                score = [0, 2]
                brick_create()
                bomb_prize_create()

            elif cx >= 360 and cy >= 360 and cx <= 390 and cy <= 390:
                print('Goodbye! Score:',score[0])
                glutLeaveMainLoop()

            elif  score[1] != 0 and pause != 1:
                temp = brick_checker()
                if temp[1] == 'Stop':
                    brick[brick_dict[temp[0]]] = None
                    brick_dict[temp[0]] = None

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global tool_flag, direction_flag, tool_pos, pause

    if key == GLUT_KEY_RIGHT:
        direction_flag = '0100'
        if tool_flag == 0 and score[1] != 0 and pause != 1:
            tool_flag = 1
            t0 = tool['drill'][0][0]
            t1 = tool['drill'][0][1]
            tool['hammer'] = [[t0, t1], [t0, t1 - 20], [t0 + 50, t1 - 20], [t0 + 50, t1], [t0 + 20, t1 + 5], [t0 + 20, t1],
                            [t0 + 30, t1], [t0 + 30, t1 + 5], [t0 + 20, t1 - 20], [t0 + 20, t1 - 45], [t0 + 30, t1 - 45],
                            [t0 + 30, t1 - 20], [t0 + 10, t1], [t0 + 10, t1 - 20], [t0 + 40, t1 - 20], [t0 + 40, t1]]

        if score[1] != 0 and pause != 1:
            check = brick_checker()
            if tool['hammer'][0][0]+50 <= 350 and check[1] == 'Move' and pause != 1:
                tool_pos += check[2]
                for i in tool['hammer']:
                    i[0] += 50

    if key == GLUT_KEY_LEFT:
        direction_flag = '1000'
        if tool_flag == 0 and score[1] != 0 and pause != 1:
            tool_flag = 1
            t0 = tool['drill'][0][0]
            t1 = tool['drill'][0][1]
            tool['hammer'] = [[t0, t1], [t0, t1 - 20], [t0 + 50, t1 - 20], [t0 + 50, t1], [t0 + 20, t1 + 5], [t0 + 20, t1],
                              [t0 + 30, t1], [t0 + 30, t1 + 5], [t0 + 20, t1 - 20], [t0 + 20, t1 - 45], [t0 + 30, t1 - 45],
                              [t0 + 30, t1 - 20], [t0 + 10, t1], [t0 + 10, t1 - 20], [t0 + 40, t1 - 20], [t0 + 40, t1]]

        if score[1] != 0 and pause != 1:
            check = brick_checker()
            if tool['hammer'][0][0] - 50 >= -400 and check[1] == 'Move' and pause != 1:
                tool_pos += check[2]
                for i in tool['hammer']:
                    i[0] -= 50

    if key == GLUT_KEY_UP:
        direction_flag = '0010'
        if tool_flag == 1 and score[1] != 0 and pause != 1:
            tool_flag = 0
            t0 = tool['hammer'][0][0]
            t1 = tool['hammer'][0][1]
            tool['drill'] = [[t0,t1],[t0+10,t1],[t0+40,t1],[t0+50,t1],[t0+10,t1+5],[t0+10,t1-5],[t0+40,t1-5],[t0+40,t1+5],
                             [t0+15,t1-5],[t0+15,t1-23],[t0+35,t1-23],[t0+35,t1-5],[t0+15,t1-23],[t0+20,t1-27],[t0+30,t1-27],
                             [t0+35,t1-23],[t0+20,t1-27],[t0+20,t1-35],[t0+30,t1-35],[t0+30,t1-27],[t0+18,t1-35],[t0+25,t1-45],
                             [t0+32,t1-35],[t0+18,t1-35]]

        if score[1] != 0 and pause != 1:
            check = brick_checker()
            if tool['drill'][4][1]+50 <= 250 and check[1] == 'Move' and pause != 1:
                tool_pos += check[2]
                for i in tool['drill']:
                    i[1] += 50

    if key == GLUT_KEY_DOWN:
        direction_flag = '0001'
        if tool_flag == 1 and score[1] != 0 and pause != 1:
            tool_flag = 0
            t0 = tool['hammer'][0][0]
            t1 = tool['hammer'][0][1]
            tool['drill'] = [[t0, t1], [t0 + 10, t1], [t0 + 40, t1], [t0 + 50, t1], [t0 + 10, t1 + 5],
                             [t0 + 10, t1 - 5], [t0 + 40, t1 - 5], [t0 + 40, t1 + 5],
                             [t0 + 15, t1 - 5], [t0 + 15, t1 - 23], [t0 + 35, t1 - 23], [t0 + 35, t1 - 5],
                             [t0 + 15, t1 - 23], [t0 + 20, t1 - 27], [t0 + 30, t1 - 27],
                             [t0 + 35, t1 - 23], [t0 + 20, t1 - 27], [t0 + 20, t1 - 35], [t0 + 30, t1 - 35],
                             [t0 + 30, t1 - 27], [t0 + 18, t1 - 35], [t0 + 25, t1 - 45],
                             [t0 + 32, t1 - 35], [t0 + 18, t1 - 35]]

        if score[1] != 0 and pause != 1:
            check = brick_checker()
            if tool['drill'][4][1]-50 >= -350 and check[1] == 'Move' and pause != 1:
                tool_pos += check[2]
                for i in tool['drill']:
                    i[1] -= 50

    glutPostRedisplay()

def keyboardListener(key, x, y):
    global pause
    if key==b' ':
        if pause == 0:
            pause = 1
        else:
            pause = 0

    glutPostRedisplay()

def animate():
    glutPostRedisplay()
    pass

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0,0,401,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)

    score_display(str(score[0]))
    life_display(str(score[1]))
    button_display()
    if tool_flag == 0:
        drill_display()
    if tool_flag == 1:
        hammer_display()
    bomb_prize_display()
    brick_display()

    glutSwapBuffers()


def init():
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90,	1,	1,	1500)


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(50, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"OpenGL Coding Practice")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()