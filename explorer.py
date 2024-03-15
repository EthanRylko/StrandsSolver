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
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from time import sleep


start_button_class = 'Feo8La_playButton'
close_button_class = 'PwGt5a_closeX'
hint_div_class = 'XmXXwG_hint'
board_class = 'UOpmtW_board'

# I hope these stay cosntant
ROWS = 8
COLS = 6

class ButtonInfo():
    def __init__(self, text, id):
        self.text = text
        self.id = id
        self.visited = False
        self.hint = False


class Explorer():

    def __init__(self):
        nltk.download('words')
        self.word_set = set(words.words())
        self.driver = webdriver.Chrome()
        self.tried = set()
        self.board = [[None for x in range(COLS)] for y in range(ROWS)]


    def run(self):
        self.start()
        self.total_words = self.find_total_words()
        self.load_board()
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
        self.hint_div = WebDriverWait(self.driver, 2).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, hint_div_class)))
        paragraph = self.hint_div.find_element(By.TAG_NAME, 'p')
        bold_tags = paragraph.find_elements(By.TAG_NAME, 'b')

        if bold_tags:
            total_words = int(bold_tags[-1].text)
            print(f'There are {total_words} words in this puzzle.')
            return total_words

        else:
            print('Bold Tags not found, how many words are there?')
            return 0
        

    def load_board(self):
        """
        Load the board into an array of buttons that can be clicked through later
        """
        counter = 0

        self.board_div = WebDriverWait(self.driver, 2).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, board_class)))
        for y in range(ROWS):
            for x in range(COLS):
                try:
                    button = self.board_div.find_element(By.ID, f'button-{counter}')
                    button_id = button.get_property('id')
                    button_info = ButtonInfo(button.text[0], button_id)
                    if 'border: 3px dashed var(--hint-blue);' in button.get_attribute('style'):
                        print(f'hint at {x}, {y}')
                        button_info.hint = True

                except NoSuchElementException:
                    button_info = None

                self.board[y][x] = button_info
                counter += 1
        

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
                    self.load_board()

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
        #self.print_by_breadth(root, word_length)
        self.traverse(root, word_length, list())
        # at each attempt, check the word count to see if there is a success. If so, update the grid to eliminate some letters


    def add_surroundings(self, node: Node, x: int, y: int, depth: int, word_length: int, hint_mode: bool = False):
        """
        Fill tree by adding surrounding buttons as children

        Args:
            Node node: Node to check around
            int x: x-position of current node
            int y: y-position of current node
            int depth: Depth of tree
            int word_length: Maximum depth
            bool hint_mode: True if searching through hint
        """
        if depth == word_length:
            return

        for offset_y in (-1, 0, 1):
            for offset_x in (-1, 0, 1):
                if offset_x == 0 and offset_y == 0:
                    continue

                if self.is_valid_index(x + offset_x, y + offset_y, hint_mode) and self.not_in_lineage(node, self.board[y + offset_y][x + offset_x]):
                    child = node.add_child(self.board[y + offset_y][x + offset_x])

                    # recursively find children
                    self.add_surroundings(child, x + offset_x, y + offset_y, depth + 1, word_length, hint_mode)

        #print(f'Node {node.data.text} has {0 if node.children is None else len(node.children)} children')


    def is_valid_index(self, x: int, y: int, hint_mode: bool) -> bool:
        """
        Check if index is within bounsd of the board

        Args:
            int x: x-position being checked
            int y: y-position being checked
            bool hint_mode: True if searching through hint

        Returns:
            bool: True if valid, else False
        """
        in_bounds = x in range(COLS) and y in range(ROWS)
        if in_bounds and hint_mode:
            return in_bounds and self.board[y][x].hint
        return in_bounds


    def not_in_lineage(self, node: Node, data: ButtonInfo) -> bool:
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
        
        # search_id = data.get_attribute('id')
        # parent_id = node.parent.data.get_attribute('id')
        # print(f'compare {search_id} and {parent_id}')
        if data.id == node.parent.data.id:
            return False

        return self.not_in_lineage(node.parent, data)


    def traverse(self, node: Node, word_length: int, path: List = list(), hint_mode: bool = False):
        """
        Print paths of all traversals of tree, recursively

        Args:
            Node node: Node to start from
            str path: Path traveled as a string of characters
            bool hint_mode: True if searching through hint
        """
        if node is None:
            return
        
        path.append(node.data)

        if word_length == 1:
            word = str()
            for item in path:
                word += item.text
            
            in_dictionary = word.lower() in self.word_set or word.lower() + 's' in self.word_set

            # hint mode, try any possible combination
            if hint_mode:
                print('traverse in hint_mode')
                print(f'tried {word}')
                self.click_on_path(path, hint_mode=True)
           
            # Found a real word
            elif word not in self.tried and in_dictionary:
                print(f'tried {word}')
                self.click_on_path(path)
                self.tried.add(word)

        else:
            for child in node.children:
                self.traverse(child, word_length - 1, path[:], hint_mode)
                

    def click_on_path(self, path, hint_mode = False):
        for item in path:
            # get id
            # need access to board div somehow...
            #print(f'Button {item.text} with id {item.id}')

            button = self.board_div.find_element(By.ID, item.id)

            # click
            button.click()
            self.load_board()

        # end of path, click again
        button.click()

        # TODO: Verify word
        # check word count, if increased then return true
        print(hint_mode)
        return self.verify_word(hint_mode)
        
    
    def verify_word(self, hint_mode = False):
        print(f'verify word hint mode {hint_mode}')

        # hint?
        try:
            hint_button = WebDriverWait(self.driver, 0.2).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'XmXXwG_lightbulb')))
        except TimeoutException:
            if hint_mode:
                return False

            hint_button = WebDriverWait(self.driver, 0.2).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'XmXXwG_bluebulb')))
            hint_button.click()
            self.search_among_hints()
            return True # ???
        
        # no hint :(
        print('need more hints')
        return False
    

    def search_among_hints(self):
        # find subset that are hint letters
        self.load_board()
        hint_list = list()
        for y in range(ROWS):
            for x in range(COLS):
                if self.board[y][x].hint:
                    hint_list.append((x, y))
        
        word_length = len(hint_list)
        print(hint_list)
        for coord in hint_list:
            x, y = coord
            root = Node(self.board[y][x])
            print(x, y, root.data.text)
            self.add_surroundings(root, x, y, 1, word_length, True)
            self.traverse(root, word_length, list(), True)
            sleep(0.1)
            self.load_board()



    def print_by_breadth(self, root, depth):
        nodes = [root]
        children = list()
        for i in range(depth):
            for node in nodes:
                print(node.data.text, end='')
                if node.children is None:
                    continue
                for child in node.children:
                    children.insert(0, child)

            print('')
            nodes = children
            children = list()
            
"""
Note for later
When hint is active, button class has dashed outline
style="border: 3px dashed var(--hint-blue);"
Maybe when hint button is available, use, and then go into a subroutine that only checks the hint area
Must solve hint before using another, even if enough words found to get another
style="color: white; background-color: black;"
"""