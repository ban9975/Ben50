import os
import configparser

basedir = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(basedir, "config.ini"))
nSensors = 3
gestures = ["down", "up", "open", "little finger"]
calibrationModes = ["no", "flat", "greenpoint", "maxmin"]
testSplit = 0.7
