import os.path
import sys

#import csv

# Here I define the variables to be more  readable

ARGS = sys.argv

INVALID_LENGTH_MSG = "Invalid input - more\less args than necessary"

NO_MATRIX_MSG = "Matrix file not found"

NO_WORDS_MSG = "Words file not found"

INVALID_DIRECTIONS_MSG = "Invalid input- invalid direcrtions"

NUM_OF_VALUES = 5

# A dictionary that is linking every direction to the change in the coordinates (x,y) in cartesian axis
# When assume one move in each direction
DIRECTIONS_DIC = {'u': (-1, 0), 'd': (1, 0), 'r': (0, 1), 'l': (0, -1), 'w': (-1, 1), 'x': (-1, -1), 'y': (1, 1),
                  'z': (1, -1)}

# All the possible directions
POSSIBLE_DIRECTIONS = ['u', 'd', 'r', 'l', 'w', 'x', 'y', 'z']


def check_input_args(args):
    """This function checks if the parametrs to the program  are valid"""

    # If either the matrix file or the words file not exist it returns an  appropriate message
    if not os.path.exists(sys.argv[1]) and not os.path.exists(sys.argv[2]):
        return NO_WORDS_MSG

    # If the there are too many or not enough  parameters  it returns an appropriate message
    elif len(args) != NUM_OF_VALUES:
        return INVALID_LENGTH_MSG

    # If the matrix file  not exist it returns appropriate message
    elif not os.path.exists(sys.argv[2]):
        return NO_MATRIX_MSG

    else:
        # If the directions contain an invalid direction it returns an appropriate message
        for char in sys.argv[4]:
            if char not in POSSIBLE_DIRECTIONS:
                return INVALID_DIRECTIONS_MSG

    return None




def read_matrix_file(filename):
    """this function receives the matrix file name, open him
    and return him as a list of strings"""
    with open(filename, 'r') as file:
        lines_list = [line[:-1] for line in file.readlines()]
        matrix = []
        for i in range(len(lines_list)):
            line = []
            for j in range(len(lines_list[i])):
                if lines_list[i][j] != ',':
                    line.append(lines_list[i][j])
            matrix.append(line)
        return matrix



def read_wordlist_file(filename):
    '''function reads the file containing the words for the game and returns
     a suited list containing the words'''
    f = open(filename)
    tmp_list = f.readlines()[:]
    f.close()
    for i in range(len(tmp_list)):
        tmp_list[i] = tmp_list[i].strip('\n')
    return tmp_list




def set_parametrs():
    """This function sets the parametrs to the finding function"""

    MATRIX = read_matrix_file(sys.argv[2])

    WORDS = read_wordlist_file(sys.argv[1])

    foundwords_dic = {}  # Define a dictionary that will link words that found in the matrix to their count

    COL_LEN = len(MATRIX)  # Define the columns length

    ROW_LEN = len(MATRIX[0])  # Define the rows length

    return COL_LEN, MATRIX, ROW_LEN, WORDS, foundwords_dic


def dic_to_list(foundwords_dic):
    """This function convert a dictionary to a list of pairs-key,value"""

    foundwords_lst = []
    for item in foundwords_dic.items():
        foundwords_lst.append(item)
    return foundwords_lst


def update_words_count(current_word, foundwords_dic):
    """This function updates the count of a found word in the found words dictionary"""
    if current_word in foundwords_dic:
        foundwords_dic[current_word] += 1

    else:
        foundwords_dic[current_word] = 1

    return foundwords_dic


def update_coordinates(direction, x, y):
    """This function changes the coordinates according to the chosen direction"""
    if direction not in POSSIBLE_DIRECTIONS:
        return x, y
    else:
        x += DIRECTIONS_DIC[direction][1]
        y += DIRECTIONS_DIC[direction][0]
        return x, y


