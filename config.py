import configparser
import os
from printer import ERROR, time_now

# Read the config file
config = configparser.ConfigParser(interpolation=None)
if not os.path.exists(os.path.dirname(__file__)+"\config.ini"):
    print(ERROR + time_now() + "config.ini not found in {}\. Terminating...".format(os.path.dirname(__file__)))
    exit()
config.read("config.ini")