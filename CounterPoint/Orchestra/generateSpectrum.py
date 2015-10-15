import MoogTools

moogPyConfigFile = 'spectrum.cfg'
Moog = MoogTools.MoogStokesSpectrum(moogPyConfigFile, fileBase = 'example')
wavelength, flux = Moog.run(save=True)
