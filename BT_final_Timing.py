import time
tStart = time.time()

for i in range(10):
    #Utility functions
    def dec2bin(dec, bitLength):
        temp = [0]*bitLength
        k = 0
        while dec > 0:
            temp[k] = dec % 2
            dec = dec // 2
            k += 1
        #Reverse the list
        ans = []
        for i in range(-1, -len(temp)-1, -1):
            ans.append(temp[i])
        return ans


    def subset(n):
        ans = []
        for i in range(2**n):
            ans.append(dec2bin(i, n))
        return ans


    def list2board(L):
        ans = []
        n = int(len(L) ** 0.5)  # Square Root of the len(L)
        for i in range(n):
            temp = []
            for j in range(n):
                temp.append(L[i*n + j])
            ans.append(temp)
        return ans


    def printBoard(board, rowSum, colSum):
        l1 = "   |"
        for i in range(len(board)):
            l1 = l1 + " " + str(i+1) + " |"
        print(l1)
        l = "---|"
        for i in range(len(board)):
            l += "---|"
        l += "---"
        for i in range(len(board)):
            print(l)
            temp = " " + str(i+1) + " |"
            for j in range(len(board)):
                temp = temp + " " + str(board[i][j]) + " |"
            temp  = temp + " " + str(rowSum[i])
            print(temp)
        print(l)
        lEnd = "   |"
        for i in range(len(board)):
            if colSum[i] < 10: #in order to align the layout
                lEnd = lEnd + " " + str(colSum[i]) + " |"
            else:
                lEnd = lEnd + " " + str(colSum[i]) + "|"
        print(lEnd)


    def isSolution(board, rowSum, colSum):
        for i in range(len(rowSum)):
            sumRow = 0
            sumCol = 0
            for j in range(len(rowSum)):
                sumRow += board[i][j] * (j + 1)
                sumCol += board[j][i] * (j + 1)
            if sumRow != rowSum[i] or sumCol != colSum[i]:
                return False
        #if pass both check, return True
        return True


    def getPossible(partial, boardSize, rowSum, colSum): #determine whether 0 or 1
        #check if reach the end
        if len(partial) == boardSize ** 2:
            return []
        # get next position's index
        l = len(partial) + 1
        x = l // boardSize
        y = l % boardSize #Remainder
        #get row
        if y == 0:
            row = x - 1 #here index represented as 2d list (board)
        else:
            row = x
        #get col
        col = l - boardSize*row - 1
        #check the row&col sum to determine if it's 0 or 1
        rS = 0 #row sum
        cS= 0 #col sum
        counter = 1
        for i in range(row*boardSize, len(partial)):
            rS += partial[i] * counter
            counter += 1
        counter = 1 #reset the counter
        for i in range(row):
            cS += partial[col + boardSize*i] * counter
            counter += 1
        #determine the final result
        #check if the current row and col can reach the goal (can finally equal to the sum)
        rowDiff = rowSum[row] - rS
        colDiff = colSum[col] - cS
        isValidRow = False
        isValidCol = False
        possRow = subset(boardSize - col)
        possCol = subset(boardSize - row)
        #check row
        for i in range(len(possRow)):
            counter = col + 1
            sum = 0
            temp = possRow[i]
            for j in range(len(temp)):
                sum += temp[j] * counter
                counter += 1
            if sum == rowDiff:
                isValidRow = True
                break
        #check col
        for i in range(len(possCol)):
            counter = row + 1
            sum = 0
            temp = possCol[i]
            for j in range(len(temp)):
                sum += temp[j] * counter
                counter += 1
            if sum == colDiff:
                isValidCol = True
                break
        #now return the possible value
        if isValidRow == True and isValidCol == True:
            if rowDiff < 0 or colDiff < 0:
                return []
            if rowDiff == 0 or colDiff == 0:
                return [0]
            if rowDiff == (col + 1) or colDiff == (row + 1):
                return [1]
            else:
                return [0, 1]
        else:
            return []


    def processSolution(partial, boardSize, rowSum, colSum):
        if len(partial) == boardSize ** 2:
            ans = list2board(partial)
            # because once the length of partial matches board, the last element in
            # partial will be 0
            # so now check the ans
            if isSolution(ans, rowSum, colSum) == True: # if found the (first) ans return ans, any other case return False
                # printBoard(ans, rowSum, colSum)
                return ans
            else:
                return False
        else:
            return False


    def kakurasu(partial, boardSize, rowSum, colSum):
        possibleItems = getPossible(partial, boardSize, rowSum, colSum)
        # check if partial is a solution
        if possibleItems == []:
            b = processSolution(partial, boardSize, rowSum, colSum)
            return b # return the value got in processSolution (can be either the ans or False)
        else:
            for item in possibleItems:
                partial.append(item)
                ans = kakurasu(partial, boardSize, rowSum, colSum) # check if the got the ans (returned value != False)
                if ans != False:
                    return ans # if got the ans just return and will not pop again!
                partial.pop()
        return False


    def backtrack(rowSum, colSum):
        n = len(rowSum) #Board Size
        return kakurasu([], n, rowSum, colSum)


    rowSum = [55,55,55,55,55,55,55,55,55,55]
    colSum = [55,55,55,55,55,55,55,55,55,55]
    ans = backtrack(rowSum, colSum)
    printBoard(ans,rowSum, colSum)

print("Time:", time.time() - tStart)