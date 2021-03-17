# global_var
# Description : เก็บตัวแปรในรูปแบบ Global ซึ่งใช้ใน PlannerController, Packer และ Node 
# Author : Athiruj Poositaporn
def init():
    global UNFITTED_ITEMS
    global BASE_BOXES
    global START_POSITION
    global USED_VOLUME
    global BOXES_STACK
    global BOXES_STACK_DETAIL
    
    UNFITTED_ITEMS = [] # List of unfitted node
    BASE_BOXES = [] # Start node of each stack (Each node contain a bottom first box)
    START_POSITION = [0, 0, 0] # Start point to place the first box
    USED_VOLUME = 0 # The number of qubic unit (cm or inch) used in the container
    BOXES_STACK = []
    BOXES_STACK_DETAIL = [] # List of all stack (Each stack contains all data of each boxes)