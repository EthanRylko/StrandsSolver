from typing import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.remote.webelement import WebElement

driver_path = 'C:\\Users\\egame\\chromedriver'
options = Options()
driver = webdriver.Chrome(options=options)

start_button_class = 'Feo8La_playButton'
close_button_class = 'PwGt5a_closeX'
hint_div_class = 'XmXXwG_hint'
board_class = 'UOpmtW_board'

# I hope these stay cosntant
ROWS = 8
COLS = 6



def start():
    """
    Click through some buttons to get to the puzzle
    """
    print('Hello World!')

    driver.get('https://www.nytimes.com/games/strands')
    start_button = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, start_button_class)))
    start_button.click()

    close_button = WebDriverWait(driver, 2).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, close_button_class)))
    close_button.click()


def find_total_words():
    """
    Find the total number of words in the puzzle

    Returns:
        int: Number of words to find in the puzzle
    """
    hint_div = WebDriverWait(driver, 2).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, hint_div_class)))
    paragraph = hint_div.find_element(By.TAG_NAME, 'p')
    bold_tags = paragraph.find_elements(By.TAG_NAME, 'b')

    if bold_tags:
        total_words = int(bold_tags[-1].text)
        print(f'There are {total_words} words in this puzzle.')
        return total_words

    else:
        print('Bold Tags not found, how many words are there?')
        return 0


def print_board(board: List[List[WebElement]]):
    """
    Print the board in a human-readable format

    Args:
        list(list(WebElement)) board:

    """
    for row in board:
        for button in row:
            print(f'{button.text}', end=' ')
        print('')


def load_board() -> List[List[WebElement]]:
    """
    Load the board into an array of buttons that can be clicked through later

    Returns:
        list(list(WebElement)): Array of buttons
    """
    board = list()
    counter = 0

    board_div = WebDriverWait(driver, 2).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, board_class)))
    for y in range(ROWS):
        row = list()
        for x in range(COLS):
            button = board_div.find_element(By.ID, f'button-{counter}')
            row.append(button)

            counter += 1

        board.append(row)
    
    print_board(board)
    return board


if __name__ == '__main__':
    start()
    total_words = find_total_words()
    board = load_board()

    while (True):
        pass
