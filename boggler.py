import random
import enchant
from EnglishNGraphs import *

DICT = enchant.Dict("en_US")

BOARD_EDGE_LENGTH = 4


def boggle():
    board = create_board()
    words = find_words(board)

    [print(word) for word in sorted(words)]


def create_board():
    board = []
    for _ in range(BOARD_EDGE_LENGTH):
        row = []
        for __ in range(BOARD_EDGE_LENGTH):
            c_or_v = random.choices(LETTER_TYPES, TYPE_WEIGHTS)[0]
            letter = random.choice(c_or_v)
            row.append(letter)
        board.append(row)

    print_board(board)
    return board


def find_words(board):
    # create graph
    visited_status, neighbor_graph = create_graph(board)

    # traverse graph
    words = gather_words(board, visited_status, neighbor_graph)

    return words


def create_graph(board):
    visited_status = {(i, j): False for j in range(BOARD_EDGE_LENGTH) for i in range(BOARD_EDGE_LENGTH)}

    neighbors = dict()
    for i, row in enumerate(board):
        for j, letter in enumerate(board[i]):
            add_neighbors(neighbors, i, j)

    return visited_status, neighbors


def add_neighbors(neighbors, i, j):
    current = (i, j)
    neighbors[current] = set()

    up = i - 1
    down = i + 1
    left = j - 1
    right = j + 1

    # up
    if i > 0:
        # up left
        if j > 0:
            neighbor = (up, left)
            neighbors[current].add(neighbor)

        # up
        neighbor = (up, j)
        neighbors[current].add(neighbor)

        # up right
        if j < (BOARD_EDGE_LENGTH - 1):
            neighbor = (up, right)
            neighbors[current].add(neighbor)

    # horizontal
    if j > 0:
        neighbor = (i, left)
        neighbors[current].add(neighbor)
    if j < (BOARD_EDGE_LENGTH - 1):
        neighbor = (i, right)
        neighbors[current].add(neighbor)

    # down
    if i < (BOARD_EDGE_LENGTH - 1):
        # down left
        if j > 0:
            neighbor = (down, left)
            neighbors[current].add(neighbor)

        # down
        neighbor = (down, j)
        neighbors[current].add(neighbor)

        # down right
        if j < (BOARD_EDGE_LENGTH - 1):
            neighbor = (down, right)
            neighbors[current].add(neighbor)


def gather_words(board, visited_status, neighbor_graph):
    all_words = set()

    for i in range(BOARD_EDGE_LENGTH):
        for j in range(BOARD_EDGE_LENGTH):
            print("Checking " + str(i) + " " + str(j))
            words = traverse_board(board, visited_status, neighbor_graph, i, j, "", 0, 0, 0)
            all_words = all_words.union(words)

    print()
    return all_words


def traverse_board(board, visited_status, neighbor_graph, i, j, current_word, c_in_a_row, v_in_a_row, l_in_a_row):
    node = (i, j)
    words = set()
    visited_status[node] = True
    letter = board[i][j]

    current_word += letter
    l_in_a_row += 1

    if len(current_word) >= MIN_WORD_LEN and DICT.check(current_word):
        words.add(current_word)
        l_in_a_row = 0

    #print(current_word)

    should_continue, c_in_a_row, v_in_a_row = check_current_word(current_word, letter, c_in_a_row, v_in_a_row, l_in_a_row)

    # recursively visit unvisited neighbors
    if should_continue:
        for neighbor in neighbor_graph[node]:
            if not visited_status[neighbor]:
                visited_status[neighbor] = True

                neighbor_i = neighbor[0]
                neighbor_j = neighbor[1]

                child_words = traverse_board(board, visited_status, neighbor_graph, neighbor_i, neighbor_j,
                                             current_word, c_in_a_row, v_in_a_row, l_in_a_row)
                words = words.union(child_words)

                visited_status[neighbor] = False

    visited_status[node] = False
    l_in_a_row -= 1

    return words


def print_board(board):
    print()
    for row in board:
        for letter in row:
            print(letter, end=" ")
        print()
    print()


if __name__ == '__main__':
    boggle()
