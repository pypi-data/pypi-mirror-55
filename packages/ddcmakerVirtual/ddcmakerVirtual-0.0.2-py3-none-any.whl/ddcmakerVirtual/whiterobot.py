# import cv2
# import time


from inspect import signature
from functools import wraps


def typeassert(*type_args, **type_kwargs):
    def decorate(func):
        sig = signature(func)
        bound_types = sig.bind_partial(*type_args, **type_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError('Argument {} must be {}'.format(name, bound_types[name]))
            return func(*args, **kwargs)

        return wrapper

    return decorate





class robot(object):
    # lsc.MoveServo(6, 1500, 1000)
    # lsc.MoveServo(7, 1500, 1000)
    # time.sleep(2.1)

    def up(self, step=1):
        # lsc.RunActionGroup(0, step)
        # lsc.WaitForFinish(5000)
        # time.sleep(1.2)
        # print("机器人站立")
        print({"code": 0, "times": step})

    def down(self, step=1):
        # lsc.RunActionGroup(14, step)
        # lsc.WaitForFinish(5000)
        # time.sleep(1)
        # print("机器人蹲下")
        print({"code": 14, "times": step})

    def check(self, step=1):
        # lsc.RunActionGroup(188, step)
        # lsc.WaitForFinish(5000)
        # time.sleep(1)
        # print("机器人自检")
        print({"code": 188, "times": step})

    def forward(self, step=1):
        # for i in range(step):
            # lsc.RunActionGroup(1, 1)
            # lsc.WaitForFinish(5000)
            # time.sleep(2)
            # print("机器人前进")
        print({"code": 1, "times": step})

    def backward(self, step=1):
        # for i in range(step):
            # lsc.RunActionGroup(2, 1)
            # lsc.WaitForFinish(5000)
            # time.sleep(2)
            # print("机器人后退")
        print({"code": 2, "times": step})

    def left(self, step=1):
        # for i in range(step):
            # lsc.RunActionGroup(3, 1)
            # lsc.WaitForFinish(5000)
            # time.sleep(2)
            # print("<---机器人左转")
        print({"code": 3, "times": step})

    def right(self, step=1):
        # for i in range(step):
            # lsc.RunActionGroup(4, 1)
            # lsc.WaitForFinish(5000)
            # time.sleep(2)
            # print("机器人右转--->")
        print({"code": 4, "times": step})


    def nod(self, step=1):
        # for i in range(step):
            # PWMServo.setServo(1, 1800, 200)
            # time.sleep(0.3)
            # PWMServo.setServo(1, 1200, 200)
            # time.sleep(0.3)
            # PWMServo.setServo(1, 1500, 100)
            # time.sleep(1)
            # print("机器人点头")
        print({"code": 54, "times": step})

    def shaking_head(self, step=1):
        # for i in range(step):
            # PWMServo.setServo(2, 1800, 200)
            # time.sleep(0.4)
            # PWMServo.setServo(2, 1200, 200)
            # time.sleep(0.4)
            # PWMServo.setServo(2, 1500, 100)
            # time.sleep(1)
            # print("机器人摇头")
        print({"code": 55, "times": step})

    '''这里的动作组不再是点头摇头了，需要重新写'''
    # =======================================================
    def left_slide(self, step=1):
        # for i in range(step):
            # lsc.RunActionGroup(11, 1)
            # lsc.WaitForFinish(5000)
            # time.sleep(1)
            # print("<<<*****机器人左滑")
        print({"code": 11, "times": step})

    def right_slide(self, step=1):
        # for i in range(step):
            # lsc.RunActionGroup(12, 1)
            # lsc.WaitForFinish(5000)
            # time.sleep(1)
            # print("机器人右滑*****>>>")
        print({"code": 12, "times": step})

    def push_up(self, step=1):
        # lsc.RunActionGroup(7, step)
        # time.sleep(7.5)
        # print("机器人俯卧撑")
        print({"code": 7, "times": step})

    def abdominal_curl(self, step=1):
        # lsc.RunActionGroup(8, step)
        # time.sleep(9.8)
        # print("机器人仰卧起坐")
        print({"code": 8, "times": step})

    def wave(self, step=1):
        # for i in range(step):
            # lsc.RunActionGroup(9, 1)
            # time.sleep(3.1)
            # print("机器人挥手┏(＾0＾)┛")
        print({"code": 9, "times": step})

    def bow(self, step=1):
        # lsc.RunActionGroup(10, step)
        # time.sleep(4.1)
        # print("机器人鞠躬╰(￣▽￣)╭")
        print({"code": 10, "times": step})

    def spread_wings(self, step=1):
        # lsc.RunActionGroup(13, step)
        # time.sleep(10.5)
        # print("机器人大鹏展翅")
        print({"code": 13, "times": step})

    def haha(self, step=1):
        # lsc.RunActionGroup(15, step)
        # time.sleep(8.2)
        # print("机器人哈哈大笑o(*￣▽￣*)o")
        print({"code": 15, "times": step})

    def straight_boxing(self, step=1):
        # lsc.RunActionGroup(30, step)
        # time.sleep(1.9)
        # print("机器人直拳连击")
        print({"code": 30, "times": step})

    def lower_hook_combo(self, step=1):
        # lsc.RunActionGroup(31, step)
        # time.sleep(2.8)
        # print("机器人下勾拳连击")
        print({"code": 31, "times": step})

    def left_hook(self, step=1):
        # lsc.RunActionGroup(32, step)
        # time.sleep(1.7)
        # print("机器人左勾拳")
        print({"code": 32, "times": step})

    def right_hook(self, step=1):
        # lsc.RunActionGroup(33, step)
        # time.sleep(1.4)
        # print("机器人右勾拳")
        print({"code": 33, "times": step})

    def punching(self, step=1):
        # lsc.RunActionGroup(34, step)
        # time.sleep(2)
        # print("机器人攻步冲拳")
        print({"code": 34, "times": step})

    def crouching(self, step=1):
        # lsc.RunActionGroup(35, step)
        # time.sleep(3)
        # print("机器人八字蹲拳")
        print({"code": 35, "times": step})

    def yongchun(self, step=1):
        # lsc.RunActionGroup(36, step)
        # time.sleep(2.5)
        # print("机器人咏春拳")
        print({"code": 36, "times": step})

    def beat_chest(self, step=1):
        # lsc.RunActionGroup(37, step)
        # time.sleep(7)
        # print("机器人捶胸")
        print({"code": 37, "times": step})

    def left_side_kick(self, step=1):
        # lsc.RunActionGroup(50, step)
        # time.sleep(1.5)
        # print("机器人左侧踢")
        print({"code": 50, "times": step})

    def right_side_kick(self, step=1):
        # lsc.RunActionGroup(51, step)
        # time.sleep(2)
        # print("机器人右侧踢")
        print({"code": 51, "times": step})

    def left_foot_shot(self, step=1):
        # lsc.RunActionGroup(52, step)
        # time.sleep(1.5)
        # print("机器人左脚射门")
        print({"code": 52, "times": step})

    def right_foot_shot(self, step=1):
        # lsc.RunActionGroup(53, step)
        # time.sleep(1.5)
        # print("机器人右脚射门")
        print({"code": 53, "times": step})

    def show_poss(self, step=1):
        # print("机器人摆拍poss")
        # lsc.RunActionGroup(60, step)
        # time.sleep(60)
        print({"code": 60, "times": step})

    def inverted_standing(self, step=1):
        # lsc.RunActionGroup(101, step)
        # time.sleep(5)
        # print("机器人前倒站立")
        print({"code": 101, "times": step})

    def rear_stand_up(self, step=1):
        # lsc.RunActionGroup(102, step)
        # time.sleep(5)
        # print("机器人后倒站立")
        print({"code": 102, "times": step})


"""
-----------------------我也是有底线的-------------------------
"""