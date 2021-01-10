from .RotationType import RotationType
from .Box import Box
# from .global_var import START_POSITION, USED_VOLUME
import global_var

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
        self.box = Box()

    def get_volume(self):
        return self.width * self.height * self.depth

    def put_item(self, box):
        fit = False
        # valid_box_position = box.position
        # box.position = self.position

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
     
            print(self.get_box_dimension_and_position())
            FILE.write("0 {}\n".format(self.get_box_dimension_and_position()))
            FILE_html.write("{}\n".format(self.get_box_dimension()))
            # return fit (True)
            return fit
        
        # return not fit (False)
        return fit

    # def get_box_dimension_and_position(self):
    #     x = self.position[0]
    #     y = self.position[1]
    #     z = self.position[2]
    #     return "{} {} {} {}".format(self.box.get_data(),int(x),int(y),int(z))