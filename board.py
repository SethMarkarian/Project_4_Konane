class Board:
    def __init__(self):
        #Columns
        self.columnIndex = [i for i in range(1, 9)] 
        
        #Rows
        self.rowIndex = []
        for i in range(8):
            self.rowIndex.append([])

        #Fill Board
        for i in range(8):
            for j in range(8):
                if i % 2 == 0:
                    if j % 2 == 0:
                        self.rowIndex[i].append("B")
                    else:
                        self.rowIndex[i].append("W")
                else:
                    if j % 2 == 0:
                        self.rowIndex[i].append("W")
                    else:
                        self.rowIndex[i].append("B")
                


    def updateBoard(self, prev_pos, curr_pos):
        moved = self.rowIndex[prev_pos[0]][prev_pos[1]]
        self.rowIndex[prev_pos[0]][prev_pos[1]] = "."

        #Removes pieces from range of x and y
        remove_x = sorted([from_pos[0], to_pos[0]+1])
        remove_y = sorted([from_pos[1], to_pos[1]+1])
        for i in range(remove_x):
            for j in range(remove_y):
                #Replaces piece with empty
                self.rowIndex[i][j] = "."
        #Places moved piece in updated spot
        self.rowIndex[prev_pos[0]][curr_pos[1]] = moved        

    def removePiece(self, curr_pos):
        self.rowIndex[curr_pos[0]][curr_pos[1]] = "."

    def strBoard(self):
        #Prints board
        output = "  "
        for i in self.columnIndex:
            output += str(i) + " "
        output += "\n"
        rowNum = 1
        for row in self.rowIndex:
            output += str(rowNum) + " "
            for piece in row:
                output += piece + " "
            output += "\n"
            rowNum += 1
        return output

if __name__ == '__main__':
    print(Board().strBoard())