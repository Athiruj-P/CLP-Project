# Node
# Description : คลาสจัดการข้อมูลภายใน Node
# Author : Athiruj Poositaporn

from .RotationType import RotationType
from .Box import Box
# from .global_var import START_POSITION, USED_VOLUME
from . import global_var
import logging
import logging.config
logger = logging.getLogger("planner_controller")
class Node: 
    def __init__(self, width, height, depth) : 
        # Leaf
        self.left = None
        self.center = None
        self.right = None

        # Node data
        self.position = global_var.START_POSITION
        self.width = width
        self.height = height
        self.depth = depth

        # Box data
        self.box = None

    # get_volume
    # Description : ฟังก์ชันคำนวณปริมาตรของพื้นที่ว่างที่ Node มีอยู่
    # Author : Athiruj Poositaporn
    def get_volume(self):
        return self.width * self.height * self.depth

    # get_box_dimension
    # Description : ฟังก์ชันดึงข้อมูลตำแหน่งภายในตู้บรรจุสินค้าของกล่องบรรจุสินค้า 
    # Author : Athiruj Poositaporn
    def get_box_dimension(self):
        dim1, dim2, dim3 = self.box.get_int_dimension()
        x1 = self.position[0] # width
        y1 = self.position[2] # depth
        z1 = self.position[1] # height

        x2 = self.position[0] + dim1
        y2 = self.position[2] + dim3
        z2 = self.position[1] + dim2

        box_dim = {
            'x' : [x1,x1,x2,x2,x1,x1,x2,x2],
            'y' : [y1,y2,y1,y2,y1,y2,y1,y2],
            'z' : [z1,z1,z1,z1,z2,z2,z2,z2],
        }

        return box_dim

    # get_box_detail
    # Description : ฟังก์ชันดึงข้อมูลของกล่องบรรจุสินค้า รวมไปถึงตำแหน่งภายในตู้บรรจุสินค้า
    # Author : Athiruj Poositaporn
    def get_box_detail(self):
        box_dim = self.get_box_dimension()
        box_detail = self.box.get_detail()
        return {'box_dim' : box_dim, 'box_detail' : box_detail}

    # put_item
    # Description : ฟังก์ชันคำนวณการนำกล่องไปใส่ใน Node 
    # Author : Athiruj Poositaporn
    def put_item(self, box):
        fit = False

        # Loop ตามการหมุนของกล่องเพื่อหาด้านที่ fit กับพื้นที่
        # เริ่มจากกล่องในมุมแบบเดิมก่อน แล้วถ้าใสไม่ได้ค่อยเปลี่ยนแนวกล่อง
        for i in range(0, len(RotationType.ALL)):
            if(box.fixed_direction):
                if(i == 0 or i == 3):
                    box.rotation_type = i
                else:
                    continue
            box.rotation_type = i
            dimension = box.get_dimension()
            box_w = dimension[0]
            box_h = dimension[1]
            box_d = dimension[2]
             
            # ถ้าขนาดของกล่องเทียบกับพื้นที่แล้วใส่ไม่ได้จะข้ามไปเพื่อหมุนกล่อง
            if (
                self.width < box_w or
                self.height < box_h or
                self.depth < box_d
            ):
                continue
            # กล่องใส่ในพื้นที่ได้
            fit = True

            # เก็บกล่องไปที่ node ปัจจุบัน
            if fit:
                self.box = box
                # global USED_VOLUME
                global_var.USED_VOLUME += box.get_volume()
                # ตรวจสอบพื้นที่ว่างด้านบนกล่อง (ด้าน height)
                if(self.height - box_h > 0):
                    # เพิ่ม node สำหรับพื้นที่ว่างด้านบนกล่อง
                    new_width = box_w #width
                    new_height = self.height - box_h
                    new_depth = box_d #depth
                    self.left = Node(new_width,new_height,new_depth)
                    # (width)
                    x = self.position[0]
                    y = self.position[1] + box_h
                    z = self.position[2]
                    self.left.position = [x,y,z]                    
                
                # ตรวจสอบพื้นที่ว่างด้านกว้าง (ด้าน width)
                if(self.width - box_w > 0):
                    # เพิ่ม node สำหรับพื้นทที่ว่างด้านกว้าง
                    new_width = self.width - box_w
                    new_height = self.height
                    new_depth = box_d #depth
                    self.center = Node(new_width,new_height,new_depth)
                    x = self.position[0] + box_w
                    y = self.position[1]
                    z = self.position[2]
                    self.center.position = [x,y,z]  
                
                # ตรวจสอบพื้นที่ว่างด้านยาว (ด้าน depth)
                if(self.depth - box_d > 0):
                    # เพิ่ม node สำหรับพื้นทที่ว่างด้านยาว
                    new_width = self.width
                    new_height = self.height
                    new_depth = self.depth - box_d
                    self.right = Node(new_width,new_height,new_depth)
                    x = self.position[0]
                    y = self.position[1]
                    z = self.position[2] + box_d
                    self.right.position = [x,y,z] 
            # return fit (True)
            return fit
        
        # return not fit (False)
        return fit
