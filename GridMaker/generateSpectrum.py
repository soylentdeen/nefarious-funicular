import MoogTools
import sys

moogPyConfigFile = sys.argv[1]
flavor = sys.argv[2]
Moog = MoogTools.MoogStokesSpectrum(moogPyConfigFile, fileBase = flavor)
wavelength, flux = Moog.run(save=True)
