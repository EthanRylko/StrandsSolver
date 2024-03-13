from typing import *
from selenium.webdriver.remote.webelement import WebElement
from tree import *
import nltk
from nltk.corpus import words

nltk.download('words')
word_set = set(words.words())

def solve(board: List[List[WebElement]]):
    """
    Solve puzzle!

    args:
        List[List[WebElement]] board: Array of buttons
    """
    solved = False
    word_length = 4

    while not solved:
        for y, row in enumerate(board):
            for x, button in enumerate(row):
                check_all_words(board, x, y, word_length)

        while True:
            # stop for now
            pass

        # all words of length word_length found, go up one
        word_length += 1


def check_all_words(board: List[List[WebElement]], x: int, y: int, word_length: int):
    """
    Check from a starting point all possible words with a given length

    args:
        List[List[WebElement]] board: Array of buttons
        int x: x-position on board to search from
        int y: y-position on board to search from
        int word_length: Length of words being searched
    """
    # button at x, y is root of tree
    tree = Tree(board[y][x])
    node = tree.root

    # get surroundings (check if edge or already in other word)
    add_surroundings(node, x, y, board, 1, word_length)
    print(f'finished {x}, {y} search')

    # repeat until word_length reached
    # traverse tree, clicking on buttons
    # TODO: Click on buttons
    traverse(node)
    # at each attempt, check the word count to see if there is a success. If so, update the grid to eliminate some letters


def add_surroundings(node: Node, x: int, y: int, board: List[List[WebElement]], depth: int, word_length: int):
    """
    Fill tree by adding surrounding buttons as children

    Args:
        Node node: Node to check around
        int x: x-position of current node
        int y: y-position of current node
        List[List[WebElement]] board: Board to read
        int depth: Depth of tree
        int word_length: Maximum depth
    """
    if depth == word_length:
        return

    for offset_y in (-1, 0, 1):
        for offset_x in (-1, 0, 1):
            if offset_x == 0 and offset_y == 0:
                continue

            if is_valid_index(x + offset_x, y + offset_y) and not_in_lineage(node, board[y + offset_y][x + offset_x]):
                child = node.add_child(board[y + offset_y][x + offset_x])

                # recursively find children
                add_surroundings(child, x + offset_x, y + offset_y, board, depth + 1, word_length)

    #print(f'Node {node.data.text} has {0 if node.children is None else len(node.children)} children')


def is_valid_index(x: int, y: int) -> bool:
    """
    Check if index is within bounsd of the board

    Args:
        int x: x-position being checked
        int y: y-position being checked

    Returns:
        bool: True if valid, else False
    """
    return x in range(0, 6) and y in range(0, 8)


def not_in_lineage(node: Node, data: WebElement) -> bool:
    """
    Recursively check if data is present in lineage of node

    Args:
        Node node: Node being checked
        WebElement data: Data to look for

    Returns:
        bool: True not found, else False
    """
    if node.parent is None:
        return True
    
    search_id = data.get_attribute('id')
    parent_id = node.parent.data.get_attribute('id')
    # print(f'compare {search_id} and {parent_id}')
    if search_id == parent_id:
        return False

    return not_in_lineage(node.parent, data)


def traverse(node: Node, path: str = ''):
    """
    Print paths of all traversals of tree, recursively

    Args:
        Node node: Node to start from
        str path: Path traveled as a string of characters
    """
    if node is None:
        return
    
    path += node.data.text

    if node.children is None:
        if path.lower() in word_set:
            # Found a real word
            print(path)
            #click_on_path(path)
    else:
        for child in node.children:
            traverse(child, path)
            