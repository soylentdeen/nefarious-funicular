import pyfits
import AstroUtils
import matplotlib.pyplot as pyplot
import scipy
import numpy
import SpectralTools
import sys
import numpy
import Moog960

configFile = sys.argv[1]
try:
    plot = bool(sys.argv[2]=='True')
except:
    plot = False

config = AstroUtils.parse_config(configFile)

fig1 = pyplot.figure(0)
fig1.clear()
ax1 = fig1.add_axes([0.1, 0.1, 0.8, 0.8])
fig2 = pyplot.figure(1)
fig2.clear()
ax2 = fig2.add_axes([0.1, 0.1, 0.8, 0.8])

watched_dir = config['watched_dir']
wlStart = config['wlStart']
wlStop = config['wlStop']
vacca = config['Vacca']

parameters = {}
parameters["TEFF"] = []
parameters["LOGG"] = []
parameters["BFIELD"] = []

orchestra = Moog960.Score(directory='../../cuddly-weasel/MusicMaker/TWHydra', suffix='', observed='../../cuddly-weasel/Theremin/TWHydra.fits')

mastered = orchestra.master()
orchestra.selectEnsemble(selectedLabels=mastered)

bfield = []
logg = []
teff = []

temps = orchestra.convolvedGridPoints["TEFF"]
gravs = orchestra.convolvedGridPoints["LOGG"]
bs = orchestra.convolvedGridPoints["BFIELD"]

models, labels = orchestra.perform(selectedLabels=mastered)

twHydraSpectrum, twHydraLabel = orchestra.listen()
twHydraSpectrum.wl -= 5.5

TWHydra_EW = twHydraSpectrum.calc_EW(wlStart, wlStop, findContinuum=False)

EWs = []

for model in models:
    EWs.append(model.calc_EW(wlStart, wlStop))
    if plot:
        ax2.clear()
        twHydraSpectrum.plot(ax=ax2)
        ax2.plot([wlStart, wlStart], [0.0, 1.0], color = 'k')
        ax2.plot([wlStop, wlStop], [0.0, 1.0], color = 'k')
        model.plot(ax=ax2)
        ax2.set_xbound(wlStart-10.0, wlStop+10.0)
        ax2.set_ybound(0.0, 1.5)
        fig2.show()
        raw_input()

    teff.append(model.label.parameters["TEFF"])
    logg.append(model.label.parameters["LOGG"])
    bfield.append(model.label.parameters["BFIELD"])

bfield = numpy.array(bfield)
logg = numpy.array(logg)
teff = numpy.array(teff)

EWs = numpy.array(EWs)

orchestra.selectEnsemble(selectedLabels=mastered)

CMJParams = {"TEFF":4180, "LOGG":4.8, "BFIELD":2.3}
WVParams = {"TEFF":3600, "LOGG":3.5, "BFIELD":0.0}
SpectrumCMJ, LabelCMJ = orchestra.blend(desiredParameters=CMJParams)
SpectrumWV, LabelWV = orchestra.blend(desiredParameters=WVParams)

EW_CMJ = LabelCMJ[0].Spectrum.calc_EW(wlStart, wlStop)
EW_WV = LabelWV[0].Spectrum.calc_EW(wlStart, wlStop)

r_CMJ_vacca = (1.0 - vacca/EW_CMJ)
r_CMJ_IGRINS = (1.0 - TWHydra_EW/EW_CMJ)
r_WV_vacca = (1.0 - vacca/EW_WV)
r_WV_IGRINS = (1.0 - TWHydra_EW/EW_WV)

print("Veiling")
print("CMJ Parameters, Vacca EW: %.3f" % r_CMJ_vacca)
print("CMJ Parameters, IGRINS EW: %.3f" % r_CMJ_IGRINS)
print("Vacca Parameters, Vacca EW: %.3f" % r_WV_vacca)
print("Vacca Parameters, IGRINS EW: %.3f" % r_WV_IGRINS)

for g, lc in zip(gravs, ['b', 'g', 'r']):
    for b, ls in zip(bs, ['--', '-.', '-', ':', (0, (5, 3))]):
        bm = (bfield==b) & (logg ==g)
        order = numpy.argsort(teff[bm])
        ax1.plot(teff[bm][order], EWs[bm][order], ls=ls, color =lc, lw=2.0)

ax1.plot([numpy.min(teff), numpy.max(teff)], [vacca, vacca], lw=2.0, color = 'k')
ax1.plot([numpy.min(teff), numpy.max(teff)], [TWHydra_EW, TWHydra_EW], lw=2.0, color = 'm')
fig1.show()

del(orchestra)
del(twHydraSpectrum)
del(twHydraLabel)

