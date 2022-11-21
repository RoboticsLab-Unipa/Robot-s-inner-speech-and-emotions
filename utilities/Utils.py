# coding=utf-8
"""Class utilities from manage common models in the entire project"""
from execnet import makegateway
from os.path import dirname, join
from configparser import ConfigParser


lang_supported = {
    'ja': 'Japanese',
    'en': 'English',
    'fr': 'French',
    'it': 'Italian',
    'de': 'German',
    'es': 'Spanish',
}


def text_to_dict(file_path):
    """Convert text file in Python dict.
    Key and value are separated from ':' character.

    :param file_path: File path to be converted
    :type file_path: basestring
    :returns: Converted dict object
    :rtype: dict
    """
    dishes = {}
    with open(file_path, 'r') as file:
        for line in file.readlines():
            key, point = line.split(':')
            xPos, yPos = point[:-1].split(",")
            dishes[key] = [int(xPos), int(yPos)]
    return dishes


def is_valid_appraisal(appraisal):
    """
    Check if the parameter function is a valid appraisal patter

    :param appraisal: Object with two index and appraisal variable
    :type appraisal: list
    :raise ValueError: exception raises of index is out of bound or parameter is not
            an iterable object (list)
    """
    try:
        iter(appraisal)
        index = len(appraisal)
        if index != 2:
            raise ValueError("Index {} out of bound. 2 allowed".format(index))
    except ValueError as ex:
        raise ValueError(ex)
    return True


def convert_value_range(value, old_range, new_range):
    """
    Convert a value in old range and transform it in new value in new range
    mantaing ratio

    :param value: Value to be converted
    :type value: float
    :param old_range: Starting old range
    :type old_range: list
    :param new_range: Final new range
    :type new_range: list
    :return: Converted value
    :rtype: float
    """
    new_value = value
    old_max = old_range[1]
    old_min = old_range[0]

    if old_min > old_max:
        raise ValueError("Range not valid! Min value {} greater than max value {}!".format(old_min, old_max))

    if value < old_min or value > old_max:
        raise ValueError("{} not in range [{}, {}]!".format(value, old_min, old_max))

    Old_Range = (old_max - old_min)
    if Old_Range == 0:
        return new_value
    else:
        new_max = new_range[1]
        new_min = new_range[0]
        New_Range = (new_max - new_min)
        new_value = (((value - old_min) * New_Range) / Old_Range) + new_min

    return new_value


class ConfigFile:
    """Handle Class for Robot's net settings config file.
        """

    def __init__(self, file_ini):
        """Constructor method.

        :param file_ini: Config file ini name
        :type file_ini: basestring
        """
        self.config = ConfigParser()

        try:
            # Open config file
            self.file_ini = file_ini
            script_dir = dirname(__file__)  # <-- absolute dir the script is in
            rel_path = "../config/" + file_ini
            abs_file_path = join(script_dir, rel_path)
            self.config.read(abs_file_path)
            self.check_parameter(file_ini)
        except Exception as ex:
            raise Exception(ex)

    def check_parameter(self, file_ini):
        """Check if all config parameter are filled.

        :param file_ini: Config file ini name
        :type file_ini: basestring
        :raise AttributeError: if a parameter in config file is missing
        """
        section = 'setting'
        parameter = ['address', 'port', 'url', 'lang']
        if file_ini == 'pythonpath.ini':
            section = 'python'
            parameter = ['PATH_2.7', 'PATH_3.8']
        try:
            self.config.has_section(section)
            for param in parameter:
                self.config.get(section, param)
        except AttributeError as ex:
            raise AttributeError(ex)

    def get_all_parameter(self):
        """Gel all parameter in config file from section.

        :return: list
        """
        section = 'setting'
        if self.file_ini == 'pythonpath.ini':
            section = 'python'
        if self.config.has_section(section):
            return self.config.items(section)

    def get_url(self):
        """Get Url config parameter.

        :return: url
        :rtype: basestring
        """
        if self.config.has_option('setting', 'url'):
            return self.config.get('setting', 'url')
        return None

    def get_ipaddress(self):
        """Get IP Address config parameter.

        :return: ip address
        :rtype: basestring"""
        if self.config.has_option('setting', 'address'):
            return self.config.get('setting', 'address')
        return None

    def get_port(self):
        """Get Port number config parameter.

        :return: port number
        :rtype: int
        """
        if self.config.has_option('setting', 'port'):
            return int(self.config.get('setting', 'port'))
        return None

    def get_lang(self):
        """Get language config parameter.

        :return: language
        :rtype: basestring
        """
        if self.config.has_option('setting', 'lang'):
            return self.config.get('setting', 'lang')
        return None

    def get_path_interpreter(self, version):
        """Get python path interpreter bases on it's version.

        :param version: python interpreter version
        :type version: float
        :rtype: basestring
        """
        if self.config.has_section('python'):
            if self.config.has_option('python', 'PATH_' + str(version)):
                return self.config.get('python', 'PATH_' + str(version))
            return None


