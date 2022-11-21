"""
    Definizioni di classi per la generazione di errori ed eccezioni
"""


class BeliefException(Exception):
    def __init__(self, belief):
        self.belief = belief

    def __str__(self):
        if type(self.belief) is not list:
            return "{} object received. Appraisal Belief required as list!".format(type(self.belief))
        elif not self.belief:
            return "{} empty Appraisal belief received!"
        elif len(self.belief) < 2:
            return "Received {} appraisal elements! Required only Valence and Arousal!".format(len(self.belief))
