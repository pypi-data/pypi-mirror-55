import sys

# only work for 64 bit system
if sys.maxsize < 2**31:
    raise RuntimeError('64 bit system is required')

# python 3.6 is required
if sys.version_info[0] != 3:
    raise RuntimeError('Python version 3.7 is need (Anaconda is recommended https://www.anaconda.com/distribution/)')

if sys.version_info[1] != 7:
    raise RuntimeError('Python version 3.7 is need (Anaconda is recommended https://www.anaconda.com/distribution/)')

# platform dependent
if sys.platform.startswith('linux'):

    from openseespy.opensees.linux.opensees import *

elif sys.platform.startswith('win'):

    from openseespy.opensees.win.opensees import *

    # if sys.version_info[1] == 6:

    #    from openseespy.opensees.winpy36.opensees import *

    # elif sys.version_info[1] == 7:

    #    from openseespy.opensees.winpy37.opensees import *

    # elif sys.version_info[1] == 8:

    #    from openseespy.opensees.winpy38.opensees import *

elif sys.platform.startswith('darwin'):

    from openseespy.opensees.mac.opensees import *


else:

    raise RuntimeError(sys.platform+' is not supported yet')


