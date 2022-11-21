# coding=utf-8
from __future__ import print_function

from naoqi import ALProxy
# from translate import Translator
import numpy as np
from utilities.Utils import ConfigFile, PythonBridge, text_to_dict, lang_supported, convert_value_range
from termcolor import colored


class Attention:
    """ Class implementation of Attention module in Gross' Modal Model.
    Through inner voice the robot focuses its attention on
    particular aspects situation, and possibly search for others by calling up the Situation module again.
    He chooses which particular aspects of the situation. It is responsible for the attribution
    of meaning to situations and for generating the appraisal variables through the Inner Voice mechanism.
    May request new insights from the Situation module.
    """

    # Max and Min values for mid appraisal variables in Valence
    MAX_C = 3
    MIN_C = -3
    MAX_D = 1
    MIN_D = -1
    MAX_T = 1
    MIN_T = 0
    MAX_Ch = 3
    MIN_Ch = 0
    MAX_G = MAX_T + MAX_D + MAX_C + 8
    MIN_G = -MAX_G * 0.2

    # Max and Min values for mid appraisal variables in Arousal
    MAX_B = 1
    MIN_B = 0
    MAX_Te = 0
    MIN_Te = -3

    items = text_to_dict('./InnerVoice/resources/points.txt')
    wine = np.array(items['Wine'])
    fork = np.array(items['Appetizer Fork'])

    def __init__(self, range=None):
        """Constructor method.

        :param range: Valence and Arousal range values
        :type range: list
        """
        config = ConfigFile('configfile.ini')
        self.ip = config.get_ipaddress()
        self.port = config.get_port()
        self.url = config.get_url()
        self.lang = config.get_lang()
        self.valence = self.arousal = 0.0
        self.range = range
        self.convert = True
        if range is None:
            self.range = [-1, 1]
            self.convert = False
        self.CLARION = PythonBridge(3.8, file='CLARION', module='cognitive')

    def __gradient(self, item, state, occupied):
        """
        Evaluate gradient function g.

        :param item: Item currently moved in simulation
        :type item: basestring
        :param state: Current state of simulation
        :type state: dict
        :param occupied: Current items occupied in simulation
        :type occupied: dict
        :return: Gradient value
        :rtype: float
        """

        rho = np.linalg.norm(self.wine - self.fork)
        current_position = np.array(self.items[occupied[item]])
        real_position = np.array(self.items[item])
        delta = np.linalg.norm(real_position - current_position)

        if str(state[item][1]) == 'YES':
            gradient = self.MAX_G
        else:
            gradient = ((rho / 2) - (1.2 * delta)) / rho
            # gradient = - self.MAX_G * delta * 0.2

        return gradient

    def __recovery(self, item, state):
        """
        Evaluate recovery function T.

        :param item: Item currently moved in simulation
        :type item: basestring
        :param state: Current state of simulation
        :type state: dict
        :return: Recovery value
        :rtype: int
        """
        recovery = int(state[item][2])

        return recovery

    def __changeability(self, state, likelihood):
        """
        Evaluate changeability function ch.

        :param state: Current state of simulation
        :type state: dict
        :param likelihood: Likelihood value from previous step
        :type likelihood: float
        :return: Changeability value and likelihood variation
        :rtype: float, float
        """
        beta = gamma = 0
        expression = state['Human'][0]
        vocal = state['Human'][1]
        noise = state['Noise']
        current_likelihood = state['Likelihood']

        if expression in ['anger', 'sorrow']:
            beta = -1
        elif expression in ['joy', 'laughter', 'excitement', 'surprise']:
            beta = 1
        if vocal in ['anger', 'sorrow']:
            gamma = -1
        elif vocal in ['joy', 'laughter']:
            gamma = 1

        K = beta + gamma - noise
        x = abs(current_likelihood - likelihood)
        print("K = " + str(K))
        K = abs(K)
        #x = current_likelihood - likelihood
        print("X = " + str(x))
        print("L_p = " + str(current_likelihood))
        print("L_a = " + str(likelihood))

        if x == 0:
            x = current_likelihood
        changeability = K * x

        return changeability, x

    def __controllability(self, state, likelihood):
        """
        Evaluate controllability function c.

        :param state: Current state of simulation
        :type state: dict
        :param likelihood: Likelihood value from previous step
        :type likelihood: float
        :return: Controllability value
        :rtype: float
        """
        Ch, x = self.__changeability(state, likelihood)
        new_value_ch = convert_value_range(Ch, [self.MIN_Ch, self.MAX_Ch], self.range)

        if x == 0:
            controllability = 0.0
        else:
            controllability = - (1 / Ch) + (x ** 2)
            if controllability < self.MIN_C:
                controllability = self.MIN_C

        return controllability

    def __desirability(self, item, state):
        """
        Evaluate desirability function c.

        :param item: Item currently moved in simulation
        :type item: basestring
        :param state: Current state of simulation
        :type state: dict
        :return: Desirability value
        :rtype: int
        """
        desiderability = -1
        """if state[item][0] == 'User':
            desiderability = 0"""
        if state[item][1] == 'YES':
            desiderability = 1

        return desiderability

    def get_valence(self):
        """Returns valence parameter.

        :returns: Parameter valence
        :rtype: float"""
        return self.valence

    def get_arousal(self):
        """Returns arousal parameter.

        :returns: Parameter arousal
        :rtype: float"""
        return self.arousal

    def eval_valence(self, item, current_state, occupied, likelihood):
        """Evaluate Valence variable based on input state from simulation

        :param item: Item currently moved in simulation
        :type item: basestring
        :param current_state: Current state of simulation
        :type current_state: dict
        :param occupied: Current occupied items in simulation
        :type occupied: dict
        :param likelihood: Likelihood value from previous step
        :type likelihood: float
        :return: Evaluated Valence value
        :rtype: float
        """
        max_valence = self.MAX_C + self.MAX_T + self.MAX_D + self.MAX_G - self.MAX_Ch
        min_valence = (self.MIN_C + self.MIN_T + self.MIN_D + self.MIN_G - self.MIN_Ch)

        #max_valence = self.MAX_C + self.MAX_D - self.MAX_Ch
        #min_valence = (self.MIN_C + self.MIN_D - self.MIN_Ch) - 1

        g_delta = self.__gradient(item, current_state, occupied)
        T = self.__recovery(item, current_state)
        Ch, _ = self.__changeability(current_state, likelihood)
        c = self.__controllability(current_state, likelihood)
        d = self.__desirability(item, current_state)

        # Evaluate valence for use case test
        valence = g_delta + T + c + d - Ch

        # Evaluate valence for simulation tests
        #valence = c + d - Ch

        self.valence = convert_value_range(valence, [min_valence, max_valence], self.range)

        return self.valence

    def eval_arousal(self, current_state):
        """Evaluate Arousal variable as weighted average of input parameters

        :param current_state: Current state of simulation
        :type current_state: dict
        :return: Evaluated Arousal value
        :rtype: float
        """
        max_arousal = self.MAX_B - self.MAX_Te
        min_arousal = self.MIN_B + self.MIN_Te

        battery = current_state['Robot'][0]
        temperature = current_state['Robot'][1]
        arousal = battery - temperature
        self.arousal = convert_value_range(arousal, [min_arousal, max_arousal], self.range)

        return self.arousal

    def inner_speak(self, line):
        """Enable Robot to speak line passed in parameter.

        :param line: Line spoken by robot
        :type line: basestring
        """
        try:
            tts = ALProxy('ALTextToSpeech', self.ip, self.port)
            tts.setParameter('speed', 60)
            tts.setVolume(0.8)
            tts.setLanguage(lang_supported.get(self.lang))
            # line = self.translator.translate(line)
            tts.say(line.encode('utf-8'))
        except Exception as e:
            raise Exception(e)

    def innerquery(self):
        pass
