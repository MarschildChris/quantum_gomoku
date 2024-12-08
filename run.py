from tkinter import *
from time import *
import sys
import time
import numpy as np
from idna import check_initial_combiner

myInterface = Tk()
s = Canvas(myInterface, width=800, height=800, background= "#e8e0c8")
s.pack()

#Board SizeGomoku.py
Board_Size = 15
Frame_Gap = 35
width = 500
height = 500


def create_circle(x, y, radius, fill = "", outline = "black", width = 1):
    c=s.create_oval(x - radius, y - radius, x + radius, y + radius, fill = fill, outline = outline, width = width)
    return c

def delete_circle(c):
    global circles
    s.delete(c)
    circles.remove(c)

def Value_Check_int(Value):
    try:
        Value = int(Value)
    except ValueError:
        return "string"
    else:
        return "int"

def MouseClick(event):
    global Click_Cord
    X_click = event.x
    Y_click = event.y
    Click_Cord = Piece_Location(X_click, Y_click)
    print(Click_Cord)

s.bind("<Button-1>", MouseClick)

Click_Cord = [None, None]

def Piece_Location(X_click, Y_click):
    X = None
    Y = None
    for i in range(len(Actual_CordX1)):

        if X_click > Actual_CordX1[i] and X_click < Actual_CordX2[i]:
            X = Game_CordX[i]

        if Y_click > Actual_CordY1[i] and Y_click < Actual_CordY2[i]:
            Y = Game_CordY[i]

    return X, Y

def Location_Validation():

    global isMeasure
    global isQuantum
    global Turn_Num

    v = False

    if X == None or Y == None:
        return False

    elif board[Y - 1][X - 1] == 0 and not isMeasure:
        v = True
    elif isMeasure:
        if board[Y - 1][X - 1] == 3 or board[Y - 1][X - 1] == 4 or board[Y - 1][X - 1] == 5:
            v = True
    elif isQuantum:
        print("bnum",board[Y - 1][X - 1])
        if board[Y - 1][X - 1] == 3 and Turn_Num % 2 == 1:
            v = True
        if board[Y - 1][X - 1] == 4 and Turn_Num % 2 == 0:
            v = True

    return v

def Score_Board():
    if Winner == None:
        Turn_Text = s.create_text(width / 2+100, height - Frame_Gap+5, text = "Turn = " + Turn, font = "Helvetica 15 bold", fill = Turn)
        return Turn_Text
    else:
        s.create_text(width / 2 +100, height - Frame_Gap + 5, text = Winner.upper() + " WINS!", font = "Helvetica 15 bold", fill = Winner.lower())

def winCheck(Piece_Number, Piece_Colour, board):
    if rowCheck(Piece_Number, board) or rowCheck(Piece_Number, transpose(board)) or rowCheck(Piece_Number, transposeDiagonalInc(board)) or rowCheck(Piece_Number, transposeDiagonalDec(board)):
        Winner = Piece_Colour
        return Winner

def rowCheck(Piece_Number, board):
    for i in range(len(board)):
        if board[i].count(Piece_Number) >= 5:

            for z in range(len(board) - 3): #may cause issue
                Connection = 0

                for c in range(5):
                    print("z+c:",(z+c))
                    if (z+c)<15 and board[i][z + c] == Piece_Number:
                        Connection += 1

                    else:
                        break

                    if Connection == 5:
                        return True

def getDiagonalDec(loa, digNum):
    lst=[]
    if digNum <= len(loa) - 1:
        index = len(loa) - 1
        for i in range(digNum, -1, -1):
            lst.append(loa[i][index])
            index -= 1
        return lst
    else:
        index = (len(loa) * 2 - 2) - digNum
        for i in range(len(loa) - 1, digNum - len(loa), -1):
            lst.append(loa[i][index])
            index -= 1
        return lst


def transposeDiagonalDec(loa):
    lst = []
    for i in range(len(loa) * 2 - 1):
        lst.append(getDiagonalDec(loa, i))
    return lst

def getDiagonalInc(loa, digNum):
    lst=[]
    if digNum <= len(loa) - 1:
        index = 0
        for i in range(digNum, -1, -1):
            lst.append(loa[i][index])
            index += 1
        return lst
    else:
        index =  digNum - len(loa) + 1
        for i in range(len(loa) - 1, digNum - len(loa), -1):
            lst.append(loa[i][index])
            index += 1
        return lst


def transposeDiagonalInc(loa):
    lst = []
    for i in range(len(loa) * 2 - 1):
        lst.append(getDiagonalInc(loa, i))
    return lst

def transpose(loa):
    lst = []
    for i in range(len(loa)):
        lst.append(getCol(loa, i))
    return lst