class PythonBridge:
    """ Class implementation for build a bridge for different version of python interpreter.
        This class can instantiate class and call it's methods, call static method and execute
        script.
        """

    BASE_PATH = '../../Emobot'
    INNER_PATH = './InnerVoice'

    def __init__(self, version, file=None, module=None):
        """Constructor method.

        :param version: python interpreter version
        :type version: float
        :param module: Python module to be import
        :type module: basestring
        :param file: file in previous module to be import
        :type file: basestring
        """
        self.version = ConfigFile('pythonpath.ini').get_path_interpreter(version)
        if version == 2.7:
            self.path_dir = self.BASE_PATH
        elif version == 3.8:
            self.path_dir = self.INNER_PATH
        self.file = file
        self.module = module

    def call_method(self, function, arguments=None):
        """Method for call simple function from file imported.

        :param function: function name to be call
        :type function: basestring
        :param arguments: Set of arguments passes to class function.
        :type arguments: list
        :return: the function output or None if it not exists
        :rtype: basestring, None
        """
        if arguments is None:
            arguments = []
        elif type(arguments) is not list:
            raise ValueError('Expected argument as a list! {} receive instead!'.format(type(arguments)))
        gw = makegateway("popen//python=%s//chdir=%s" % (self.version, self.path_dir))
        if self.module is None:
            channel = gw.remote_exec("""
                                from %s import %s as the_function
                                channel.send(the_function(*channel.receive()))
                            """ % (self.file, function))
        else:
            channel = gw.remote_exec("""
                from %s.%s import %s as the_function
                channel.send(the_function(*channel.receive()))
            """ % (self.module, self.file, function))
        channel.send(arguments)
        return channel.receive()

    def call_class_method(self, class_mod, function, arguments=None):
        """Method for call @classmethod from imported class.

        :param class_mod: Class module to be import
        :type class_mod: basestring
        :param function: Class function name to be call
        :type function: basestring
        :param arguments: Set of arguments passes to class function.
        :type arguments: list
        :return: the function output or None if it not exists
        :rtype: basestring, None
        """
        if arguments is None:
            arguments = []
        elif type(arguments) is not list:
            raise ValueError('Expected argument as a list! {} receive instead!'.format(type(arguments)))
        gw = makegateway("popen//python=%s//chdir=%s" % (self.version, self.path_dir))
        channel = gw.remote_exec("""
            from %s.%s import %s as %s
            channel.send(%s.%s(*channel.receive()))
        """ % (self.module, self.file, class_mod, class_mod, class_mod, function))
        channel.send(arguments)
        return channel.receive()

    def call_instance_method(self, class_mod, function, params=None, arguments=None):
        """Method for call a class method from imported class. Create an instance of class.

        :param class_mod: Class module to be import
        :type class_mod: basestring
        :param function: Class function name to be call
        :type function: basestring
        :param params: Set of parameters passes to class instantiate.
        :type params: list
        :param arguments: Set of arguments passes to class function.
        :type arguments: list
        :return: the function output or None if it not exists
        :rtype: basestring, None
        """
        if params is None:
            params = []
        if arguments is None:
            arguments = []
        elif type(arguments) is not list:
            raise ValueError('Expected argument as a list! {} receive instead!'.format(type(arguments)))
        gw = makegateway("popen//python=%s//chdir=%s" % (self.version, self.path_dir))
        channel = gw.remote_exec("""
                    from %s.%s import %s
                    Class = %s(*channel.receive())
                    channel.send(Class.%s(*channel.receive()))
                """ % (self.module, self.file, class_mod, class_mod, function))
        channel.send(params)
        channel.send(arguments)
        return channel.receive()
