# coding=utf-8
import random
from threading import Thread

from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QIcon
from random import shuffle

import numpy as np
from sys import float_info, exit

from utilities.Utils import PythonBridge, text_to_dict
from utilities.global_params import *
from model import execute_loop


# Global variables
list_obj = text_to_dict('./resources/points.txt')
all_items = list_obj
items = {}
centers = {}
item_under = None
item_over = None


def call_to_help():
    # pepper_bridge = PythonBridge(version=2.7, file='model')
    # print("Model says: " + str(pepper_bridge.call_method('execute_loop', [state, occupied, True])))
    missing = []
    pieces = []
    for value in occupied.values():
        pieces.append(value[0])
    for key in all_items.keys():
        if key in pieces:
            continue
        missing.append(key)
    if not missing:
        print("I have no pieces to move!")
        return
    rand_index = random.randint(0, len(missing) - 1)
    label_choice = missing[rand_index]
    if label_choice in occupied.keys():
        # Potrebbe in questo caso scambiare i pezzi prima di spostarli
        print("I can't move that piece! His seat is taken!")
    items[label_choice].move_to_closer_point(False)


def stop_simulation():
    # last_bridge = PythonBridge(version=2.7, file='model')
    # print("Model says: " + str(last_bridge.call_method('execute_loop', [state, occupied])))
    exit('You stopped the simulation!')


