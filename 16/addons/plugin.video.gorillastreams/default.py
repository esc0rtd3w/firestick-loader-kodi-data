import sys, traceback

#####################################################################################################
#####################################################################################################
##I AM NOT THE CREATOR OF THIS ADDON, I HAVE MODDIFIED CODE THAT ALREADY EXISTS AND I'M NOT TRYING ##
##TO PASS THIS OFF AS MY OWN WORK. THANK YOU TO THE DEVS WHO HAVE WORKED ON THIS AND THANK YOU FOR ##
##                GIVING ME A PLATFORM TO LEARN FROM - BEATBOX8501                                 ##
#####################################################################################################
#####################################################################################################


# REMOTE DEBUGGING
REMOTE_DBG = False

# append pydev remote debugger
if REMOTE_DBG:
    # Make pydev debugger works for auto reload.
    # Note pydevd module need to be copied in XBMC\system\python\Lib\pysrc
    try:
        import pysrc.pydevd as pydevd
    # stdoutToServer and stderrToServer redirect stdout and stderr to eclipse console
        pydevd.settrace('localhost', stdoutToServer=True, stderrToServer=True, suspend=False)
    except ImportError:
        sys.stderr.write("Error: " +
            "You must add org.python.pydev.debug.pysrc to your PYTHONPATH.")
        sys.exit(1)
    except:
        sys.stderr.write('Remote Debugger is not started')




# ACTUAL ADDON
from lib import main

try:
    myAddon = main.Main()
    myAddon.run(sys.argv)
except:
    traceback.print_exc(file = sys.stdout)
