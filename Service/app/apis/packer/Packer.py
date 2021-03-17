# Packer
# Description : คลาสสำหรับจัดเรียงกล่องบรรจุสินค้า
# Author : Athiruj Poositaporn

from .Box import Box
from .Node import Node
from . import global_var
import logging
import logging.config
logger = logging.getLogger("planner_controller")

class Packer:
    def __init__(self):
        self.root_nodes = []
        self.boxes = []
        self.total_boxes = 0

    # add_root_node
    # Description : ฟังก์ชันกำหนดค่า Root node (Node ของ container)
    # Author : Athiruj Poositaporn
    def add_root_node(self, node):
        return self.root_nodes.append(node)

    # add_box
    # Description : ฟังก์ชันเพิ่มกล่องบรรจุสินค้าสำหรับเตรียมการจัดเรียง
    # Author : Athiruj Poositaporn
    def add_box(self, box):
        self.total_boxes = len(self.boxes) + 1
        return self.boxes.append(box)

    # pack_to_node
    # Description : ฟังก์ชันเพิ่มกล่องบรรจุสินค้าให้แก่ Node ที่สามารถบรรจุได้
    # Author : Athiruj Poositaporn
    def pack_to_node(self, node, box):
    # Recursive function: To pack a box into a node
        fitted = True
        # ใส่กล่องให้ Node
        if not node.box:            
            response = node.put_item(box)
            
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

    # pack
    # Description : ฟังก์ชันนำกล่องที่ได้จัดเตรียมไว้มาใส่ใน Node
    # Author : Athiruj Poositaporn
    def pack(self, bigger_first=True):
        self.root_nodes.sort(
            key=lambda node: node.get_volume(), reverse=bigger_first
        )
        self.boxes.sort(
            key=lambda box: box.get_volume(), reverse=bigger_first
        )

        # ลูปสำหรับนำแต่ละกล่องไปใส่ในตู้
        for node in self.root_nodes:
            for box in self.boxes:
                fited = self.pack_to_node(node, box)
                if(not fited):
                    global_var.UNFITTED_ITEMS.append(box.get_detail())

    # get_stack
    # Description : ฟังก์ชันท่องไปใน Ternary tree เพิ่มนำข้อมูลของกล่องมาจัดเรียงเป็น Stack
    # Author : Athiruj Poositaporn
    def get_stack(self, root, opt=True):
        # opt ใช้บังคับไม่ให้ Node ที่เป็นฐานไปดึงข้อมูลจากส่วนอื่นที่ไม่ใช่ "ด้านบน" หรือ Left node
        if(root.box):
            global_var.BOXES_STACK_DETAIL.append(root.get_box_detail())
            if(root.left != None):
                self.get_stack(root.left)
            if(root.center != None and opt):
                self.get_stack(root.center)
            if(root.right != None and opt):
                self.get_stack(root.right)
    
    # format_unfitted_item
    # Description : ฟังก์ชันจัดเรียงรูปแบบของข้อมูลของกล่องที่ไม่สามารถนำไปใส่ในตู้ได้
    # Author : Athiruj Poositaporn
    def format_unfitted_item(self):
        tmp = global_var.UNFITTED_ITEMS
        tmp_arr = []
        tmp_id = []
        tmp_name = []
        if(tmp):
            # เรียงลำดับของกล่องตาม box_id
            tmp.sort(key=lambda x: (x['box_id']), reverse=False)
            
            for item in tmp:
                tmp_id.append(item['box_id'])
                tmp_id = list(dict.fromkeys(tmp_id))
            
            for box_id in tmp_id:
                tmp_dict = {}
                tmp_num = 0
                for item in tmp:
                    if(item['box_id'] == box_id):
                        tmp_num = tmp_num + 1
                        tmp_dict = item
                        tmp_dict['box_unfitted'] = tmp_num
                        tmp_dict['box_name'] = tmp_dict['box_name'][:tmp_dict['box_name'].rfind("-")]
                tmp_arr.append(tmp_dict)
            
        return tmp_arr
            
            

        