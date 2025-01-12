# LIBRARIES
from flask import Flask
from flask import Blueprint
from flask import request
from flask import jsonify
from flask_cors import CORS
import cv2
import numpy as np
import tensorflow as tf
import requests
import os

# GLOBAL VARIABLES
class_names = ['SU 11', 'SU 10', 'SU 1', 'Nr 9', 'nr 8', 'Nr 6', 'nr 29', 'Nr 28', 'Nr 25', 'nr 24', 'nr 23 v2', 'nr 18', 'Nr 16', 'nr 15', 'nr 14', 'nr 13', 'Nr 12', 'Nr 11', 'nr -', 'as', 'ab 9', 'ab 8', 'ab 7', 'ab 6', 'ab 5', 'ab 4', 'ab 30', 'ab 3', 'ab 29', 'ab 28', 'ab 27', 'ab 26', 'ab 25', 'ab 24', 'ab 23', 'ab 22', 'ab 21', 'ab 20', 'ab 2', 'ab 19', 'ab 18', 'ab 17', 'ab 16', 'ab 15', 'ab 14', 'ab 13', 'ab 12', 'ab 11', 'ab 10', 'ab 1', 'SU 9', 'SU 8', 'SU 7', 'SU 6', 'SU 5', 'SU 4', 'SU 30', 'SU 29', 'SU 28', 'SU 27', 'SU 26', 'SU 25', 'SU 24', 'SU 23', 'SU 22', 'SU 21', 'SU 20', 'SU 2', 'SU 19', 'SU 18', 'SU 17', 'SU 16', 'SU 15', 'SU 14', 'SU 13', 'SU 12']

# CONTROLLERS
from controllers import enginecontroller

# BLUEPRINTS
from routes.engineroute import engine_blueprint