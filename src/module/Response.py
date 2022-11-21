# coding=utf-8
from time import sleep

from utilities.Utils import ConfigFile, lang_supported
from NaoQi.API import Audio, Core, address


class Response:
    """Class implementation of Response Module in Gross' Modal Model.
    This class implements the coping strategies basing on the
    emotion generated. The only coping strategy considered at this time is
    to outsource the emotion and its intensity.
    """

    def __init__(self):
        """Constructor method.
        """
        config = ConfigFile('configfile.ini')
        self.ip = config.get_ipaddress()
        self.port = config.get_port()
        self.url = config.get_url()
        self.lang = config.get_lang()

    def show_emotion(self, emotion):
        """Show evaluated emotion on Pepper's tablet.

        :param emotion: emotion evaluated by Appraisal model
        :type emotion: basestring
        :raises Exception: exception raised when the Robot's session could not start
        (unable to connect with Robot)
        """
        try:
            tabletService = Core.ALTabletService()
            tabletService.showImage("http://{}/apps/aldebaran/{}_title.png".format(address, emotion))
            sleep(1)
            tabletService.hideImage()
        except Exception as ex:
            print(ex)

    def speak(self, line):
        """Enable Robot to speak line passed in parameter.

        :param line: Line spoken by robot
        :type line: basestring
        """
        try:
            tts = Audio.ALTextToSpeech()
            tts.setParameter('speed', 60)
            tts.setVolume(0.8)
            tts.setLanguage(lang_supported.get(self.lang))
            #line = self.translator.translate(line)
            tts.say(str(line.encode('utf-8')))
        except Exception as e:
            raise Exception(e)

    def say_emotion(self, emotion, intensity):
        """Communication of emotion evaluated through Pepper's voice.

        :param emotion: emotion evaluated by Appraisal module
        :type emotion: basestring
        :param intensity: intensity level of emotion
        :type intensity: basestring
        :raises Exception: exception raised when the Robot's session could not start
        (unable to connect with Robot)
        """
        try:
            tts = ALProxy("ALTextToSpeech", self.ip, self.port)
            tts.setParameter('speed', 60)
            tts.setVolume(0.8)
            tts.setLanguage(lang_supported.get(self.lang))
            if emotion is None:
                return
            if intensity is not None:
                line = "Sono " + intensity + " " + emotion + "!"
                #line = self.translator.translate("Sono " + intensity + " " + emotion + "!")
            else:
                line = "Sono " + emotion + "!"
                #line = self.translator.translate("Sono " + emotion + "!")
            tts.say(line.encode('utf-8'))
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def print_emotion(emotion, intensity):
        """Communication of emotion evaluated through terminal video.

        :param emotion: emotion evaluated by Appraisal module
        :type emotion: basestring
        :param intensity: intensity level of emotion
        :type intensity: basestring
        :return: Robot's speak line
        :rtype: basestring
        """
        try:
            if emotion is None:
                return
            elif intensity is not None:
                line = "Sono " + intensity + " " + emotion + "!"
                #line = self.translator.translate("Sono " + intensity + " " + emotion + "!")
            else:
                line = "Sono " + emotion + "!"
                #line = self.translator.translate("Sono " + emotion + "!")
            print(line)
            return line
        except Exception as e:
            raise Exception(e)