def getCol(loa, colNum):
    lst = []
    for i in range(len(loa)):
        lst.append(loa[i][colNum])
    return lst

def addQubit():
    qc=qs.QuantumCircuit(2,2)
    qc.h(0)
    qc.x(1)
    qc.cx(0,1)




#Board
Board_Size = Board_Size - 1
Board_X1 = width / 10
Board_Y1 = height / 10
Board_GapX = (width - Board_X1 * 2) / Board_Size
Board_GapY = (height - Board_Y1 * 2) / Board_Size

#Chess Piece
Chess_Radius = (Board_GapX * (9 / 10)) / 2

#Turn
Turn_Num = 1
Turn = "white"
Winner = None

#Cord List
Black_Cord_PickedX = []
Black_Cord_PickedY = []
White_Cord_PickedX = []
White_Cord_PickedY = []
Quantum_White_Cord_Picked = []
Quantum_Black_Cord_Picked = []
Quantum_Picked=[]
circles = []

#Click Detection Cord
Game_CordX = []
Game_CordY = []
Actual_CordX1 = []
Actual_CordY1 = []
Actual_CordX2 = []
Actual_CordY2 = []

#2D Board List
board = []

#quantum
isQuantum = False
#quantum List
quantumList = []

#
isMeasure = False

def quantum():
    global isQuantum
    global isMeasure
    isQuantum = True
    if isMeasure:
        isMeasure = False



def measure():
    global isQuantum
    global isMeasure
    isMeasure = True
    if isQuantum:
        isQuantum = False

def collpse(X,Y,isDetermined):
    global Quantum_Black_Cord_Picked
    global Quantum_White_Cord_Picked
    global Quantum_Picked
    global board


    if board[Y - 1][X - 1] == 5:


        n = np.random.choice([0, 1])
        if n:
            board[Y - 1][X - 1] = 4
            collpse(X, Y, False)
            board[Y - 1][X - 1] = 3
            chess = create_circle(Board_X1 + Board_GapX * (X - 1), Board_Y1 + Board_GapY * (Y - 1), radius=Chess_Radius,
                                  outline="Black", width=2)
            circles.append(chess)
            Quantum_Picked.append([X, Y])
            if board[Y - 1][X - 1] == 0:
                collpse(X, Y, False)
            else:
                collpse(X, Y, True)
                board[Y - 1][X - 1] = 4
        else:
            board[Y - 1][X - 1] = 3
            collpse(X, Y, False)
            board[Y - 1][X - 1] = 4
            chess = create_circle(Board_X1 + Board_GapX * (X - 1), Board_Y1 + Board_GapY * (Y - 1), radius=Chess_Radius,
                                  outline="White", width=2)
            circles.append(chess)
            Quantum_Picked.append([X, Y])
            if board[Y - 1][X - 1] == 0:
                collpse(X, Y, False)
            else:
                collpse(X, Y, True)
                board[Y - 1][X - 1] = 3




    elif board[Y - 1][X - 1] == 3:
        i1 = Quantum_Black_Cord_Picked.index([X, Y])
        [x1,y1]=Quantum_Black_Cord_Picked.pop(i1)
        if i1 % 2 == 0:
            [x2,y2]=Quantum_Black_Cord_Picked.pop(i1)
        else:
            [x2,y2]=Quantum_Black_Cord_Picked.pop(i1-1)

        if isDetermined:
            n=0
        else:
            n = np.random.choice([0, 1])
        if n:
            ic = Quantum_Picked.index([x1, y1])
            delete_circle(circles[ic])
            Quantum_Picked.pop(ic)
            create_circle(Board_X1 + Board_GapX * (x1 - 1), Board_Y1 + Board_GapY * (y1 - 1), radius=Chess_Radius,
                          fill="Black")
            board[y1 - 1][x1 - 1] = 1
            ##now deal with its pair
            ic = Quantum_Picked.index([x2, y2])
            if board[y2 - 1][x2 - 1] ==  3:
                delete_circle(circles[ic])
                Quantum_Picked.pop(ic)
                board[y2 - 1][x2 - 1] = 0
            else:
                s.itemconfig(circles[ic], outline='white')
                board[y2 - 1][x2 - 1] = 4

        else:
            ic = Quantum_Picked.index([x1, y1])
            delete_circle(circles[ic])
            Quantum_Picked.pop(ic)
            board[y1 - 1][x1 - 1] = 0
            ##now deal with its pair
            ic = Quantum_Picked.index([x2, y2])
            if board[y2 - 1][x2 - 1] == 3:
                delete_circle(circles[ic])
                Quantum_Picked.pop(ic)
                create_circle(Board_X1 + Board_GapX * (x2 - 1), Board_Y1 + Board_GapY * (y2 - 1), radius=Chess_Radius,
                              fill="Black")
                board[y2 - 1][x2 - 1] = 1
            else:
                s.itemconfig(circles[ic], outline='white')
                board[y2 - 1][x2 - 1] = 4
                collpse(x2,y2,True)
                create_circle(Board_X1 + Board_GapX * (x2 - 1), Board_Y1 + Board_GapY * (y2 - 1), radius=Chess_Radius,
                              fill="Black")
                board[y2 - 1][x2 - 1] = 1




    elif board[Y - 1][X - 1] == 4:
        i1 = Quantum_White_Cord_Picked.index([X, Y])
        [x1, y1] = Quantum_White_Cord_Picked.pop(i1)
        if i1 % 2 == 0:
            i2 = i1 + 1
            [x2, y2] = Quantum_White_Cord_Picked.pop(i1)
        else:
            i2 = i1 - 1
            [x2, y2] = Quantum_White_Cord_Picked.pop(i2)

        if isDetermined:
            n = 0
        else:
            n = np.random.choice([0, 1])
        if n:
            ic = Quantum_Picked.index([x1, y1])
            delete_circle(circles[ic])
            Quantum_Picked.pop(ic)
            create_circle(Board_X1 + Board_GapX * (x1 - 1), Board_Y1 + Board_GapY * (y1 - 1), radius=Chess_Radius,
                          fill="White")
            board[y1 - 1][x1 - 1] = 2
            ##now deal with its pair
            ic = Quantum_Picked.index([x2, y2])
            if board[y2 - 1][x2 - 1] == 4:
                delete_circle(circles[ic])
                Quantum_Picked.pop(ic)
                board[y2 - 1][x2 - 1] = 0
            else:
                s.itemconfig(circles[ic], outline='black')
                board[y2 - 1][x2 - 1] = 3

        else:
            ic = Quantum_Picked.index([x1, y1])
            delete_circle(circles[ic])
            Quantum_Picked.pop(ic)
            board[y1 - 1][x1 - 1] = 0
            ##now deal with its pair
            ic = Quantum_Picked.index([x2, y2])
            if board[y2 - 1][x2 - 1] == 4:
                delete_circle(circles[ic])
                Quantum_Picked.pop(ic)
                create_circle(Board_X1 + Board_GapX * (x2 - 1), Board_Y1 + Board_GapY * (y2 - 1), radius=Chess_Radius,
                              fill="White")
                board[y2 - 1][x2 - 1] = 2
            else:
                s.itemconfig(circles[ic], outline='white')
                board[y2 - 1][x2 - 1] = 3
                collpse(x2, y2, True)
                create_circle(Board_X1 + Board_GapX * (x2 - 1), Board_Y1 + Board_GapY * (y2 - 1), radius=Chess_Radius,
                              fill="White")
                board[y2 - 1][x2 - 1] = 2




