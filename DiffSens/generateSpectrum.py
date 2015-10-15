import MoogTools
import sys

moogPyConfigFile = sys.argv[1]
Moog = MoogTools.MoogStokesSpectrum(moogPyConfigFile, fileBase = 'example')
wavelength, flux = Moog.run(save=True)
