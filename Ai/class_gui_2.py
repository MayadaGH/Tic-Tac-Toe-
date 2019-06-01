# import tkinter
from tkinter import *
from tkinter import messagebox, simpledialog
from pygame import *

# from tic_tac_toe import Board

c = 0


# import os


def win():
    import pygame
    mixer.init()
    mixer.music.load('win.ogg')
    mixer.music.play(0)
    while mixer.music.get_busy():
        pygame.time.Clock().tick()


def lose():
    import pygame
    mixer.init()
    mixer.music.load('lose.ogg')
    mixer.music.play(0)
    while mixer.music.get_busy():
        pygame.time.Clock().tick()


def printCell(cell):
    return str(cell)


#     color = Fore.BLUE
#     if cell == 'X':
#         color = Fore.GREEN
#     elif cell == 'O':
#         color = Fore.RED
#     else:
#         color = Fore.BLUE
#
#     return color + str(cell) + Style.RESET_ALL


class Board():
    currentTurn = 'X'
    calls = 0
    whoWon = 'No one'
    initialDepth = 0
    temp_depth = 0

    def __init__(self):
        self.currentTurn = 'X'
        self.calls = 0
        self.whoWon = 'No one'
        self.initialDepth = 1
        self.temp_depth = 0
        self.cells = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def updateCell(self, cellNumber, player):
        if (cellNumber <= 0 or cellNumber > 9):
            return False

        if self.isEmptyCell(self.cells[cellNumber - 1]):
            self.cells[cellNumber - 1] = player
            return True
        return False

    def bestMove(self):
        res = self.minimax('O')
        print(res)
        # print 'CALLS:' + str(self.calls)
        return res.get("index")

    def minimax(self, player, depth=0):
        global c
        c += 1
        # get empty cells
        emptyCells = self.getEmptyCells()

        ## check if game over
        if (self.isWinner('X') == -1):
            temp_dict = {'score': 0, 'depth': self.temp_depth}
            self.temp_depth = 0
            return temp_dict

        ## assign score to moves
        if (self.isWinner('X') == 1):
            temp_dict = {'score': -10, 'depth': self.temp_depth}
            self.temp_depth = 0
            return temp_dict
        elif (self.isWinner('O') == 1):
            temp_dict = {'score': 10, 'depth': self.temp_depth}
            self.temp_depth = 0
            return temp_dict
        elif (len(emptyCells) == 0):
            temp_dict = {'score': 10, 'depth': self.temp_depth}
            self.temp_depth = 0
            return temp_dict

        if (depth == self.initialDepth):
            temp_dict = {'score': 10, 'depth': self.temp_depth}
            self.temp_depth = 0
            return temp_dict

        moves = []
        self.temp_depth += 1
        for i in range(0, len(self.cells)):  # len out of for loop
            if (self.isEmptyCell(self.cells[i])):
                move = {}
                move["index"] = self.cells[i]
                self.cells[i] = player

                if player == 'O':
                    result = self.minimax('X', depth + 1)
                    move["score"] = result.get("score")
                    move['depth'] = result.get('depth')
                else:
                    result = self.minimax('O', depth + 1)
                    move["score"] = result.get("score")
                    move['depth'] = result.get('depth')

                # set the old value back
                self.cells[i] = move.get("index")

                # add the move to 'moves' list to check after recursion is done

                moves.append(move)

            move = {}

        bestMove = 3

        if (player == 'O'):
            bestScore = -10000
            init_depth = 10000
            for y in range(0, len(moves)):
                if (moves[y].get("score") >= bestScore and moves[y].get('depth') < init_depth):
                    bestScore = moves[y].get("score")
                    bestMove = y
                    ## stop when reaching 10 score, no need to continue.
                    if (bestScore == 10):
                        break
        else:
            bestScore = 10000
            init_depth = -10000
            for y in range(0, len(moves)):
                if (moves[y].get("score") <= bestScore and moves[y].get('depth') > init_depth):
                    bestScore = moves[y].get("score")
                    bestMove = y
                    ## stop when reaching 10 score, no need to continue.
                    if (bestScore == -10):
                        break

        return moves[bestMove]

    def checkWinner(self):
        if (self.isWinner('X') or self.isWinner('O') or self.isWinner('X') == -1 or self.isWinner('O') == -1):
            print
            'Game ended'
            if (self.whoWon != 'No one'):
                print
                'Player ' + printCell(self.whoWon) + ' won!'
            else:
                print
                'No one won. That\'s a draw!'
            return True
        else:
            return False

    def isWinner(self, player):
        # Rows
        if self.cells[0] == player and self.cells[1] == player and self.cells[2] == player:
            self.whoWon = player
            return 1
        if self.cells[3] == player and self.cells[4] == player and self.cells[5] == player:
            self.whoWon = player
            return 1
        if self.cells[6] == player and self.cells[7] == player and self.cells[8] == player:
            self.whoWon = player
            return 1
        # Columns
        if self.cells[0] == player and self.cells[3] == player and self.cells[6] == player:
            self.whoWon = player
            return 1
        if self.cells[1] == player and self.cells[4] == player and self.cells[7] == player:
            self.whoWon = player
            return 1
        if self.cells[2] == player and self.cells[5] == player and self.cells[8] == player:
            self.whoWon = player
            return 1
        # Diagonal 1 (/)
        if self.cells[2] == player and self.cells[4] == player and self.cells[6] == player:
            self.whoWon = player
            return 1
        # Diagonal 2 (\)
        if self.cells[0] == player and self.cells[4] == player and self.cells[8] == player:
            self.whoWon = player
            return 1
        if self.getEmptyCells(True) == 0:
            self.whoWon = 'No one'
            return -1
        return 0

    def isEmptyCell(self, cell):
        if (str(cell).upper() != 'X' and str(cell).upper() != 'O'):
            return True
        return False

    def getEmptyCells(self, displayCount=False):
        emptyCellsCount = 0;
        emptyCells = []
        for cell in self.cells:
            if self.isEmptyCell(cell):
                emptyCellsCount += 1
                emptyCells.append(self.cells.index(cell))

        if (displayCount):
            return emptyCellsCount
        return emptyCells