def Exit():
    global Winner
    Winner = "Exit"
    myInterface.destroy()

def restart():
    global Turn_Num
    global Turn

    # 2D Board List
    global board
    global isQuantum

    # Turn
    Turn_Num = 1
    Turn = "white"
    # 2D Board List
    board = []
    isQuantum = False
    s.update()

#Buttons
Q = Button(myInterface, text = "Quantum", font = "Helvetica 10 bold", command = quantum, bg = "white", fg = "black")
Q.pack()
Q.place(x = width / 2 * 0.5 - 80, y = height - Frame_Gap * 1.6 + 15, height = Chess_Radius * 2, width = Chess_Radius * 7)

M = Button(myInterface, text = "Measure", font = "Helvetica 10 bold", command = measure, bg = "white", fg = "black")
M.pack()
M.place(x = width / 2 * 0.5+20, y = height - Frame_Gap * 1.6 + 15, height = Chess_Radius * 2, width = Chess_Radius * 7)

E = Button(myInterface, text = "Restart", font = "Helvetica 10 bold", command = restart, bg = "white", fg = "black")
E.pack()
E.place(x = width / 2 * 0.5-80, y = height - Frame_Gap * 1.6 + 50, height = Chess_Radius * 2, width = Chess_Radius * 7)

R = Button(myInterface, text = "EXIT", font = "Helvetica 10 bold", command = Exit, bg = "white", fg = "black")
R.pack()
R.place(x = width / 2 * 0.5+20, y = height - Frame_Gap * 1.6 + 50, height = Chess_Radius * 2, width = Chess_Radius * 7)


#2D list for gameboard
for i in range(Board_Size + 1):
    board.append([0] * (Board_Size + 1))

Unfilled = 0
Black_Piece = 1
White_Piece = 2

