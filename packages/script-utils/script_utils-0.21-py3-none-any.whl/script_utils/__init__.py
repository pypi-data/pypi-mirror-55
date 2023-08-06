

if not __name__ == '__main__':
    from .script_utils import *
    print("Logging turned {}, you can change it with LOGGING "
          "variable in script_utils.py file".format("on" if LOGGING else "off"))