###########################################################################
tk = Tk()
tk.configure(background='white')
tk.title("Tic Tac Toe")

HUMAN_BG = 'orange'
AI_BG = 'red'
BG_TEXT = 'black'
NORMAL_BG = 'white'
CLICKED_COLOR_X = 'DarkTurquoise'
CLICKED_COLOR_O = 'DarkGreen'
temp_cell_index = -1


class ClassGui:
    click = True
    buttons = StringVar()
    b = 0

    def __init__(self):
        self.b = Board()
        self.render_buttons = [None for _ in range(0, 9)]
        self.init_buttons()

    #  self.show()

    def colorandwrite(self, buttons):

        if self.b.isEmptyCell(buttons['text']) and self.click:
            self.b.updateCell(int(buttons["text"]), 'X')
            buttons["text"] = "X"
            buttons["fg"] = 'white'
            buttons["bg"] = CLICKED_COLOR_X
            if (self.b.checkWinner()):
                messagebox.showinfo("The Winner IS", "Winner is " + self.b.whoWon)
                if (self.b.whoWon == "X"):
                    win()
                    result = messagebox.askquestion("Exit", "Do you want to exit", icon='warning')
                    if result == 'yes':
                        exit()
                    else:
                        v = ClassGui()
                        print(v)

                else:
                    lose()
                    result = messagebox.askquestion("Exit", "Do you want to exit", icon='warning')
                    if result == 'yes':
                        exit()
                    else:
                        c = ClassGui()
                        print(c)

            self.click = False
            self.play_ai()
            buttons['state'] = 'disabled'  # making cells choosen by the computer disabled
            buttons['disabledforeground'] = 'white'
            if (self.b.checkWinner()):
                messagebox.showinfo("The Winner IS", "Winner is " + self.b.whoWon)
                if (self.b.whoWon == "X"):
                    win()
                    result = messagebox.askquestion("Exit", "Do you want to exit", icon='warning')
                    if result == 'yes':
                        exit()
                    else:
                        c = ClassGui()
                        print(c)
                else:
                    lose()
                    result = messagebox.askquestion("Exit", "Do you want to exit", icon='warning')
                    if result == 'yes':
                        exit()
                    else:
                        c = ClassGui()
                        print(c)
        else:
            print('this game is not for dummies ')

    # AI Turn
    def play_ai(self):
        if self.b.bestMove()is None :
            exit()
        else:
            best_move = int(self.b.bestMove())
            print(best_move)
            print(str(c))
            self.b.updateCell(best_move, 'O')
            button = self.render_buttons[best_move - 1]
            button["text"] = "O"
            button["fg"] = 'white'
            button["bg"] = CLICKED_COLOR_O
            # buttons['state'] = 'disabled'
            # buttons['disabledforeground'] = 'white'
            self.click = True

    def init_buttons(self):
        answer = simpledialog.askstring("Input", "enter 0 for easy 1 for medium 2 for hard",
                                        parent=tk)
        while answer != "0" and answer != "1" and answer != "2":
            if answer is None:
                exit()
            else:
                messagebox.showinfo("Not Valid Input", "Please Enter Valid Number ")
                answer = simpledialog.askstring("Input", "enter 0 for easy 1 for medium 2 for hard", parent=tk)
        if int(answer) == 0:
            self.b.initialDepth = 1
        elif int(answer) == 1:
            self.b.initialDepth = 3
        elif int(answer) == 2:
            self.b.initialDepth = 9

        row = 1
        col = 0
        for i in range(0, 9):
            if col == 3:
                col = 0
                row += 1
            self.render_buttons[i] = Button(tk, text=str(i + 1), font='Ubuntu 20 bold', bg='white', fg='white',
                                            relief=SOLID, borderwidth=2, highlightthickness=4,
                                            height=3, width=8,
                                            command=lambda i=i: self.colorandwrite(self.render_buttons[i]))
            self.render_buttons[i].grid(row=row, column=col, sticky=S + N + E + W)
            col += 1
        tk.mainloop()


c = ClassGui()
print(c)
