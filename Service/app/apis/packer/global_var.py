def init():
    global UNFITTED_ITEMS
    global BASE_BOXES
    global START_POSITION
    global USED_VOLUME
    global BOXES_STACK
    
    UNFITTED_ITEMS = [] # List of unfitted node
    BASE_BOXES = [] # Start node of each stack
    START_POSITION = [0, 0, 0]
    USED_VOLUME = 0
    BOXES_STACK = []