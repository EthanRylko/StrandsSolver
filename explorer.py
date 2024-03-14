from tree import Node
from typing import *
from selenium.webdriver.remote.webelement import WebElement
import nltk
from nltk.corpus import words
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webelement import WebElement

start_button_class = 'Feo8La_playButton'
close_button_class = 'PwGt5a_closeX'
hint_div_class = 'XmXXwG_hint'
board_class = 'UOpmtW_board'

# I hope these stay cosntant
ROWS = 8
COLS = 6

class Explorer():

    def __init__(self):
        nltk.download('words')
        self.word_set = set(words.words())
        self.driver = webdriver.Chrome()

    def run(self):
        self.start()
        self.total_words = self.find_total_words()
        self.board = self.load_board()
        self.print_board()
        self.solve()


    def start(self):
        """
        Click through some buttons to get to the puzzle
        """
        print('Hello World!')

        self.driver.get('https://www.nytimes.com/games/strands')
        start_button = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, start_button_class)))
        start_button.click()

        close_button = WebDriverWait(self.driver, 2).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, close_button_class)))
        close_button.click()


    def print_board(self):
        """
        Print the board in a human-readable format
        """
        for row in self.board:
            for button in row:
                print(f'{button.text}', end=' ')
            print('')


    def find_total_words(self):
        """
        Find the total number of words in the puzzle

        Returns:
            int: Number of words to find in the puzzle
        """
        hint_div = WebDriverWait(self.driver, 2).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, hint_div_class)))
        paragraph = hint_div.find_element(By.TAG_NAME, 'p')
        bold_tags = paragraph.find_elements(By.TAG_NAME, 'b')

        if bold_tags:
            total_words = int(bold_tags[-1].text)
            print(f'There are {total_words} words in this puzzle.')
            return total_words

        else:
            print('Bold Tags not found, how many words are there?')
            return 0

    def load_board(self) -> List[List[WebElement]]:
        """
        Load the board into an array of buttons that can be clicked through later

        Returns:
            List[List[WebElement]]: Array of buttons
        """
        board = list()
        counter = 0

        board_div = WebDriverWait(self.driver, 2).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, board_class)))
        for y in range(ROWS):
            row = list()
            for x in range(COLS):
                button = board_div.find_element(By.ID, f'button-{counter}')
                row.append(button)

                counter += 1

            board.append(row)
        
        return board


    def solve(self):
        """
        Solve puzzle!
        """
        solved = False
        found_words = 0
        word_length = 4

        while not solved:
            for y, row in enumerate(self.board):
                for x, button in enumerate(row):
                    self.check_all_words(x, y, word_length)

            # all words of length word_length found, go up one
            word_length += 1


    def check_all_words(self, x: int, y: int, word_length: int):
        """
        Check from a starting point all possible words with a given length

        args:
            int x: x-position on board to search from
            int y: y-position on board to search from
            int word_length: Length of words being searched
        """
        # button at x, y is root of tree
        root = Node(self.board[y][x])

        # get surroundings (check if edge or already in other word)
        self.add_surroundings(root, x, y, 1, word_length)
        print(f'finished {x}, {y} search for length {word_length}')

        # repeat until word_length reached
        # traverse tree, clicking on buttons
        # TODO: Click on buttons
        self.traverse(root)
        # at each attempt, check the word count to see if there is a success. If so, update the grid to eliminate some letters


    def add_surroundings(self, node: Node, x: int, y: int, depth: int, word_length: int):
        """
        Fill tree by adding surrounding buttons as children

        Args:
            Node node: Node to check around
            int x: x-position of current node
            int y: y-position of current node
            int depth: Depth of tree
            int word_length: Maximum depth
        """
        if depth == word_length:
            return

        for offset_y in (-1, 0, 1):
            for offset_x in (-1, 0, 1):
                if offset_x == 0 and offset_y == 0:
                    continue

                if self.is_valid_index(x + offset_x, y + offset_y) and self.not_in_lineage(node, self.board[y + offset_y][x + offset_x]):
                    child = node.add_child(self.board[y + offset_y][x + offset_x])

                    # recursively find children
                    self.add_surroundings(child, x + offset_x, y + offset_y, depth + 1, word_length)

        #print(f'Node {node.data.text} has {0 if node.children is None else len(node.children)} children')


    def is_valid_index(self, x: int, y: int) -> bool:
        """
        Check if index is within bounsd of the board

        Args:
            int x: x-position being checked
            int y: y-position being checked

        Returns:
            bool: True if valid, else False
        """
        return x in range(0, 6) and y in range(0, 8)


    def not_in_lineage(self, node: Node, data: WebElement) -> bool:
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

        return self.not_in_lineage(node.parent, data)


    def traverse(self, node: Node, path: List = list()):
        """
        Print paths of all traversals of tree, recursively

        Args:
            Node node: Node to start from
            str path: Path traveled as a string of characters
        """
        if node is None:
            return
        
        path.append(node.data)

        if node.children is None:
            #if path.lower() in self.word_set:
            #    # Found a real word
                self.click_on_path(path)
        else:
            for child in node.children:
                self.traverse(child, path)
                

    def click_on_path(self, path):
        for item in path:
            # get id
            #button_id = item.get_attribute('id')
            # need access to board div somehow...
            #button = board_div.find_element(By.ID, button_id)

            # click
            #button.click()
            pass

        # end of path, click again
        #button.click()

        # check word count, if increased then return true
        #return verify_word()

        # return false