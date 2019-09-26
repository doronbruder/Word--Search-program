from wordsearch import *
import sys


def set_test_parameters():
    """set the parameters for runing the test fucntion"""
    global DIRECTIONS_DIC, POSSIBLE_DIRECTIONS, COL_LEN, ROW_LEN
    NUM_OF_VALUES = 5
    DIRECTIONS_DIC = {'u': (-1, 0), 'd': (1, 0), 'r': (0, 1), 'l': (0, -1), 'w': (-1, 1), 'x': (-1, -1), 'y': (1, 1),
                      'z': (1, -1)}
    POSSIBLE_DIRECTIONS = ['u', 'd', 'r', 'l', 'w', 'x', 'y', 'z']
    MATRIX_FILE = sys.argv[2]
    WORDS_FILE = sys.argv[1]
    DIRECTIONS = sys.argv[4]
    words = read_wordlist_file("word_list.txt")
    matrix = read_matrix_file("mat.txt")
    COL_LEN = len(matrix)
    ROW_LEN = len(matrix[0])
    foundwords_dic = {}


set_test_parameters()


def update_coordinates_test():
    """This function checks if the update coordinates function works """
    flg = False
    # checks all the ordinary cases where the direction is valid - make sure the coordinates updated properly
    for direction in POSSIBLE_DIRECTIONS:
        for j in range(COL_LEN):

            for i in range(ROW_LEN):

                x = i

                y = j

                expected_x = x + DIRECTIONS_DIC[direction][1]
                expected_y = y + DIRECTIONS_DIC[direction][0]

                if (expected_x, expected_y) == update_coordinates(direction, x, y):
                    flg = True

    x, y = update_coordinates('g', 0, 0)
    # checks an extreme case that the direction is invalid and makes sure it doesnt change the coordination in that case
    if (x, y) != (0, 0):
        flg = False

    return flg


if __name__ == "__main__":
    print(update_coordinates_test())
