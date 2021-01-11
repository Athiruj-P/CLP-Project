from .Box import Box
from .Node import Node
# from .global_var import BASE_BOXES, UNFITTED_ITEMS
from . import global_var
import logging
import logging.config
logger = logging.getLogger("planner_controller")

class Packer:
    def __init__(self):
        self.root_nodes = []
        self.boxes = []
        self.total_boxes = 0

    # Set container dimension
    def add_root_node(self, node):
        return self.root_nodes.append(node)
    
    def add_box(self, box):
        self.total_boxes = len(self.boxes) + 1
        return self.boxes.append(box)

    # Recursive function: To pack a box into a node
    def pack_to_node(self, node, box):

        fitted = True
        # ใส่กล่องให้ Node
        if not node.box:            
            response = node.put_item(box)
            
            # global BASE_BOXES
            if not response:
                return not fitted
            else:
                z = node.position[1]
                if(z == 0):
                    global_var.BASE_BOXES.append(node)
                return fitted
        # เปลี่ยน Node เพื่อหาที่ใส่กล่อง
        if node.left:
            if self.pack_to_node(node.left, box):
                return fitted
        
        if node.center:
            if self.pack_to_node(node.center, box):
                return fitted
        
        if node.right:
            if self.pack_to_node(node.right, box):
                return fitted
        
        return not fitted


    def pack(self, bigger_first=False):
        # self.root_nodes.sort(
        #     key=lambda node: node.get_volume(), reverse=bigger_first
        # )
        # self.boxes.sort(
        #     key=lambda box: box.get_volume(), reverse=bigger_first
        # )
        
        # global UNFITTED_ITEMS
        for node in self.root_nodes:
            for box in self.boxes:
                fited = self.pack_to_node(node, box)
                if(not fited):
                    global_var.UNFITTED_ITEMS.append(box)
    
    def get_stack(self, root, opt=True):
        # opt ใช้บังคับไม่ให้ Node ที่เป็นฐานไปดึงข้อมูลจากส่วนอื่นที่ไม่ใช่ "ด้านบน" หรือ Left node
        if(root.box):
            # file.write(root.get_box_dimension()+"\n")
            # global_var.BOXES_STACK.append(root.get_box_dimension())
            global_var.BOXES_STACK_DETAIL.append(root.get_box_detail())
            if(root.left != None):
                self.get_stack(root.left)
            if(root.center != None and opt):
                self.get_stack(root.center)
            if(root.right != None and opt):
                self.get_stack(root.right)