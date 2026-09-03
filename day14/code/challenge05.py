"""Challenge 5: 钻石继承调试"""
class Device:
    def __init__(self):
        self.powered = False
    def toggle(self):
        self.powered = not self.powered
        return self.powered

class Camera(Device):
    def __init__(self):
        super().__init__()
        self.recording = False

class Wifi(Device):
    def __init__(self):
        super().__init__()
        self.connected = False

# TODO: 创建 Smartphone 同时继承 Camera 和 Wifi
# TODO: 打印 MRO
# TODO: 验证 super() 不会重复调用 Device.__init__
