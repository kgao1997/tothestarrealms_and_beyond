import math

class GameTree:
    def __init__(self, v, c):
        self.value = v   # all values in a tree should have same type (i.e. game state)
        self.children = c   # list of child gametrees

    def print_tree(self):
        print (self.value)
        for c in self.children:
            c.print_tree()

    def eval(self, value):
        return value   # later: convert state to int

    def minimax(self, depth):
        if (depth == 0 or not self.children):
            return self.eval(self.value)
        else:
            maxval = -math.inf
            for c in self.children:
                tempval = c.maximin (depth-1)
                if (tempval > maxval):
                    maxval = tempval
            return maxval

    def maximin(self, depth):
        if (depth == 0 or not self.children):
            return self.eval(self.value)
        else:
            minval = math.inf
            for c in self.children:
                tempval = c.minimax (depth-1)
                if (tempval < minval):
                    minval = tempval
            return minval

    def minimaxAB(self, depth, a, b):
        #print ("visiting "+str(self.value))
        if (depth == 0 or not self.children):
            return self.eval(self.value)
        else:
            maxval = -math.inf
            for c in self.children:
                tempval = c.maximinAB (depth-1, max(a, maxval), b)
                if (tempval >= b):
                    return maxval
                if (tempval > maxval):
                    maxval = tempval
            return maxval

    def maximinAB(self, depth, a, b):
        #print ("visiting "+str(self.value))
        if (depth == 0 or not self.children):
            return self.eval(self.value)
        else:
            minval = math.inf
            for c in self.children:
                tempval = c.minimaxAB (depth-1, a, min(b, minval))
                if (tempval <= a):
                    return minval
                if (tempval < minval):
                    minval = tempval
            return minval

'''
tree = GameTree(7, [GameTree(5, [GameTree(1, []), GameTree(2, [])]), GameTree(6, [GameTree(3, []), GameTree(4, [])])])

#tree.print_tree()
print (tree.minimax(0))
print (tree.minimax(1))
print (tree.minimax(20))

print (tree.maximin(0))
print (tree.maximin(1))
print (tree.maximin(20))

print (tree.minimaxAB(0, -10000, 10000))
print (tree.minimaxAB(1, -10000, 10000))
print (tree.minimaxAB(20, -10000, 10000))

print (tree.maximinAB(0, -10000, 10000))
print (tree.maximinAB(1, -10000, 10000))
print (tree.maximinAB(20, -10000, 10000))
'''
