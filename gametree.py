import math

class GameTree:
    def __init__(self, l, v, f, c):
        self.label = l   # label of the action leading to this node
        self.value = v   # all values in a tree should have same type (i.e. game state)
        self.children = c   # list of child gametrees
        self.eval_node = f   # evaluation function (value --> number)

    def print_tree(self):
        print (self.value)
        for c in self.children:
            c.print_tree()
    
    def minimax(self, depth):
        if (depth == 0 or not self.children):
            return self.label, self.eval_node(self.value)
        else:
            maxval = -math.inf
            besta = ''
            for c in self.children:
                _, tempval = c.maximin (depth-1)
                if (tempval > maxval):
                    maxval = tempval
                    besta = c.label
            return besta, maxval

    def maximin(self, depth):
        if (depth == 0 or not self.children):
            return self.label, self.eval_node(self.value)
        else:
            minval = math.inf
            besta = ''
            for c in self.children:
                _, tempval = c.minimax (depth-1)
                if (tempval < minval):
                    minval = tempval
                    besta = c.label
            return besta, minval

    def minimaxAB(self, depth, a, b):
        #print ("visiting "+str(self.value))
        if (depth == 0 or not self.children):
            return (self.label, self.eval_node(self.value))
        else:
            maxval = -math.inf
            besta = ''
            for c in self.children:
                (_, tempval) = c.maximinAB (depth-1, max(a, maxval), b)
                if (tempval >= b):
                    return (besta, maxval)
                if (tempval > maxval):
                    maxval = tempval
                    besta = c.label
            return (besta, maxval)

    def maximinAB(self, depth, a, b):
        #print ("visiting "+str(self.value))
        if (depth == 0 or not self.children):
            return (self.label, self.eval_node(self.value))
        else:
            minval = math.inf
            besta = ''
            for c in self.children:
                (_, tempval) = c.minimaxAB (depth-1, a, min(b, minval))
                if (tempval <= a):
                    return (besta, minval)
                if (tempval < minval):
                    minval = tempval
                    besta = c.label
            return (besta, minval)

def eval1(value):
    return value

def eval2(value):
    return 2*value


tree = GameTree('root', 7, eval2, [GameTree('A', 5, eval2, [GameTree('C', 1, eval2, []), GameTree('D', 2, eval2, [])]), GameTree('B', 6, eval2, [GameTree('E', 3, eval2, []), GameTree('F', 4, eval2, [])])])
'''
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
