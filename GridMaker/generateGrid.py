import MoogTools
import AstroUtils
import sys
import os
import pyfits
import SpectralTools
import matplotlib.pyplot as pyplot
import numpy
import random
import string

def synthesizeSpectra(configFiles, flavor):
    for f in configFiles:
        os.system('python generateSpectrum.py '+f+' '+flavor)


def generateConfigFiles(baseConfig, gridConfig):
    try:
        teff = numpy.array(gridConfig['grid_T'].split(','), dtype = numpy.int)
    except:
        teff = [baseConfig['Teff']]

    try:
        logg = numpy.array(gridConfig['grid_logg'].split(','), dtype= numpy.float)
    except:
        logg = [baseConfig['logg']]

    try:
        bfield = numpy.array(gridConfig['grid_B'].split(','), dtype=numpy.float)
    except:
        bfield = [baseConfig['Bfield']]

    try:
        vsini = numpy.array(gridConfig['grid_vsini'].split(','), dtype=float)
    except:
        vsini = [baseConfig['vsini']]

    filenames = []
    for temp in teff:
        for grav in logg:
            for b in bfield:
                for v in vsini:
                    configFile = baseConfig.copy()
                    configFile["Teff"] = temp
                    configFile["logg"] = grav
                    configFile["Bfield"] = b
                    configFile["vsini"] = v
                    filename = 'ConfigFiles/Config_T%d_G%.1f_B%.1f_V%.1f.cfg' % (temp, grav, b, v)
                    AstroUtils.write_config(filename, configFile)
                    filenames.append(filename)

    return filenames

diffspecConfigFile = sys.argv[1]
config = AstroUtils.parse_config(diffspecConfigFile)

flavor = ''.join(random.choice(string.ascii_uppercase) for _ in range(4))

baseconfig = {}
gridconfig = {}
for key in config.keys():
    if not('grid' in key):
        baseconfig[key] = config[key]
    else:
        gridconfig[key] = config[key]

configFiles = generateConfigFiles(baseconfig, gridconfig)
synthesizeSpectra(configFiles, flavor)

