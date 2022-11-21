# coding=utf-8
"""Support file for global paramaters shared by simulation and modal model blocks"""

# Global variables
state = {}
occupied = {}
backup_state = {}
backup_occupied = {}


def execute_backup_state():
    """Save current state dict in backup variable"""
    global backup_state
    backup_state = state


def execute_backup_occupied():
    """Save current occupied dict in backup variable"""
    global backup_occupied
    backup_occupied = occupied


def add_to_state(key, value):
    """Add a tuple [key, value] in state dict

    :param key: Key to be add
    :type key: basestring
    :param value: Value to be add
    :type: any
    """
    state[key] = value


def remove_from_state(key):
    """Remove a key from state.

    :param key: Key to be removed
    :type key: basestring
    """
    del state[key]


def add_to_occupied(key, value):
    """Add a tuple [key, value] in occupied dict

    :param key: Key to be add
    :type key: basestring
    :param value: Value to be add
    :type: any
    """
    occupied[key] = value


def remove_from_occupied(key):
    """Remove a key from occupied.

    :param key: Key to be removed
    :type key: basestring
    """
    del occupied[key]