class DraggableItem(QLabel):
    """Extended class from PyQt5.QtWidgets.QLabel. This class provide a Draggable QLabel that represents
    dish item in table. User can drag and drop an item in table, setting it's position"""

    def __init__(self, parent, label, image, startPoint, finalPoint):
        """Constructor method.

        :param parent: PyQt5 QWidget parent that contain the item
        :type parent: QWidget
        :param label: Item name
        :type label: basestring
        :param image: Path for item's image file
        :type image: basestring
        :param startPoint: Item's initial position in table
        :type startPoint: QPoint
        :param finalPoint: Item's real and final position in table
        :type finalPoint: QPoint
        """
        super(QLabel, self).__init__(parent)
        self.thread = None
        self.mousePressPos = self.mouseMovePos = None
        self.startPosition = startPoint
        self.finalPosition = finalPoint
        self.currentPosition = QPoint(self.x(), self.y())
        self.label = label
        self.trad = label
        self.pixmap = QPixmap(image)

        self.attempt = 2
        self.blocked = False

        self.change_into_text()
        self.move(startPoint)

    def change_into_image(self):
        """Change label into image label
        """
        self.setPixmap(self.pixmap)
        self.setFixedHeight(self.pixmap.height())
        self.setFixedWidth(self.pixmap.width())
        self.setStyleSheet("""
                            background-color: transparent;
                        """)

    def change_into_text(self):
        """Change label into label with text
        """
        self.setText("      " + self.trad)
        self.setFixedHeight(30)
        self.setFixedWidth(180)
        self.setStyleSheet("""
                            background-color: white;
                        """)

    def erase(self):
        """Remove previous occupied position from item and it's state in table
        """
        global item_under
        global item_over
        if item_under == self.label:
            item_under = None
        elif item_over == self.label:
            item_over = None
        for key, value in occupied.items():
            if value[0] == self.label:
                remove_from_state(self.label)
                remove_from_occupied(key)
                return

    def mousePressEvent(self, event):
        if self.attempt == 0:
            self.blocked = True
            return
        if event.button() == Qt.LeftButton:
            self.mousePressPos = event.globalPos()
            self.mouseMovePos = event.globalPos()
            if self.attempt == 1:
                self.erase()

        super(DraggableItem, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.blocked:
            return
        if event.buttons() == Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            # Enable movement in widget dimension parent
            parent_w = self.parent().width()
            obj_w = self.width()
            if newPos.x() in range(0, parent_w + obj_w):
                self.move(newPos)
                self.mouseMovePos = globalPos
                self.currentPosition = QPoint(self.x(), self.y())
                if self.x() in range(400 - obj_w, parent_w + obj_w):
                    self.change_into_image()
                else:
                    self.change_into_text()
                global item_under
                global item_over
                if item_under is not None and item_over is None:
                    items[item_under].stackUnder(self)
                elif item_under is not None and item_over is not None:
                    items[item_under].stackUnder(items[item_over])
                    items[item_over].stackUnder(self)

        super(DraggableItem, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.blocked:
            return
        if self.mousePressPos is not None:
            xPos = self.currentPosition.x()
            if xPos in range(0, 400 - self.width()):
                self.move(self.startPosition)
                self.erase()
                self.change_into_text()
            else:
                self.move_to_closer_point()

        # Start Model Cycle
        self.thread = Thread(target=execute_loop, args=(self.label, state, occupied))
        self.thread.start()

        super(DraggableItem, self).mouseReleaseEvent(event)

    def move_to_closer_point(self, user=True):
        """Move item into currently closer point. The closer position will be occupied from item.
        The item state will be update.

        :param user: If the user is moving pieces or it's the robot
        :type user: bool
        """
        curr_key = None
        curr_value = None
        xPos = (self.pixmap.width() // 2)
        yPos = (self.pixmap.height() // 2)
        who = 'User'
        set_plates = ['Plate', 'Appetizer Plate']

        # Pepper is moving piece
        if not user:
            who = 'Pepper'
            self.change_into_image()
            add_to_state(self.label, [who, 'YES', 0])
            self.currentPosition = self.finalPosition
            self.move(self.finalPosition)
            curr_key = self.label
        else:
            obj_point = [self.currentPosition.x() + xPos, self.currentPosition.y() + yPos]
            min_dist = float_info.max
            for dish, point in list_obj.items():
                center = [centers[dish].x(), centers[dish].y()]
                curr = np.linalg.norm(np.array(center) - np.array(obj_point))
                if curr < min_dist:
                    min_dist = curr
                    curr_key = dish
                    curr_value = center
        # Check if closer point is occupied and move to piece's start position
        global item_under
        global item_over
        if (curr_key in occupied.keys() and curr_key not in set_plates) or \
                (curr_key in set_plates and item_under is not None and item_over is not None):
            self.change_into_text()
            self.move(self.startPosition)
            return

        # Reduce attempt
        self.attempt = self.attempt - 1

        if (item_under == 'Plate' and self.label == 'Appetizer Plate' and
                curr_key in set_plates) or \
                (item_under is None and self.label == 'Plate' and
                 curr_key in set_plates) or (curr_key == self.label and self.label not in set_plates):
            #add_to_state(self.label, [who, 'YES', self.attempt])
            add_to_state(self.label, [who, 'YES', self.attempt, list_obj[curr_key]])
            self.currentPosition = self.finalPosition
            self.move(self.finalPosition)
        else:
            add_to_state(self.label, [who, 'NO', self.attempt, list_obj[curr_key]])
            self.currentPosition = QPoint(curr_value[0] - xPos, curr_value[1] - yPos)
            self.move(self.currentPosition)

        # Add occupied position
        if curr_key in set_plates and 'Plate' in occupied.keys():
            add_to_occupied(self.label, 'Appetizer Plate')
        elif curr_key in set_plates and 'Appetizer Plate' in occupied.keys():
            add_to_occupied(self.label, 'Plate')
        else:
            #add_to_occupied(curr_key, [self.label, list_obj[curr_key]])
            add_to_occupied(self.label, curr_key)

        if curr_key in set_plates and item_under is None:
            item_under = self.label
        elif curr_key in set_plates and item_under is not None:
            items[item_under].stackUnder(self)
            item_over = self.label


class Table(QWidget):
    """Extended class for PyQt5.QtWidgets.QWidget that represent Table in simulation.
    """

    def __init__(self):
        super(Table, self).__init__()
        self.setFixedSize(1200, 600)

        container = QWidget()
        container.setAttribute(Qt.WA_TransparentForMouseEvents)
        container.setStyleSheet("""
                background-image: url('./resources/images/tablecloth_empty.jpg')
            """)
        box = QHBoxLayout(self)
        box.setContentsMargins(0, 0, 0, 0)
        box.addWidget(container)
        container.raise_()


if __name__ == "__main__":
    app = QApplication([])
    window = QWidget()

    table = Table()
    layout = QHBoxLayout()
    layout.addWidget(table)
    window.setFixedSize(1200, 620)
    window.setLayout(layout)
    title = 'Help Pepper to setting up the table!'
    window.setWindowTitle(title)
    window.setGeometry(500, 300, 1200, 600)

    # Shuffle starting item table
    temp_list = list(list_obj.items())
    shuffle(temp_list)
    list_obj = dict(temp_list)

    # Initialize Dish items and add to table
    step = 15
    for label, point in list_obj.items():
        start_point = QPoint(20, step)
        end_point = QPoint(point[0], point[1])
        image = './resources/images/' + label + '.png'
        dish = DraggableItem(table, label, image, start_point, end_point)
        items[label] = dish
        pixmap = QPixmap(image)
        centers[label] = QPoint(point[0] + (pixmap.width() // 2), point[1] + (pixmap.height() // 2))
        step = step + 45

    # Set Help Button
    help_btn = QPushButton(table)
    help_btn.setGeometry(220, 200, 150, 50)
    help_btn_text = '  Ask for help'
    help_btn.setText(help_btn_text)
    help_btn.clicked.connect(call_to_help)
    help_btn.setIcon(QIcon('./resources/images/pepper_icon.png'))

    # Set stop simulation button
    stop_btn = QPushButton(table)
    stop_btn.setGeometry(220, 300, 150, 50)
    stop_btn_text = '  Stop'
    stop_btn.setText(stop_btn_text)
    stop_btn.clicked.connect(stop_simulation)
    stop_btn.setIcon(QIcon('./resources/images/stop_icon.png'))

    window.show()
    app.exec_()
