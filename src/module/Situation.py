# coding=utf-8
from utilities.Utils import ConfigFile
from NaoQi.API import SensorsLed


class Situation:
    """ Class implementation of Situation module in Gross' Modal Model.
    It's responsible for collecting external data through the robot's outer ear
    and the inner ear (through the inner voice the robot listens to itself) in order to identify the situation
    the robot has to deal with. The channel of perceptions are passed
    input to this class.
    """

    def __init__(self, state, occupied):
        """Constructor method.

        :param state: Current State of Simulation
        :type state: dict
        :param occupied: Item's position in Simulation
        :type occupied: dict
        """
        config = ConfigFile('configfile.ini')
        self.ip = config.get_ipaddress()
        self.port = config.get_port()
        self.url = config.get_url()
        self.state = state
        self.occupied = occupied
        # self.items = text_to_dict('../InnerVoice/resources/points.txt')

    def get_item_state(self, item):
        """Return current state of item in table.

        :param item: The item to be analyzed
        :type item: basestring
        :returns: Item's current state. None if item is not present
        :rtype: list, None
        """
        return self.state[item]

    def get_item_position(self, item):
        """Return current position of item in table.

        :param item: The item to be analyzed
        :type item: basestring
        :returns: Item's point in table. None if item is not present
        :rtype: list, None
        """
        for key, value in self.occupied.items():
            if value[0] == item:
                return value
        return None

    def num_pieces(self):
        """Return state number of pieces in table simulation

        :returns: State number of pieces in table
        :rtype: tuple
        """
        wrong = 0
        for key, value in self.state.items():
            if value[1] == 'NO':
                wrong = wrong + 1
        return {'YES': len(self.state) - wrong, 'NO': wrong}

    def battery_state(self): # Restituisce un intero tra 0 e 100 (percentuale)
        """Return robot's current battery level

        :returns: Level battery
        :rtype: int
        """
        try:
            battery = SensorsLed.ALBattery()
            return battery.getBatteryCharge()
        except Exception as e:
            raise Exception(e)

    def body_state(self):
        """Return robot's current body temperature

        :returns: Level temperature. 0 (NEGLIGIBLE), 1 (SERIOUS), 2 (CRITICAL)
        :rtype: int
        """
        try:
            temperature = SensorsLed.ALBodyTemperature()
            level = temperature.getTemperatureDiagnosis()
            if level is not None:
                return level.keys()[0]
            return level
        except Exception as e:
            raise Exception(e)
