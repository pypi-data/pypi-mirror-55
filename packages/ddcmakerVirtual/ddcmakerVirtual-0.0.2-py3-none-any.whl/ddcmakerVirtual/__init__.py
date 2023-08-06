""" 虚拟机器人包！！！！ """
__version__ = '0.0.2'
__metaclass__ = type
__all__ = [
    'car', 'whiterobot'
]


import os
import subprocess
from inspect import signature
from functools import wraps


def parameter_checking(*type_args, **type_kwargs):
    def decorate(func):
        sig = signature(func)
        bound_types = sig.bind_partial(*type_args, **type_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError('Argument [{}] must be {}'.format(name, bound_types[name]))
                if value < 0:
                    raise ArithmeticError("Argument [{}] must be positive integer!".format(name))
            return func(*args, **kwargs)

        return wrapper

    return decorate



from ddcmakerVirtual import car
Ca = car.car()


class Car(object):

    @staticmethod
    @parameter_checking(int, int)
    def left(step=1, speed=50):
        if step > 30:
            step = 30
            #print("参数值超过设置上限，默认运行最大上限次数 ", step)

        Ca.left(step, speed)

    @staticmethod
    @parameter_checking(int, int)
    def right(step=1, speed=50):
        if step > 30:
            step = 30
            #print("参数值超过设置上限，默认运行最大上限次数 ", step)
        Ca.right(step, speed)

    @staticmethod
    @parameter_checking(int, int)
    def forward(step=1, speed=50):
        if step > 30:
            step = 30
            #print("参数值超过设置上限，默认运行最大上限次数 ", step)
        Ca.forward(step, speed)

    @staticmethod
    @parameter_checking(int, int)
    def backward(step=1, speed=50):
        if step > 30:
            step = 30
            #print("参数值超过设置上限，默认运行最大上限次数 ", step)
        Ca.backward(step, speed)

    @staticmethod
    def stop():
        Ca.stop(0)




from ddcmakerVirtual import whiterobot
from ddcmakerVirtual import showlib

Rb = whiterobot.robot()
Sh = showlib.showlib()

class Robot(object):

    @staticmethod
    @parameter_checking(int)
    def left(step=1):
        if step > 30:
            step = 30
            #print("参数值超过设置上限，默认运行最大上限次数 ", step)
        Rb.left(step)

    @staticmethod
    @parameter_checking(int)
    def right(step=1):
        if step > 30:
            step = 30
            #print("参数值超过设置上限，默认运行最大上限次数 ", step)
        Rb.right(step)

    @staticmethod
    @parameter_checking(int)
    def left_slide(step=1):
        if step > 30:
            step = 30
            #print("参数值超过设置上限，默认运行最大上限次数 ", step)
        Rb.left_slide(step)

    @staticmethod
    @parameter_checking(int)
    def right_slide(step=1):
        if step > 30:
            step = 30
            #print("参数值超过设置上限，默认运行最大上限次数 ", step)
        Rb.right_slide(step)

    @staticmethod
    @parameter_checking(int)
    def forward(step=1):
        if step > 30:
            step = 30
            #print("参数值超过设置上限，默认运行最大上限次数 ", step)
        Rb.forward(step)

    @staticmethod
    @parameter_checking(int)
    def backward(step=1):
        if step > 30:
            step = 30
            #print("参数值超过设置上限，默认运行最大上限次数 ", step)
        Rb.backward(step)

    @staticmethod
    @parameter_checking(int)
    def up(step=1):
        if step > 1:
            step = 1
            #print("参数值超过设置上限，默认运行最大上限次数 1")
        Rb.up(step)

    @staticmethod
    @parameter_checking(int)
    def down(step=1):
        if step > 1:
            step = 1
            #print("参数值超过设置上限，默认运行最大上限次数 1")
        Rb.down(step)

    @staticmethod
    @parameter_checking(int)
    def check(step=1):
        if step > 1:
            step = 1
            #print("参数值超过设置上限，默认运行最大上限次数 1")
        Rb.check(step)

    # @staticmethod
    # def circle(step, radius):
    #     step = 10 if step > 10 else step
    #     Rb.circle(step, radius)

    @staticmethod
    @parameter_checking(int)
    def nod(step=1):
        if step > 30:
            step = 30
            #print("参数值超过设置上限，默认运行最大上限次数 ", step)
        Rb.nod(step)

    @staticmethod
    @parameter_checking(int)
    def shaking_head(step=1):
        if step > 30:
            step = 30
            #print("参数值超过设置上限，默认运行最大上限次数 ", step)
        Rb.shaking_head(step)

    '''虚不实真，苦切一除能，咒等等无是，咒上无是，咒明大是'''

    @staticmethod
    def jiangnanstyle():
        Sh.jiangnanstyle()


    @staticmethod
    def smallapple():
        Sh.smallapple()

    @staticmethod
    def lasong():
        Sh.lasong()

    @staticmethod
    def feelgood():
        Sh.feelgood()

    @staticmethod
    def fantastic_baby():
        Sh.fantastic_baby()

    @staticmethod
    def super_champion():
        Sh.super_champion()

    @staticmethod
    def youth_cultivation():
        Sh.youth_cultivation()

    @staticmethod
    def love_starts():
        Sh.love_starts()

    @staticmethod
    def push_up():
        Rb.push_up()

    @staticmethod
    def abdominal_curl():
        Rb.abdominal_curl()

    @staticmethod
    def wave():
        Rb.wave()

    @staticmethod
    def bow():
        Rb.bow()

    @staticmethod
    def spread_wings():
        Rb.spread_wings()

    @staticmethod
    def straight_boxing():
        Rb.straight_boxing()

    @staticmethod
    def lower_hook_combo():
        Rb.lower_hook_combo()

    @staticmethod
    def left_hook():
        Rb.left_hook()

    @staticmethod
    def right_hook():
        Rb.right_hook()

    @staticmethod
    def punching():
        Rb.punching()

    @staticmethod
    def crouching():
        Rb.crouching()

    @staticmethod
    def yongchun():
        Rb.yongchun()

    @staticmethod
    def beat_chest():
        Rb.beat_chest()

    @staticmethod
    def left_side_kick():
        Rb.left_side_kick()

    @staticmethod
    def right_side_kick():
        Rb.right_side_kick()

    @staticmethod
    def left_foot_shot():
        Rb.left_foot_shot()

    @staticmethod
    def right_foot_shot():
        Rb.right_foot_shot()

    @staticmethod
    def show_poss():
        Rb.show_poss()

    @staticmethod
    def inverted_standing():
        Rb.inverted_standing()

    @staticmethod
    def rear_stand_up():
        Rb.rear_stand_up()