#Fills Empty List
for z in range(1, Board_Size + 2):

    for i in range(1, Board_Size + 2):
        Game_CordX.append(z)
        Game_CordY.append(i)
        Actual_CordX1.append((z - 1) * Board_GapX + Board_X1 - Chess_Radius)
        Actual_CordY1.append((i - 1) * Board_GapY + Board_Y1 - Chess_Radius)
        Actual_CordX2.append((z - 1) * Board_GapX + Board_X1 + Chess_Radius)
        Actual_CordY2.append((i - 1) * Board_GapY + Board_Y1 + Chess_Radius)

#Create Board
s.create_rectangle(Board_X1 - Frame_Gap, Board_Y1 - Frame_Gap, Board_X1 + Frame_Gap + Board_GapX * Board_Size, Board_Y1 + Frame_Gap + Board_GapY * Board_Size, width = 3)

for f in range(Board_Size + 1):
    s.create_line(Board_X1, Board_Y1 + f * Board_GapY, Board_X1 + Board_GapX * Board_Size, Board_Y1 + f * Board_GapY)
    s.create_line(Board_X1 + f * Board_GapX, Board_Y1, Board_X1 + f * Board_GapX, Board_Y1 + Board_GapY * Board_Size)

    s.create_text(Board_X1 - Frame_Gap * 1.7, Board_Y1 + f * Board_GapY, text = f + 1, font = "Helvetica 10 bold", fill = "black")
    s.create_text(Board_X1 + f * Board_GapX, Board_Y1 - Frame_Gap * 1.7, text = f + 1, font = "Helvetica 10 bold", fill = "black")

Turn_Text = Score_Board()

quantumMove=0
#Game Code
while Winner is None:
    s.update()
    X = Click_Cord[0]
    Y = Click_Cord[1]

    Picked = Location_Validation()

    if Picked:

        print("turn number:", Turn_Num)
        s.delete(Turn_Text)

        if isQuantum:
            if board[Y - 1][X - 1] == 3 or board[Y - 1][X - 1] == 4:
                print("board num",board[Y - 1][X - 1])
                index = Quantum_Picked.index([X, Y])
                s.itemconfig(circles[index],outline='grey')
                board[Y - 1][X - 1] = 5
                quantumMove+=1
                if Turn_Num % 2 == 1:
                    Quantum_White_Cord_Picked.append([X,Y])
                elif Turn_Num % 2 == 0:
                    Quantum_Black_Cord_Picked.append([X,Y])
            else:
                chess=create_circle(Board_X1 + Board_GapX * (X - 1), Board_Y1 + Board_GapY * (Y - 1), radius=Chess_Radius,outline = Turn,width=2)
                circles.append(chess)
                Quantum_Picked.append([X,Y])
                quantumMove+=1
                if Turn_Num % 2 == 1:
                    Quantum_White_Cord_Picked.append([X,Y])
                    board[Y - 1][X - 1] = 4
                elif Turn_Num % 2 == 0:
                    Quantum_Black_Cord_Picked.append([X,Y])
                    board[Y - 1][X - 1] = 3
            if quantumMove == 2:
                isQuantum = False
                quantumMove = 0
                Turn_Num = Turn_Num + 1
                if Turn == "black":
                    Turn = "white"
                else:
                    Turn = "black"



        elif isMeasure:
            collpse(X,Y,False)
            Turn_Num = Turn_Num + 1
            if Turn == "black":
                Turn = "white"
            else:
                Turn = "black"
            isMeasure = False


        else:
            create_circle(Board_X1 + Board_GapX * (X - 1), Board_Y1 + Board_GapY * (Y - 1), radius = Chess_Radius, fill = Turn)
            if Turn_Num % 2 == 1:
                White_Cord_PickedX.append(X)
                White_Cord_PickedY.append(Y)
                board[Y - 1][X - 1] = 2
                Turn = "black"
            elif Turn_Num % 2 == 0:
                Black_Cord_PickedX.append(X)
                Black_Cord_PickedY.append(Y)
                board[Y - 1][X - 1] = 1
                Turn = "white"
            Turn_Num = Turn_Num + 1

        Turn_Text = Score_Board()
        print("white cord:", Quantum_White_Cord_Picked)
        print("black cord:", Quantum_Black_Cord_Picked)
        print("quantum circle",Quantum_Picked)
        print("board nubmer:")
        for i in Quantum_Picked:
            print(board[i[1]-1][i[0]-1])

        print("board len:",len(board[0]))



        if Turn == "white":
            Colour_Check = Black_Piece
            Win_Check = "Black"

        elif Turn == "black":
            Colour_Check = White_Piece
            Win_Check = "White"

        Winner = winCheck(Colour_Check, Win_Check, board)
        Click_Cord = [None, None]
        X=None
        Y=None

s.delete(Turn_Text)
Score_Board()
s.update()

time.sleep(5)