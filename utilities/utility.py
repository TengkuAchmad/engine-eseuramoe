# LIBRARIES
from flask import Flask
from flask import Blueprint
from flask import request
from flask import jsonify
from flask_cors import CORS
import cv2
import csv
import numpy as np
import tensorflow as tf
import requests
import os
import joblib
import json

# GLOBAL VARIABLES
class_names = [
    'ab 9', 'ab 7', 'SU 21', 'SU 26', 'SU 19', 'SU 10', 'SU 17', 'SU 28',
    'ab 6', 'ab 1', 'ab 8', 'SU 16', 'SU 29', 'SU 11', 'SU 27', 'SU 18',
    'SU 20', 'SU 5', 'SU 2', 'Nr 28', 'SU 4', 'Nr 11', 'nr 29', 'Nr 16',
    'nr 18', 'ab 11', 'ab 29', 'ab 16', 'ab 20', 'ab 18', 'ab 27', 'ab 19',
    'ab 26', 'ab 21', 'ab 28', 'ab 17', 'ab 10', 'nr 23 v2', 'SU 25',
    'SU 22', 'SU 14', 'SU 13', 'ab 4', 'ab 3', 'SU 12', 'SU 15', 'SU 23',
    'SU 24', 'ab 2', 'ab 5', 'Nr 25', 'nr 13', 'nr 14', 'SU 1', 'SU 6',
    'SU 8', 'nr 15', 'Nr 12', 'ab 30', 'nr 24', 'SU 9', 'as', 'SU 7',
    'Nr 9', 'ab 15', 'ab 12', 'ab 24', 'ab 23', 'Nr 6', 'nr 8', 'nr -',
    'ab 22', 'ab 25', 'ab 13', 'ab 14', 'SU 30'
]


# CONTROLLERS
from controllers import enginerapid

from controllers import enginelab

# BLUEPRINTS
from routes.engineroute import engine_blueprint