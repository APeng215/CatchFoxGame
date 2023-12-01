import tkinter
import random
from tkinter import font


class Fox:
    def __init__(self):
        self.__holePos = random.randint(1, 5)

    def getHolePos(self):
        return self.__holePos

    def posMove(self):
        if self.getHolePos() == 1:
            self.__holePos = 2
            return
        if self.getHolePos() == 5:
            self.__holePos = 4
            return
        if random.random() < 0.5:
            self.__holePos += 1
        else:
            self.__holePos -= 1


class FoxGame:
    def __init__(self, maxStep):
        self.__maxStep = maxStep
        self.__fox = Fox()
        self.__day = 1
        self.__isGameRunning = False
        self.__win = False
        self.__lose = False

    def isWinning(self):
        return self.__win

    def isLosing(self):
        return self.__lose

    def getFoxPos(self):
        return self.__fox.getHolePos()

    def getDay(self):
        return self.__day

    def isGameRunning(self):
        return self.__isGameRunning

    def try2ChooseHole(self, holeIndex):
        if not self.__isGameRunning:
            print("Game is not on running!")
            return
        if holeIndex == self.getFoxPos():
            self.__wins()
            return
        # Day passes
        self.__day += 1
        self.__fox.posMove()
        if self.__day > self.__maxStep:
            self.__loses()

    def __loses(self):
        self.__lose = True
        self.__isGameRunning = False

    def __wins(self):
        self.__win = True
        self.__isGameRunning = False

    def resetAndStart(self):
        self.__fox = Fox()
        self.__day = 1
        self.__win = False
        self.__lose = False
        self.__isGameRunning = True


