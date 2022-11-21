# coding=utf-8
from sys import argv
import xml.etree.ElementTree as ET

from module.Situation import Situation
from module.Attention import Attention
from module.Appraisal import Appraisal
from module.Response import Response

phase = None


def execute_loop(item, state=None, occupied=None, help=False, previuos_likelihood=0.0):
    # def execute_loop(item, state=None, previous_likelihood=0.0):
    """Execute one circle loop of Gross' Modal Model.
    Based on currently state of simulation, evaluate Robot's state and emotion,
    helped by Inner Speech.

    :param item: Current object moved in simulation
    :type item: basestring
    :param state: Current State of Simulation
    :type state: dict
    :param previous_likelihood: Likelihood value of previous step in simulation
    :type previous_likelihood: float
    """

    if item is None:
        raise ValueError("Required item for execute modal model loop! None received!")
    if state is None:
        state = {}
    elif type(state) is not dict:
        raise ValueError('Expected state as a dict! {} receive instead!'.format(type(state)))

    if occupied is None:
        occupied = {}
    elif type(occupied) is not dict:
        raise ValueError('Expected occupied as a dict! {} receive instead!'.format(type(occupied)))

    if not state:
        return

    situation = Situation(state, occupied)
    attention = Attention(range=[0, 5])
    #attention = Attention()

    """report_on = item
    while report_on is not None:
         report_on = attention.innerquery()
         return report_on"""

    battery = situation.battery_state()
    temperature = situation.body_state()

    arousal = attention.eval_arousal(state)
    #valence = attention.eval_valence(item, state, occupied, 0.0)
    valence = attention.eval_valence(item, state, {}, previous_likelihood)
    print("Valenza: {} Arousal: {}".format(valence, arousal))
    belief = [valence, arousal]

    appraisal = Appraisal(new_range=[0, 5])
    #appraisal = Appraisal()
    emotion, intensity = appraisal.evaluate(belief, phase)
    #appraisal.plot_emotion(belief, emotion)

    response = Response()
    line = response.print_emotion(emotion, intensity)

    return line


def extract_data_test(phase):
    """
    Extract simulation data from log filename and initialize
    state variable with item currently moved.

    :param phase: XML Element for current test phase
    :type phase: xml.etree.ElementTree.Element
    :return: The current moved item and state of simulation
    :rtype: basestring, dict, float
    """
    state = {}
    occupied = {}

    name = phase.get('name')
    # print("--- Extracting data from " + name)
    state['Robot'] = [float(phase.find('battery').text), int(phase.find('temperature').text)]
    state['Noise'] = float(phase.find('noise').text)
    human = phase.find('human')
    state['Human'] = [human.find('expression').text, human.find('vocal').text]
    state['Likelihood'] = float(phase.find('likelihood').text)

    item = phase.find('item')
    item_name = item.get('name')
    state, occupied = extract_data_item(item, state, occupied)

    table = phase.find('table')
    if table is not None:
        for item_table in table.findall('item'):
            state, occupied = extract_data_item(item_table, state, occupied)
    # print("--- Operation complete!")

    return item_name, state, occupied


def extract_data_item(item, state, occupied):
    """
    Extract data for current item in simulation

    :param item: XML Element for current item
    :type item: xml.etree.ElementTree.Element
    :param state: State of simulation to be updated
    :type state: dict
    :param occupied: Current items in simulation
    :type occupied: dict
    :return: The updated state variable
    :rtype: dict
    """
    item_name = item.get('name')
    if item.find('position').text == item_name:
        is_item_ok = 'YES'
    else:
        is_item_ok = 'NO'
    state[item_name] = [item.find('subject').text, is_item_ok, int(item.find('move').text)]
    occupied[item_name] = item.find('position').text

    return state, occupied


if __name__ == "__main__":
    xml_log = ET.parse('Loss_log_tests.xml')
    simulation = xml_log.getroot()
    tests = []
    previous_likelihood = 0.0

    for test in simulation.findall('test'):
        phase = test.get('name')
        print("\nEvaluate experiment for {} test".format(phase))
        item, state, occupied = extract_data_test(test)
        execute_loop(item, state, occupied, previous_likelihood)
        #execute_loop(item, state, occupied)
        previous_likelihood = state['Likelihood']
