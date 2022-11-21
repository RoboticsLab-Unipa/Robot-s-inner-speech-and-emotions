# coding=utf-8
"""Python file for manage GUI Pepper interface Config file setting"""

import sys
from configparser import ConfigParser
from re import search

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.uic import loadUi

from utilities.Utils import lang_supported


def write_param_config(ip_address, port, lang):
    """Write IP Address, Port Number and Language into configfile.
    Create config file if not exists.

    :param ip_address: Robot's IP Address
    :type ip_address: basestring
    :param port: Robot's port number
    :type port: basestring
    :param lang: Language Type for Robot's conversation
    :type lang: basestring
    """
    config = ConfigParser()
    # Add the structure for ip address and port setting
    config.add_section('setting')
    config.set('setting', 'address', ip_address)
    config.set('setting', 'port', port)
    config.set('setting', 'url', 'tcp://' + ip_address + ':' + port)
    for key, value in lang_supported.items():
        if value == lang:
            config.set('setting', 'lang', key)  # Save key language

    # Write the new structure to the new file
    try:
        abs_file_path = "/home/sophy0295/PycharmProjects/Emobot/config/configfile.ini"
        with open(abs_file_path, "w") as configfile:
            config.write(configfile)
            configfile.close()
    except Exception as ex:
        raise Exception(ex)


def read_param_config():
    """Read IP Address, Port number and Language from configfile (if exists).

    :return: IP Address, Port Number and Language in robot's config file
    :rtype: tuple
    """
    config = ConfigParser()
    address = None
    port = None
    lang = None

    try:
        abs_file_path = "/home/sophy0295/PycharmProjects/Emobot/config/configfile.ini"
        config.read(abs_file_path)
        if config.has_section('setting'):
            address = config.get('setting', 'address')
            port = config.get('setting', 'port')
            key_lang = config.get('setting', 'lang')
            for key, value in lang_supported.items():
                if key == key_lang:
                    lang = value

        return address, port, lang
    except Exception as ex:
        raise Exception(ex)


class Settings(QDialog):
    def __init__(self):
        super(Settings, self).__init__()
        loadUi("/home/sophy0295/PycharmProjects/Emobot/InnerVoice/gui/pepper.ui", self)
        self.lang.addItems(list(lang_supported.values()))

        init_address, init_port, init_lang = read_param_config()
        if init_address is None and init_port is None:
            self.address.setPlaceholderText("Enter IP Address...")
            self.port.setPlaceholderText("Enter Port Number...")
            self.lang.setCurrentIndex(list(lang_supported.values()).index('English'))
        else:
            self.address.setText(init_address)
            self.port.setText(init_port)
            self.lang.setCurrentIndex(list(lang_supported.values()).index(init_lang))

        self.savebutton.clicked.connect(self.update_settings)

    def update_settings(self):
        message = QMessageBox()
        message.setWindowTitle("Update Settings")

        ip_address = self.address.text()
        port = self.port.text()
        lang = self.lang.currentText()
        regex = r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[" \
                r"0-9])|localhost$"

        if not search(regex, ip_address) or not port.isnumeric():
            message.setText("Invalid IP Address or Port!")
            message.setIcon(QMessageBox.Warning)
            message.setStandardButtons(QMessageBox.Retry)
            message.exec_()
            return

        write_param_config(ip_address, port, lang)

        message.setText("Settings successfully updated!")
        message.setIcon(QMessageBox.Information)
        message.setStandardButtons(QMessageBox.Ok)
        message.exec_()

        self.address.setText(ip_address)
        self.port.setText(port)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Settings()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(main_window)
    widget.setFixedWidth(400)
    widget.setFixedHeight(391)
    widget.setGeometry(800, 300, 400, 391)
    widget.show()
    sys.exit(app.exec_())
