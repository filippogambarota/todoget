"""
UTILS functions for printing messages
"""

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def tick():
    return '\u2713'

def text_green(msg):
    out = bcolors.OKGREEN + msg + bcolors.ENDC
    return out

def text_blue(msg):
    out = bcolors.OKBLUE + msg + bcolors.ENDC
    return out

def success_init():
    print(text_green(tick()) + " configuration file " + text_green(".todoget") + " created, project initialized!")
    
def success_file_scan(filename):
    print(text_green(tick()) + " " + filename + " scanned!")

def success_output(filename):
    print(text_blue(tick()) + " " + filename + " created!")