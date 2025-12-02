from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 'p'
    HEADING = 'h'
    CODE = 'c'
    QUOTE = 'q'
    UNORDERED_LIST = 'u'
    ORDERED_LIST = 'o'

