from explorer import Explorer

if __name__ == '__main__':
    explorer = Explorer()
    explorer.run()

# TODO
# Deal with end game state (don't crash)
# Actually stop searching hint when word found (probably in traverse function)
# Search for real words first in hints and then nonsense (minor speedup maybe)
# Find a way to deal with changing classes for buttons, divs