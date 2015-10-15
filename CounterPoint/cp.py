import CounterPoint
import SpectralTools
import scipy
import numpy
import matplotlib.pyplot as pyplot
import sys

pyplot.rc('axes.formatter', useoffset=False)

fig = pyplot.figure(0)
fig.clear()
ax1 = fig.add_axes([0.1, 0.4, 0.8, 0.5])
ax2 = fig.add_axes([0.1, 0.1, 0.8, 0.3])

configFile = sys.argv[1]

Orchestra = CounterPoint.Orchestra(configFile)

wlOffset = Orchestra.config["wlOffset"]
continuum = Orchestra.config["continuum"]
veiling = Orchestra.config["veiling"]

ax1.plot(Orchestra.observed.wave, Orchestra.observed.flux, label='TW Hydra')
ax1.set_xbound(lower = Orchestra.wlStart, upper=Orchestra.wlStop)
ax1.set_ybound(lower = 0.0, upper = 1.5)
ax2.set_xbound(lower = Orchestra.wlStart, upper=Orchestra.wlStop)
ax2.set_ybound(lower = -0.3, upper = 0.3)
#params = ax.text(0.1, 0.8, "wlShift", fontsize=12, transform=ax.transAxes)
fig.show()


choice = ''
while choice != 'q':
    if choice == 's':
        Orchestra.selectPlayers()
    elif choice == 'w':
        wlOffset += float(raw_input("Enter Wavelength Offset : "))
    elif choice == 'c':
        continuum *= float(raw_input("Enter multiplicative continuum factor : "))
    elif choice == 'v':
        veiling = float(raw_input("Enter new Veiling :"))
    Ensemble = Orchestra.getEnsemble()
    ax1.clear()
    ax2.clear()
    wave = Orchestra.observed.wave+wlOffset
    flux = Orchestra.observed.flux*continuum
    ax1.plot(wave, flux, label='TW Hydra')
    ax2.plot([Orchestra.wlStart, Orchestra.wlStop], [0.0, 0.0])

    for spectra, l in zip(Ensemble[0], Ensemble[1]):
        newSpec = (SpectralTools.binSpectrum(spectra[1], spectra[0], wave)+veiling)/(1.0+veiling)
        difference = flux - newSpec

        ax1.plot(wave, newSpec, label=l)
        ax2.plot(wave, difference)

    ax1.set_xbound(lower = Orchestra.wlStart, upper=Orchestra.wlStop)
    ax1.set_ybound(lower = 0.0, upper = 1.5)
    ax2.set_xbound(lower = Orchestra.wlStart, upper=Orchestra.wlStop)
    ax2.set_ybound(lower = -0.15, upper = 0.15)
    ax1.set_xticklabels([])
    params = ax1.text(0.1, 0.8, "wlShift = %.1f A\nContinuum Scaling = %.2f\nVeiling = %.2f"
            % (wlOffset, continuum, veiling), transform = ax1.transAxes, fontsize=19.0)

    ax1.legend(loc=3)
    fig.show()
    print("(s)elect plotted spectra")
    print("(w)avelength offset")
    print("(c)ontinuum")
    print("(v)eiling")
    print("(q)uit")
    choice = raw_input("Enter choice: ")