def search_from_somepoint(COL_LEN, MATRIX, ROW_LEN, WORDS, current_word, direction, foundwords_dic, x, y):
    """This function search from a specific point in the matrix each time

    :param COL_LEN: length of the matrix column
    :param MATRIX: the matrix repesented as 2d list
    :param ROW_LEN:  length of the matrix row
    :param WORDS:  words represented as a list
    :param current_word: current part of matrix that we test
    :param direction: direction that was chosen to search
    :param foundwords_dic: a dic that links found words in matrix to their count
    :param x: represents "x coordinate" - left and right directions in the matrix
    :param y: represrnts "y coordinate"- up and down directions in the matrix
    :return: updated coordinates according the chosen direction , and updated found words dic if a new word found
    """

    while 0 <= x < ROW_LEN and 0 <= y < COL_LEN:

        current_word = current_word + MATRIX[y][x]

        if current_word in WORDS:
            foundwords_dic = update_words_count(current_word, foundwords_dic)

        x, y = update_coordinates(direction, x, y)

    return x, y, foundwords_dic


def search_currentdirection(COL_LEN, MATRIX, ROW_LEN, WORDS, direction, foundwords_dic):
    """This function starts searching with  a specific direction each time

    :param COL_LEN: length of the matrix column
    :param MATRIX: the matrix repesents as 2d list
    :param ROW_LEN:  length of the matrix row
    :param WORDS:  words represents as a list
    :param direction: some direction that chosen
    :param foundwords_dic: a dic that links found words in matrix to their count
    """
    for j in range(COL_LEN):

        for i in range(ROW_LEN):
            current_word = ""

            x = i

            y = j

            x, y, foundwords_dic = search_from_somepoint(COL_LEN, MATRIX, ROW_LEN, WORDS, current_word, direction,
                                                         foundwords_dic, x, y)


def no_dublicate_directions(directions):
    """deletes duplicates from the directions"""
    directions = set(directions)
    directions = "".join(directions)
    return directions


def find_words_in_matrix(word_list, matrix, directions):
    """This fucntion finds words from the list that appears in the matrix in chosen directions and count appearances
    :param word_list: list of words to check if appears in the matrix in chosen directions
    :param matrix: matrix of letters
    :param directions: to find  words that appears in the matrix in these directions
    :return: list of pairs the shows the words found in the matrix with their number of appearances
   """

    directions = no_dublicate_directions(directions)

    COL_LEN, MATRIX, ROW_LEN, WORDS, foundwords_dic = set_parametrs()

    if MATRIX == [] or WORDS == []:
        return []

    for direction in directions:
        search_currentdirection(COL_LEN, MATRIX, ROW_LEN, WORDS, direction, foundwords_dic)

    foundwords_lst = dic_to_list(foundwords_dic)

    return foundwords_lst


def write_output_file(results, output_filename):
    """This function writes the pairs list of found words in matrix to a text file and creates it if needed"""

    with open(output_filename, 'w') as foundwords_output:
        for i in range(len(results)):
            word, count = results[i]
            if i < len(results) - 1:
                foundwords_output.write(word + "," + str(count) + '\n')
            else:
                # to prevent an empty line in the end of the output file
                foundwords_output.write(word + "," + str(count))

    return foundwords_output


def set_program_parametrs():
    """set parameters for the main function """
    MATRIX_FILE = sys.argv[2]
    WORDS_FILE = sys.argv[1]
    DIRECTIONS = sys.argv[4]
    OUTPUT_FILE = sys.argv[3]
    words_lst = read_wordlist_file(WORDS_FILE)
    matrix = read_matrix_file(MATRIX_FILE)
    return DIRECTIONS, matrix, OUTPUT_FILE, words_lst


def main():
    """This function uses all the other functions to play the whole game"""
    DIRECTIONS, matrix, OUTPUT_FILE, words_lst = set_program_parametrs()

    if check_input_args(ARGS) != None:
        # if the args are invalid it prints a message for it and the output file became empty
        print(check_input_args(ARGS))
        open(OUTPUT_FILE, "w").close()


    else:
        # else it searches for words in the list that shown in the matrix in chosen directions and count them.
        results = find_words_in_matrix(words_lst, matrix, DIRECTIONS)

        if results == []:
            # if the results empty which means no words found in the matrix the output file became empty
            open(OUTPUT_FILE, "w").close()

        else:
            # else the output file is lines of words found in chosen directions and their count
            write_output_file(results, OUTPUT_FILE)


if __name__ == "__main__":
    main()
