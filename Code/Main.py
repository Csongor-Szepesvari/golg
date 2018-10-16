import random as r

#Handle the central logic of the game

class Cell():
    def __init__(self, pos, gridMax):
        #assumes that BLUE is counted in negatives and RED in positives
        self.filled = False
        self.colour = "BLANK" #possible colours are BLUE and RED or BLANK
        self.future = "BLANK"
        self.printColour = " "
        self.neighbours = self.calcNeighbours(pos, gridMax-1)
        self.neighboursCalc = 0

    def calcNextGen(self, grid):
        #calculates the next iteration of the grid on the current generation
        totalAlive = 0
        #print(self.neighbours)
        for i in range(len(self.neighbours)):
            if grid[self.neighbours[i][0]][self.neighbours[i][1]].colour == "RED":
                totalAlive += 1
            elif grid[self.neighbours[i][0]][self.neighbours[i][1]].colour == "BLUE":
                totalAlive -= 1
        if totalAlive < -3:
            self.future = "BLANK"
        elif totalAlive == -3:
            self.future = "BLUE"
        elif totalAlive > -2 and totalAlive < 2:
            self.future = "BLANK"
        elif totalAlive == 3:
            self.future = "RED"
        else:
            self.future = "BLANK"
        self.neighboursCalc = totalAlive

    def createNextGen(self):
        #Makes a new generation, must have run calcNextGen on all grid cells prior to using this function
        if self.future != "BLANK":
            self.filled = True
            self.printColour = self.future[0]
        else:
            self.filled = False
            self.printColour = " "
        self.colour = self.future


    def calcNeighbours(self, pos, gridMax):
        i = pos[0]
        j = pos[1]
        neighbourPotential = [[],[]]
        if i == 0:
            neighbourPotential[0].append(i)
            neighbourPotential[0].append(i+1)
        elif i == gridMax:
            neighbourPotential[0].append(i)
            neighbourPotential[0].append(i-1)
        else:
            neighbourPotential[0].append(i-1)
            neighbourPotential[0].append(i)
            neighbourPotential[0].append(i+1)

        if j == 0:
            neighbourPotential[1].append(j)
            neighbourPotential[1].append(j+1)
        elif j == gridMax:
            neighbourPotential[1].append(j-1)
            neighbourPotential[1].append(j)
        else:
            neighbourPotential[1].append(j-1)
            neighbourPotential[1].append(j)
            neighbourPotential[1].append(j+1)

        neighbours = []
        for row in neighbourPotential[0]:
            for col in neighbourPotential[1]:
                neighbours.append((row, col))
        neighbours.remove((i,j))
        return neighbours

class Main():
    def __init__(self, size):
        self.gridSize = size
        self.grid = []

    def createGrid(self):
        #creates the grid in (row,column) fashion
        for i in range(self.gridSize):
            self.grid.append([])
            for j in range(self.gridSize):
                self.grid[i].append(Cell((i,j), self.gridSize))

    def update(self):
        #Takes a turn in the grid
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                self.grid[i][j].calcNextGen(self.grid)

        for i in range(self.gridSize):
            for j in range(self.gridSize):
                self.grid[i][j].createNextGen()

    def printGrid(self, attr):
        printArray = []
        for j in range(self.gridSize):
            printArray.append("-")
        for i in range(2*self.gridSize+1):
            if i%2==0:
                print(" ".join(printArray))
            else:
                cellArray = []
                for j in range(self.gridSize):
                    if attr == "colour":
                        cellArray.append(self.grid[i//2][j].printColour)
                    elif attr == "num":
                        cellArray.append(str(self.grid[i//2][j].neighboursCalc))
                print("|".join(cellArray))

    def fillCell(self, pos, colour):
        cell = self.grid[pos[0]][pos[1]]
        cell.colour = colour
        cell.filled = True
        cell.printColour = colour[0]

    def isAlive(self):
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if self.grid[i][j].colour != "BLANK":
                    return True
        return False

main = Main(10)
main.createGrid()
def fillRandom25():
    for i in range(25):
        row = r.randrange(10)
        col = r.randrange(10)
        colour = r.randrange(2)
        if colour == 0:
            colour = "BLUE"
        else:
            colour = "RED"
        main.fillCell((row,col),colour)
def test():
    fillRandom25()
    gens = 1
    while main.isAlive():
        #main.printGrid("num")
        main.printGrid("colour")
        print()
        gens += 1
        main.update()
    print(gens)
    return gens
maxGen = 0
for i in range(100):
    numGen = test()
    if numGen > maxGen:
        maxGen = numGen
print(maxGen)
