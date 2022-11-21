# coding=utf-8
from __future__ import print_function
from utilities.Utils import PythonBridge


class Knowledge:
    """ Class implementation of robot's base knowledge.
    This class uses the basic knowledge of the robot to make reasoning about the current state of the situation.
    It is used to extract new information through inner voice.
    """

    def __init__(self):
        """Constructor method
        """
        self.bridge = PythonBridge(version=2.7)

    def call_method(self):
        result = self.bridge.call_class_method(self.__class__.__name__, 'print_hello', ['Pepper'])
        result = self.bridge.call_method('print_stat', ['Pepper'])
        result = self.bridge.call_instance_method(self.__class__.__name__, 'call_hello', ['Pepper'])
        print("Ecco il risultato: " + result)
