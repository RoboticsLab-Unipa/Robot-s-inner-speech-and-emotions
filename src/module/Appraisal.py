# coding=utf-8
from __future__ import print_function
from __future__ import division

import pandas as pd
import numpy as np
from sys import float_info
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from xml.dom import minidom

from utilities.Utils import is_valid_appraisal, convert_value_range


def generate_xml_file(filename, points):
    """
    Generate XML file with intensity points

    :param filename: Name of XML file
    :type filename: basestring
    :param points: Set of points to be write
    :type points: list
    """
    root = minidom.Document()
    xml = root.createElement('root')
    root.appendChild(xml)

    for point in points:
        label = point[0]
        intensity = point[1]
        emotionChild = root.createElement('emotion')
        emotionChild.setAttribute('name', label)

        xml.appendChild(emotionChild)
        distanceChild = root.createElement('intensity')
        distanceValue = root.createTextNode(str(intensity))
        distanceChild.appendChild(distanceValue)

        emotionChild.appendChild(distanceChild)

    xml_str = root.toprettyxml(indent="\t")
    with open(filename, "w") as f:
        f.write(xml_str)


class Appraisal:
    """Class implementation of Appraisal module in Gross' Modal Model.
    It responsible for computation of the appraisal variables according to the Russell appraisal model.
    5 Ekman primary emotions has been considered for this evaluation: Angry, Sad, Afraid, Happy and Annoyed.
    According to configurations of the appraisal values (called
    appraisal patterns), an emotion rises with a specific intensity.
    """

    def __init__(self, emotions=None,  all_emotion=False, new_range=None):
        """Constructor method.

        :param emotions: Custom columns emotion for appraisal evaluation
        :type emotions: list
        :param all_emotion: boolean value for use complete dataset Russell's emotion or only Ekman primary emotions.
                Default value False to use Ekman emotions
        :type all_emotion: bool
        :param new_range: New range of application for appraisal evaluation
        :type new_range: list
        """
        self.all_emotion = all_emotion
        self.new_range = new_range
        self.convert = True

        if new_range is None:
            self.new_range = [-1, 1]
            self.convert = False

        try:
            self.dataset = pd.read_csv('./resources/Russell_emotion_label.csv')
            self.dataset = self.dataset.set_index('Emotion')

            if self.convert:
                for label, row in self.dataset.iterrows():
                    emo_point = row.to_numpy()
                    emo_valence = convert_value_range(emo_point[0], [-1, 1], new_range)
                    emo_arousal = convert_value_range(emo_point[1], [-1, 1], new_range)
                    self.dataset.at[label, 'Valence'] = emo_valence
                    self.dataset.at[label, 'Arousal'] = emo_arousal

            if emotions is not None:
                self.emotions = emotions
            elif not all_emotion and not emotions:
                self.emotions = ['Angry', 'Sad', 'Happy', 'Afraid', 'Annoyed']
            else:
                self.emotions = list(self.dataset.index.values)

            self.data = self.dataset.loc[self.emotions]
            self.emotion = None
            self.intensity = None

        except Exception as e:
            print("Exception: {}".format(str(e)))
            exit(0)

    @property
    def emotion(self):
        return self.emotion

    @emotion.setter
    def emotion(self, emotion):
        self.emotion = emotion

    @property
    def intensity(self):
        return self.intensity

    @intensity.setter
    def intensity(self, intensity):
        self.intensity = intensity

    def __get_thresholds(self, emotion):
        """
        Calculate the maximum threshold and the minimum threshold within which to limit the intensity of the emotion.

        :param emotion: selected emotion
        :type emotion: basestring
        :return: low and high threshold for the selected emotion
        :rtype: tuple
        :raise ValueError: if emotion parameter is not string or is not a recognizable emotion
        """
        if type(emotion) is not str:
            raise ValueError("Emotion label required as a string! {} received!".format(type(emotion)))
        elif emotion not in self.emotions:
            raise ValueError("{} emotion not recognized!".format(emotion))

        emo_point = self.data.loc[emotion].to_numpy()
        low_threshold = (np.linalg.norm(emo_point - np.array([0.0, 0.0]))) / 2
        high_threshold = low_threshold / 2

        return low_threshold, high_threshold

    def evaluate(self, belief, phase=None):
        """
        Evaluate input belief and raise emotion and its intensity with euclidean distance.

        :param belief: appraisal variables to be evaluated
        :type belief: list
        :param phase: Current step in test simulation
        :type phase: basestring
        :return: the emotion evaluated and it's intensity
        :rtype: tuple
        :raise ValueError: input belief is not a valid belief (wrong appraisal pattern)
        """
        # Initial belief start. In origin
        if belief is [0.0, 0.0]:
            return None, None
        is_valid_appraisal(belief)

        valence = belief[0]
        arousal = belief[1]

        if not self.new_range[0] <= valence <= self.new_range[1]:
            raise ValueError("Valence value not in {} range! Received {} instead!".format(str(self.new_range), valence))

        if not self.new_range[0] <= arousal <= self.new_range[1]:
            raise ValueError("Arousal value not in {} range! Received {} instead!".format(str(self.new_range), arousal))

        min_dist = float_info.max
        intensity_points = []

        for index, row in self.data.iterrows():
            # Distance from belief and current emotion point
            curr = np.linalg.norm(row.to_numpy() - np.array(belief))
            intensity = None
            if self.convert:
                intensity = convert_value_range(curr, [0, self.new_range[1] + self.new_range[1]], [0, self.new_range[1]])
                intensity_points.append([index, self.new_range[1] - intensity])

            if curr < min_dist:
                min_dist = curr
                self.emotion = index

        if intensity_points:
            path_save = "intensity_emotions_" + phase + ".xml"
            generate_xml_file(path_save, intensity_points)

        # Evaluate belief intensity
        low_threshold, high_threshold = self.__get_thresholds(self.emotion)
        self.intensity = min_dist

        if min_dist <= high_threshold:
            intensity = "davvero"
        elif high_threshold < min_dist <= low_threshold:
            intensity = "molto"
        else:
            intensity = None

        return self.emotion, intensity

    def plot_emotion(self, belief=None, selected=None):
        """
        Displays the emotions and belief (if present) plot in two dimensions on the screen.
        Draws an arrow between belief and emotion (if evaluate first), otherwise plot belief in
        Russell emotion space.

        :param belief: appraisal variables to plot, default to None
        :type belief: list
        :param selected: emotion target, default to None
        :type selected: basestring
        :raise Exception: input belief is not a valid belief (wrong appraisal pattern) or selected emotion
                is not type string
        """

        label_point = 'e' + u'\u2090' + ' = ' + selected
        print(label_point)

        if belief is not None and is_valid_appraisal(belief):
            belief_df = pd.DataFrame([belief], columns=self.dataset.columns, index=[label_point])
            new_data = pd.concat([self.dataset, belief_df])
            self.emotions.append(label_point)
        elif selected is not None and type(selected) is not str:
            raise ValueError("Emotion label required as a string! {} received!".format(type(selected)))
        else:
            new_data = self.data
        colors = []

        valence = belief[0]
        arousal = belief[1]

        if not self.new_range[0] <= valence <= self.new_range[1]:
            raise ValueError("Valence value not in {} range! Received {} instead!".format(str(self.new_range), valence))

        if not self.new_range[0] <= arousal <= self.new_range[1]:
            raise ValueError("Arousal value not in {} range! Received {} instead!".format(str(self.new_range), arousal))

        if not self.all_emotion:
            colors = ['red', 'dodgerblue', 'gold', 'blueviolet', 'limegreen', 'black']

        plt.figure('Emotions and ' + label_point, figsize=[8, 8])
        # plt.xlim([self.new_range[0] - 2, self.new_range[1] + 2])
        # plt.ylim([self.new_range[0] - 2, self.new_range[1] + 2])
        plt.xlim([self.new_range[0] - 0.1, self.new_range[1] + 0.1])
        plt.ylim([self.new_range[0] - 0.1, self.new_range[1] + 0.1])
        plt.xlabel(r'$Valence\;\rightarrow$')
        plt.ylabel(r'$Arousal\longrightarrow$')
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')

        circle = plt.Circle((0, 0), radius=self.new_range[1], edgecolor='black', fill=False, linestyle='--')

        for label, i in zip(self.emotions, range(0, len(new_data))):
            x_data = new_data.loc[label]['Valence']
            y_data = new_data.loc[label]['Arousal']
            if not self.all_emotion:
                plt.scatter(x_data, y_data, marker='o', color=colors[i])
            else:
                plt.scatter(x_data, y_data, marker='o')
            if label == 'Angry':
                plt.text(x_data - .08, y_data + .03, label, fontsize=11)
            else:
                plt.text(x_data - .06, y_data - .06, label, fontsize=11)

        if selected and belief is not None:
            low_threshold, high_threshold = self.__get_thresholds(selected)
            x_center = new_data.loc[selected]['Valence']
            y_center = new_data.loc[selected]['Arousal']
            x_belief = new_data.loc[label_point]['Valence']
            y_belief = new_data.loc[label_point]['Arousal']
            circle_low = plt.Circle((x_center, y_center), radius=low_threshold, edgecolor='forestgreen', fill=False)
            circle_high = plt.Circle((x_center, y_center), radius=high_threshold, edgecolor='red', fill=False)
            # plt.text(low_threshold + .05, low_threshold, u"t\u2097", fontsize=14)
            # plt.text(x_center - high_threshold - .05, high_threshold + .05, u"t\u2095", fontsize=14)
            plt.text(x_center - low_threshold + .08, y_center - low_threshold + 0.1, u"t\u2097", fontsize=14)
            plt.text(x_center - high_threshold, y_center - high_threshold, u"t\u2095", fontsize=14)
            plt.legend([circle_high, circle_low], ['High Intensity', 'Medium Intensity'])
            arrow = ConnectionPatch((x_belief, y_belief),
                                    (x_center, y_center), 'data', 'data', arrowstyle="->", shrinkA=5, shrinkB=5,
                                    mutation_scale=20, fc="w")
            plt.gcf().gca().add_artist(arrow)
            plt.gca().add_patch(circle_low)
            plt.gca().add_patch(circle_high)
        plt.gca().add_patch(circle)
        plt.grid()
        plt.show()