class GameWindow:
    def __init__(self):
        self.__initWindow()
        self.__centerWindow()

    def __centerWindow(self):
        # Get the screen width and height
        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()

        # Calculate the center coordinates
        x_coordinate = (screen_width - self.__root.winfo_reqwidth()) / 2
        y_coordinate = (screen_height - self.__root.winfo_reqheight()) / 2

        # Set the geometry of the window to be centered
        self.__root.geometry(f"+{int(x_coordinate)}+{int(y_coordinate)}")

    def start(self):
        self.__root.mainloop()
        return self

    def __startGame(self):
        self.__game = FoxGame(5)
        self.__game.resetAndStart()
        self.__startButton.pack_forget()
        self.__packCanvas()
        self.__setMessageBox()
        self.__setSelectingButtons()
        self.__packRestartButton()
        self.__centerWindow()

    def __setSelectingButtons(self):
        self.__initSelectingButtons()
        self.__placeSelectingButtons()

    def __setMessageBox(self):
        self.__output = tkinter.StringVar(value=f"Day #{self.__game.getDay()}/5: Choose a hole")
        self.__message = tkinter.Message(self.__root, textvariable=self.__output, width=25 * 50, bg="lightblue",
                                         font=self.__minecraftBigFont)
        self.__message.pack(fill="x", expand=True)

    def __initSelectingButtons(self):
        self.__selectingFrame = tkinter.Frame(self.__root)
        buttonWidth = 16
        self.__button1 = tkinter.Button(self.__selectingFrame, text="1", width=buttonWidth,
                                        command=lambda: self.__chooseHole(1), font=self.__minecraftSmallFont)
        self.__button2 = tkinter.Button(self.__selectingFrame, text="2", width=buttonWidth,
                                        command=lambda: self.__chooseHole(2), font=self.__minecraftSmallFont)
        self.__button3 = tkinter.Button(self.__selectingFrame, text="3", width=buttonWidth,
                                        command=lambda: self.__chooseHole(3), font=self.__minecraftSmallFont)
        self.__button4 = tkinter.Button(self.__selectingFrame, text="4", width=buttonWidth,
                                        command=lambda: self.__chooseHole(4), font=self.__minecraftSmallFont)
        self.__button5 = tkinter.Button(self.__selectingFrame, text="5", width=buttonWidth,
                                        command=lambda: self.__chooseHole(5), font=self.__minecraftSmallFont)
        self.__button1.pack(side=tkinter.LEFT)
        self.__button2.pack(side=tkinter.LEFT)
        self.__button3.pack(side=tkinter.LEFT)
        self.__button4.pack(side=tkinter.LEFT)
        self.__button5.pack(side=tkinter.LEFT)

    def __chooseHole(self, holeIndex):
        self.__game.try2ChooseHole(holeIndex)

        if self.__game.isGameRunning():
            self.__output.set(f"Day #{self.__game.getDay()}/5: Choose a hole")
            return
        if self.__game.isWinning():
            self.__winHandler()
        else:
            self.__lossHandler()
        self.__switch2RestartScreen()

    def __lossHandler(self):
        self.__setLossMessage()
        self.__setMessageBgColor("red")
        self.__setMessageColor("white")
        self.__placeFoxInCanvas(self.__getFoxPost())

    def __getFoxPost(self):
        return self.__game.getFoxPos()

    def __winHandler(self):
        self.__setWinningMessage()
        self.__setMessageBgColor("lightgreen")
        self.__placeFoxInCanvas(self.__getFoxPost())

    def __setLossMessage(self):
        self.__output.set(f"You lose. Fox is in hole #{self.__getFoxPost()} today")

    def __setMessageBgColor(self, color):
        self.__message.config(bg=color)

    def __setWinningMessage(self):
        self.__output.set(f"You win! Fox found in hole #{self.__getFoxPost()}")

    def __switch2RestartScreen(self):
        self.__packRestartButton()
        self.__removeSelectingButtons()

    def __initRestartButton(self):
        self.__restartButton = tkinter.Button(self.__root, text="Restart", fg="red", width=10, command=self.__restart,
                                              font=self.__minecraftSmallFont)

    def __removeSelectingButtons(self):
        self.__selectingFrame.pack_forget()

    def __restart(self):
        self.__game.resetAndStart()
        self.__output.set(f"Day #{self.__game.getDay()}/5: Choose a hole")
        self.__resetMessageBox()
        self.__removeRestartButton()
        self.__placeSelectingButtons()
        self.__packRestartButton()
        self.__removeFoxFromCanvas()

    def __packRestartButton(self):
        self.__restartButton.pack()

    def __removeRestartButton(self):
        self.__restartButton.pack_forget()

    def __resetMessageBox(self):
        self.__setMessageBgColor("lightblue")
        self.__setMessageColor("black")

    def __placeSelectingButtons(self):
        self.__selectingFrame.pack()

    def __initWindow(self):
        self.__initRoot()
        self.__initFont()
        self.__initAndPlaceStartButton()
        self.__initRestartButton()
        self.__initCanvas()

    def __initAndPlaceStartButton(self):
        self.__startButton = tkinter.Button(self.__root, text="Start", fg="green", width=25, command=self.__startGame,
                                            font=self.__minecraftBigFont)
        self.__startButton.pack()

    def __initRoot(self):
        self.__root = tkinter.Tk()
        self.__root.title("Fox Game")

    def __initCanvas(self):
        self.__fetchBgImage()
        self.__fetchFoxImages()
        self.__canvas = tkinter.Canvas(self.__root, width=self.__bgImage.width(), height=self.__bgImage.height())
        self.__setBg2Canvas()

    def __fetchBgImage(self):
        self.__bgImage = tkinter.PhotoImage(file="foxgame_backgound.png")

    def __setBg2Canvas(self):
        self.__canvas.create_image(0, 0, anchor=tkinter.NW, image=self.__bgImage)

    def __removeFoxFromCanvas(self):
        self.__canvas.delete(self.__foxImageId)

    def __placeFoxInCanvas(self, holeIndex):
        RedFox = 1
        WhiteFox = 2

        foxType = random.randint(1, 2)
        if foxType == RedFox:
            if holeIndex == 1:
                self.__foxImageId = self.__canvas.create_image(81, 144, anchor=tkinter.NW, image=self.__redFoxImage)
            if holeIndex == 2:
                self.__foxImageId = self.__canvas.create_image(259, 147, anchor=tkinter.NW, image=self.__redFoxImage)
            if holeIndex == 3:
                self.__foxImageId = self.__canvas.create_image(437, 149, anchor=tkinter.NW, image=self.__redFoxImage)
            if holeIndex == 4:
                self.__foxImageId = self.__canvas.create_image(614, 149, anchor=tkinter.NW, image=self.__redFoxImage)
            if holeIndex == 5:
                self.__foxImageId = self.__canvas.create_image(800, 149, anchor=tkinter.NW, image=self.__redFoxImage)
            return
        if foxType == WhiteFox:
            if holeIndex == 1:
                self.__foxImageId = self.__canvas.create_image(81, 144, anchor=tkinter.NW, image=self.__whiteFoxImage)
            if holeIndex == 2:
                self.__foxImageId = self.__canvas.create_image(259, 147, anchor=tkinter.NW, image=self.__whiteFoxImage)
            if holeIndex == 3:
                self.__foxImageId = self.__canvas.create_image(437, 149, anchor=tkinter.NW, image=self.__whiteFoxImage)
            if holeIndex == 4:
                self.__foxImageId = self.__canvas.create_image(614, 149, anchor=tkinter.NW, image=self.__whiteFoxImage)
            if holeIndex == 5:
                self.__foxImageId = self.__canvas.create_image(800, 149, anchor=tkinter.NW, image=self.__whiteFoxImage)
            return

    def __packCanvas(self):
        self.__canvas.pack()

    def __fetchFoxImages(self):
        self.__redFoxImage = tkinter.PhotoImage(file="red_fox.png")
        self.__whiteFoxImage = tkinter.PhotoImage(file="white_fox.png")

    def __setMessageColor(self, color):
        self.__message.config(fg=color)

    def __initFont(self):
        self.__minecraftBigFont = font.Font(family="Minecraftia", size=24)
        self.__minecraftSmallFont = font.Font(family="Minecraftia", size=12)


if __name__ == "__main__":
    gameClient = GameWindow()
    gameClient.start()
