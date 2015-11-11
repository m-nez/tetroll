#!/usr/bin/python

SIGNS = {
    "a": [
    [0,1,1,0],
    [1,0,0,1],
    [1,1,1,1],
    [1,0,0,1],
    [1,0,0,1], ],
    "b": [
    [1,1,1,0],
    [1,0,0,1],
    [1,1,1,0],
    [1,0,0,1],
    [1,1,1,0], ],
    "c": [
    [0,1,1,0],
    [1,0,0,1],
    [1,0,0,0],
    [1,0,0,1],
    [0,1,1,0], ],
    "d": [
    [1,1,1,0],
    [1,0,0,1],
    [1,0,0,1],
    [1,0,0,1],
    [1,1,1,0], ],
    "e": [
    [1,1,1,1],
    [1,0,0,0],
    [1,1,1,1],
    [1,0,0,0],
    [1,1,1,1], ],
    "f": [
    [1,1,1,1],
    [1,0,0,0],
    [1,1,1,1],
    [1,0,0,0],
    [1,0,0,0], ],
    "g": [
    [0,1,1,1],
    [1,0,0,0],
    [1,0,1,1],
    [1,0,0,1],
    [0,1,1,0], ],
    "h": [
    [1,0,0,1],
    [1,0,0,1],
    [1,1,1,1],
    [1,0,0,1],
    [1,0,0,1], ],
    "i": [
    [1,1,1,0],
    [0,1,0,0],
    [0,1,0,0],
    [0,1,0,0],
    [1,1,1,0], ],
    "j": [
    [1,1,1,1],
    [0,0,0,1],
    [0,0,0,1],
    [1,0,0,1],
    [0,1,1,0], ],
    "k": [
    [1,0,0,1],
    [1,0,1,0],
    [1,1,0,0],
    [1,0,1,0],
    [1,0,0,1], ],
    "l": [
    [1,0,0,0],
    [1,0,0,0],
    [1,0,0,0],
    [1,0,0,0],
    [1,1,1,1], ],
    "m": [
    [1,0,0,1],
    [1,1,1,1],
    [1,0,0,1],
    [1,0,0,1],
    [1,0,0,1], ],
    "n": [
    [1,0,0,1],
    [1,1,0,1],
    [1,1,0,1],
    [1,0,1,1],
    [1,0,0,1], ],
    "o": [
    [0,1,1,0],
    [1,0,0,1],
    [1,0,0,1],
    [1,0,0,1],
    [0,1,1,0], ],
    "p": [
    [1,1,1,0],
    [1,0,0,1],
    [1,1,1,0],
    [1,0,0,0],
    [1,0,0,0], ],
    "r": [
    [1,1,1,0],
    [1,0,0,1],
    [1,1,1,0],
    [1,0,0,1],
    [1,0,0,1], ],
    "s": [
    [0,1,1,1],
    [1,0,0,0],
    [1,1,1,1],
    [0,0,0,1],
    [1,1,1,0], ],
    "t": [
    [1,1,1,1],
    [0,1,0,0],
    [0,1,0,0],
    [0,1,0,0],
    [0,1,0,0], ],
    "u": [
    [1,0,0,1],
    [1,0,0,1],
    [1,0,0,1],
    [1,0,0,1],
    [0,1,1,0], ],
    "v": [
    [1,0,0,1],
    [1,0,0,1],
    [1,0,1,0],
    [1,0,1,0],
    [0,1,0,0], ],
    "w": [
    [1,0,0,1],
    [1,0,0,1],
    [1,0,0,1],
    [1,1,1,1],
    [1,0,0,1], ],
    "x": [
    [1,0,0,1],
    [0,1,0,1],
    [0,0,1,0],
    [0,1,0,1],
    [1,0,0,1], ],
    "y": [
    [1,0,0,1],
    [1,0,0,1],
    [0,1,1,0],
    [0,1,0,0],
    [0,1,0,0], ],
    "z": [
    [1,1,1,1],
    [0,0,1,0],
    [0,1,0,0],
    [1,0,0,0],
    [1,1,1,1], ],
    "0": [
    [0,1,1,0],
    [1,0,0,1],
    [1,0,0,1],
    [1,0,0,1],
    [0,1,1,0],
    ],
    "1": [
    [0,0,1,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,0],
    [0,0,1,0],
    ],
    "2": [
    [0,1,1,0],
    [1,0,0,1],
    [0,0,1,0],
    [0,1,0,0],
    [1,1,1,1],
    ],
    "3": [
    [1,1,1,0],
    [0,0,0,1],
    [1,1,1,0],
    [0,0,0,1],
    [1,1,1,0],
    ],
    "4": [
    [1,0,1,0],
    [1,0,1,0],
    [1,1,1,1],
    [0,0,1,0],
    [0,0,1,0],
    ],
    "5": [
    [1,1,1,1],
    [1,0,0,0],
    [1,1,1,0],
    [0,0,0,1],
    [1,1,1,0],
    ],
    "6": [
    [0,0,1,0],
    [0,1,0,0],
    [1,1,1,0],
    [1,0,0,1],
    [0,1,1,0],
    ],
    "7": [
    [1,1,1,1],
    [0,0,0,1],
    [0,0,1,0],
    [0,1,0,0],
    [1,0,0,0],
    ],
    "8": [
    [0,1,1,0],
    [1,0,0,1],
    [0,1,1,0],
    [1,0,0,1],
    [0,1,1,0],
    ],
    "9": [
    [0,1,1,0],
    [1,0,0,1],
    [1,1,1,1],
    [0,0,0,1],
    [1,1,1,0],
    ],
    " ": [
    [],
    [],
    [],
    [],
    [],
    ]
    }

def str_to_matrix(string):
    """
    Convert a string of signs([a-z, 0-9]) to a matrix
    """
    mat = [[0],[0],[0],[0],[0]]
    line_num = 0
    for i in string:
        if i == "\n":
            mat.extend([[0],[0],[0],[0],[0],[0]])
            line_num += 1
        else:
            for n, j in enumerate(SIGNS[i]):
                mat[line_num*6 + n] += j + [0]

    return mat
