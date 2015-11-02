import pyfits
import AstroUtils
import matplotlib.pyplot as pyplot
import scipy
import numpy
import SpectralTools
import sys
import numpy

configFile = sys.argv[1]

config = AstroUtils.parse_config(configFile)

watched_dir = config['watched_dir']
wlStart = config['wlStart']
wlStop = config['wlStop']

parameters = {}
parameters["TEFF"] = []
parameters["LOGG"] = []
parameters["BFIELD"] = []

parameters, waves, fluxes = SpectralTools.winnow_MoogStokes_Spectra(watched_dir, wlStart, wlStop, trackedParams=parameters)
EWs = []

teff = numpy.array(parameters["TEFF"])
logg = numpy.array(parameters["LOGG"])
bfield = numpy.array(parameters["BFIELD"])

temps = numpy.unique(teff)
gravs = numpy.unique(logg)
bs = numpy.unique(bfield)

for w, f in zip(waves, fluxes):
    EWs.append(SpectralTools.calc_EW(w, f, wlStart, wlStop))

EWs = numpy.array(EWs)
fig = pyplot.figure(0)
fig.clear()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

for g, lc in zip(gravs, ['b', 'g', 'r']):
    for b, ls in zip(bs, ['-', '--', ':']):
        bm = (bfield==b) & (logg ==g)
        order = numpy.argsort(teff[bm])
        ax.plot(teff[bm][order], EWs[bm][order], ls=ls, color =lc, lw=2.0)

fig.show()
