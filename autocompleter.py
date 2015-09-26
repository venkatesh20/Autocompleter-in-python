#!/usr/bin/python

# This code implements an auto-completer using the ternary tree data structure.
# For more information, please check out: http://en.wikipedia.org/wiki/Ternary_search_tree

import sys
import os.path
import time
sys.setrecursionlimit(10000)

#global variable that keeps track of how many files have been written
total=0
flist=[]
# The Node class implements the standard node in a ternary tree.
# A ternary tree is similar to a binary tree, except each node has 3 children instead of two.
# The left child is alphabetically lower in order than the center and right children.
# Each Node consist of the center, left and right pointers.
# self.ch => contains the character.
# self.flag => Flag to Check whether the node is an end character of a valid string.
# self.left, self.right => Links to the next nodes.
# self.center => Link to the next valid character.
class Node:
# The init function acts like the default constructor for a Node object.
# The self argument stands for the object which calls the function.
# The ch argument represents the character to be added.
# The flag argument checks if the string is properly terminated and is a valid candidate for suggestion.
    def __init__(self, ch, flag):

        self.ch = ch
        self.flag = flag
        self.left = 0
        self.right = 0
        self.center = 0

# The Add function adds a string to the ternary tree.
# The self argument stands for the object which calls the function.
# The node argument represents the node in the tree to which the addition is performed (left or right)
# The string argument stands for the string which will be added.
    def Add(self, string, node):
       
        key = string[0]

        if node == 0:
            node = Node(key, 0)

        if key < node.ch:
            node.left = node.Add(string, node.left)
        elif key > node.ch:
            node.right = node.Add(string, node.right)
        else:
            if len(string) == 1:
                node.flag = 1
            else:
                node.center = node.Add(string[1:], node.center)

        return node

# The dfs function performs a depth first search on the ternary tree.
# The self argument stands for the object which calls the function.
# The match argument stands for the string to be matched.

    def dfs(self, match):

        if self.flag == 1:
            print match
            # print "Match : ", match

        if self.center == 0 and self.left == 0 and self.right == 0:
            return

        if self.center != 0:
            self.center.dfs(match + self.center.ch)

        if self.right != 0:
            self.right.dfs(match[:-1] + self.right.ch)

        if self.left != 0:
            self.left.dfs(match[:-1]+self.left.ch)


# The search function searches the ternary tree using the dfs helper function.
# The self argument stands for the object which calls the function.
# The match argument stands for the string to be matched.
# The string argument stands for the string which will be added.

    def search(self, string, match):
       
        if len(string) > 0:
            key = string[0]

            if key < self.ch:
                if self.left == 0:
                    print "No Match Found"
                    return
                self.left.search(string, match)

            elif key > self.ch:
                if self.right == 0:
                    print("No Match Found")
                    return
                self.right.search(string, match)

            else:
                if len(string) == 1:
                    if self.center != 0:
                        self.center.dfs(match + self.ch + self.center.ch)
                    return 1
                self.center.search(string[1:], match + key)

        else:
            print("Invalid String")
            return


# The fileparse function parses each file and builds the ternary tree by using the Add helper function for each Node object.
# The filename argument stands for the file to be parsed.
# The node argument stands for the node which will be created.

def fileparse(filename, node):
   
    fd = open(filename)
    line = fd.readline().strip('\r\n')

    while line != '':
        node.Add(line, node)
        line = fd.readline().strip('\r\n')
    fd.close()

# The split_data function splits the large file of all phrases into smaller chunks of 1000 lines each and creates new files.
# The filename argument stands for the file to be parsed.

def split_data(filename):

    global total
    fid = 1
    with open(filename, 'r') as infile:
        f = open('%s-%s.txt' % (filename.strip('.txt'), fid), 'wb')
        for line, doc in enumerate(infile):
            f.write(doc)
            if not line % 1000 and line > 1:
                f.close()
                fid += 1
                f = open('%s-%s.txt' % (filename.strip('.txt'), fid),
                         'wb')
        f.close()
    total=fid

# The read_data function reads all of the files created by split_data above, one at a time, and builds the ternary tree.
# The node argument stands for the root of the ternary tree.
# The filename argument stands for the file containing the list of reference phrases to be parsed.

def read_data(node, filename):
   
    global flist
    fid = 1
 
    with open(filename, 'r') as infile:
      while fid <=total: 
        f = '%s-%s.txt' % (filename.strip('.txt'), fid)
        print "Reading %s" % f
        flist.append(f)
        fileparse(f,node)
        fid +=1

def cleanup():
     for i in flist:
       print i
       if os.path.isfile(i):
          os.remove(i)
       else:    
        print("Error: %s file not found\n" % i)
 

if __name__ == '__main__':
  
    root = Node('', 0)
    print "Welcome to the autocomplete program.\n[INFO]: Loading database file containing list of phrases into memory ...\n"
    split_data(sys.argv[1])
    read_data(root, sys.argv[1])
    print "[INFO]: Finished loading database file.\n"
  
    inp = 'empty'
    while inp !='':
        if inp !='quit':
             inp = raw_input("Please type the prefix of a word:\n")
             print "\nSuggestions:"
             root.search(inp,'')
        else:
             print "Cleaning up extra files ...\n"
             cleanup()
             print "Cleanup done. Exiting the program\n"
             sys.exit(0)