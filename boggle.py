#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
__version__ = "$Revision: 0.2$"
__author__ = "Nicolas Seriot"
__date__ = "2005-09-25"

import random
import time
import sys
from sets import Set

class Boggle:
    """
    Boggle game
    """
        
    letters = []
    letters += ['a'] * 8
    letters += ['b'] * 3
    letters += ['c'] * 3
    letters += ['d'] * 4
    letters += ['e'] * 10
    letters += ['f'] * 2
    letters += ['g'] * 3
    letters += ['h'] * 3
    letters += ['i'] * 7
    letters += ['j'] * 1
    letters += ['k'] * 2
    letters += ['l'] * 5
    letters += ['m'] * 3
    letters += ['n'] * 5
    letters += ['o'] * 6
    letters += ['p'] * 3
    letters += ['q'] * 1
    letters += ['r'] * 4
    letters += ['s'] * 5
    letters += ['t'] * 5
    letters += ['u'] * 4
    letters += ['v'] * 2
    letters += ['w'] * 2
    letters += ['x'] * 1
    letters += ['y'] * 3
    letters += ['z'] * 1
    
    def __init__(self, dict_path):     
            
        self.dico = Set()
        self.radicals = Set()
        
        print "building dictionary"
        dict_file = open(dict_path)
        
        for w in dict_file:
            length = len(w)
            w = w.lower().strip()
            self.dico.add(w)
            for i in range(length, 1, -1):
                self.radicals.add(w[:i-1])

        dict_file.close()
        print "ready!\n"
    
    def new_game(self, (h, w) = (4, 4), min_len = 3):
        self.height = h
        self.width = w
        self.min_len = min_len
        
        line = []
        line.append([''] * self.width)
        self.board = [line] * self.height
        
        self.init_hits()
        
        self.new_board()
    
    def new_game_with_matrix(self, matrix):
        size = 0
        for i in range(3, 10):
            if len(matrix) == i*i:
                size = i
                break
        if not size:
            raise Exception

        self.height = i
        self.width = i
        self.min_len = i-1
        self.init_hits()
                 
        board = []
        for w in range(0, len(matrix), self.width):
            board.append(matrix[w:w+self.width])
        self.board = board
                
    def init_hits(self):
        hits = []
        
        line = []
        for w in range(self.width):
            line.append(False)
        for h in range(self.height):
            hits.append(list(line))
        
        return hits
         
    def new_board(self):
        for h in range(self.height):
            line = []
            for w in range(self.width):
                line.append(random.choice(self.letters))
            self.board[h] = line
    
    def __str__(self):
        b = []
    
        for h in range(self.height):
            b.append(" ".join(self.board[h]))
        
        return reduce(lambda x, y: x + "\n" + y, b).lower().upper()
    
    def one_line(self):
        s = ""
        for h in range(self.height):
            for w in range(self.width):
                s += self.board[h][w]
        return s.lower()
    
    def next_letters(self, height, width, hit):
        h_range = range(height-1,height+2)
        w_range = range(width-1,width+2)
        
        h_range = filter(lambda x : x >= 0 and x < self.height, h_range)
        w_range = filter(lambda x : x >= 0 and x < self.width, w_range)        

        l = []
        for h in h_range:
            for w in w_range:
                if not hit[h][w]:
                    l.append((h, w, self.board[h][w]))
        return l
    
    def add_next(self, word, height, width, hit):
        letters = self.next_letters(height, width, hit)

        for (h, w, l) in letters:
            new_word = word + l
                        
            # is it a word ?
            if len(new_word) >= self.min_len:
                if new_word in self.dico:
                    hit[h][w] = True
                    self.sol.add(new_word)
            
            # is it a radical ?
            if new_word in self.radicals:
                hit[h][w] = True
                self.add_next(new_word, h, w, hit)
            
            hit[h][w] = False
    
    def solve(self):
        
        t0 = time.clock()
        
        self.sol = Set()
    
        for h in range(self.height):
            for w in range(self.width):
                word = self.board[h][w]
                                
                hits = self.init_hits()
                
                hits[h][w] = True
                
                self.add_next(word, h, w, hits)
                
        l = list(self.sol)
        l.sort()
        
        self.__solving_time = time.clock() - t0
        
        return l
    
    def solving_time(self):
        return self.__solving_time
    
    def score(self, words):
        d = {}
        d[2] = 0
        d[3] = 1
        d[4] = 1
        d[5] = 2
        d[6] = 3
        d[7] = 5
        d[8] = 11
        
        words = filter(lambda x:x in self.dico, words)
        
        score = 0
        
        for w in words:
            l = len(w)
            if l > 8:
                l = 8
            if l < 2:
                l = 2
                
            score += d[l]
            
        return score
    
    def __del__(self):
        pass
    
if __name__ == "__main__":

    MENU = """       n - new rules
       m - boogle with matrix
       r - random boogle
       s - solve it
       q - quit"""

    wanted = ['size', 'dict', 'min']
    options = {}
    options['size'] = '4x4'
    options['dict'] = 'ODS2.txt'
    options['min'] = '3'
    
    args = sys.argv[1:]
    for a in args:
        for w in wanted:
            if a.startswith(w + '='):
                options[w] = a[len(w) + 1:]
    
    print "boggle v0.2"
    
    try:
        print "   size = " + options['size']
        print "    min = " + options['min']
        print "   dict = " + options['dict']
        
        dico = options['dict']
    
        (h, w) = options['size'].split('x')
        (h, w) = (int(h), int(w))
    
        min = int(options['min'])
        
        if (h not in range(3, 51)) or (w not in range(3, 51)):
            raise ValueError
        if min not in range(3, h*w+1):
            raise ValueError
        
    except:
        print "Error!"
        print "USAGE : " + sys.argv[0] + " size=4x4 min=3 dict=french.txt"
        sys.exit(0)
        
    b = Boggle(dico)

    k = ''
    
    b.new_game((h, w), min)
    boggle = True
    print "\n", b
    
    while k != 'q':
    
        print MENU
        k = raw_input('> ')
        if k == 'r':
            b.new_board()
            boggle = True
            print "\n", b
            #print b.one_line()
        elif k == 'm':
            try:
                matrix = raw_input("enter matrix > ").strip()
                b.new_game_with_matrix(matrix)
                boggle = True
                print "\n", b
            except:
                print "Error - bad matrix"
            #print b.one_line()
        elif k == 'n':
            try:
                size = raw_input("enter size > ").strip()
                min_len = raw_input("enter min length > ").strip()
                size = size.split('x')
                size = (int(size[0]), int(size[1]))
                b.new_game(size, int(min_len))
                print b
                boggle = True
            except:
                print "Error - bad values"
        elif boggle and k == 's':
            s = b.solve()
            s.sort(lambda x, y: len(y) - len(x))
            try:
                l = 0
                for word in s:
                    if len(word) != l:
                        l = len(word)
                        print "\n-- %s --" % l
                    print word
            except:
                print "no words found"
                
            print ""
            print "%d words" % len(s)
            print "%d points" % b.score(s)
            print "solved in %f s." % b.solving_time()
            boggle = False
