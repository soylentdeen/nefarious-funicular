import MoogTools
import AstroUtils
import sys
import os
import pyfits
import SpectralTools
import matplotlib.pyplot as pyplot
import numpy

def synthesizeSpectra():
    #fiducial
    os.system('python generateSpectrum.py fiducial.cfg')

    # Teff
    os.system('python generateSpectrum.py plus_T.cfg')
    os.system('python generateSpectrum.py minus_T.cfg')

    # log g
    os.system('python generateSpectrum.py plus_G.cfg')
    os.system('python generateSpectrum.py minus_G.cfg')

    # B
    os.system('python generateSpectrum.py plus_B.cfg')
    os.system('python generateSpectrum.py minus_B.cfg')

def generateConfigFiles(baseconfig, deltaconfig):
    fiducial = baseconfig.copy()
    fiducial["outbase"] = baseconfig["outbase"] + '_fiducial'

    AstroUtils.write_config('fiducial.cfg', fiducial)

    #delta_T
    plus_T = baseconfig.copy()
    plus_T["outbase"] = baseconfig["outbase"] + '_plusT'
    plus_T["Teff"] += deltaconfig["delta_T"]
    AstroUtils.write_config('plus_T.cfg', plus_T)
    minus_T = baseconfig.copy()
    minus_T["outbase"] = baseconfig["outbase"] + '_minusT'
    minus_T["Teff"] -= deltaconfig["delta_T"]
    AstroUtils.write_config('minus_T.cfg', minus_T)

    #delta_G
    plus_G = baseconfig.copy()
    plus_G["outbase"] = baseconfig["outbase"] + '_plusG'
    plus_G["logg"] += deltaconfig["delta_logg"]
    AstroUtils.write_config('plus_G.cfg', plus_G)
    minus_G = baseconfig.copy()
    minus_G["outbase"] = baseconfig["outbase"] + '_minusG'
    minus_G["logg"] -= deltaconfig["delta_logg"]
    AstroUtils.write_config('minus_G.cfg', minus_G)

    #delta_B
    plus_B = baseconfig.copy()
    plus_B["outbase"] = baseconfig["outbase"] + '_plusB'
    plus_B["Bfield"] += deltaconfig["delta_B"]
    AstroUtils.write_config('plus_B.cfg', plus_B)
    minus_B = baseconfig.copy()
    minus_B["outbase"] = baseconfig["outbase"] + '_minusB'
    minus_B["Bfield"] -= deltaconfig["delta_B"]
    AstroUtils.write_config('minus_B.cfg', minus_B)

def generateDifferentials(config, ax):
    base_filename = config["outbase"]
    base_dir = config["outdir"]

    T = config["Teff"]
    G = config["logg"]
    B = config["Bfield"]
    V = config["vsini"]
    dT = config["delta_T"]
    dG = config["delta_logg"]
    dB = config["delta_B"]


    fiducial_fn = base_dir+base_filename+'_fiducial_T%d_G%.2f_B%.2f_V%.1f.fits' % (T, G, B, V)
    plus_T_fn = base_dir+base_filename+'_plusT_T%d_G%.2f_B%.2f_V%.1f.fits' % (T+dT, G, B, V)
    minus_T_fn = base_dir+base_filename+'_minusT_T%d_G%.2f_B%.2f_V%.1f.fits' % (T-dT, G, B, V)
    plus_G_fn = base_dir+base_filename+'_plusG_T%d_G%.2f_B%.2f_V%.1f.fits' % (T, G+dG, B, V)
    minus_G_fn = base_dir+base_filename+'_minusG_T%d_G%.2f_B%.2f_V%.1f.fits' % (T, G-dG, B, V)
    plus_B_fn = base_dir+base_filename+'_plusB_T%d_G%.2f_B%.2f_V%.1f.fits' % (T, G, B+dB, V)
    minus_B_fn = base_dir+base_filename+'_minusB_T%d_G%.2f_B%.2f_V%.1f.fits' % (T, G, B-dB, V)

    fiducial = pyfits.getdata(fiducial_fn)
    plus_T = pyfits.getdata(plus_T_fn)
    minus_T = pyfits.getdata(minus_T_fn)
    plus_G = pyfits.getdata(minus_T_fn)
    minus_G = pyfits.getdata(minus_G_fn)
    plus_B = pyfits.getdata(plus_B_fn)
    minus_B = pyfits.getdata(minus_B_fn)

    #Do the convolution with the resolution
    wavelength, fiducial_flux = SpectralTools.resample(fiducial[0], fiducial[1], config["delta_resolution"])
    plus_T_wave, plus_T_flux = SpectralTools.resample(plus_T[0], plus_T[1], config["delta_resolution"])
    minus_T_wave, minus_T_flux = SpectralTools.resample(minus_T[0], minus_T[1], config["delta_resolution"])
    plus_G_wave, plus_G_flux = SpectralTools.resample(plus_G[0], plus_G[1], config["delta_resolution"])
    minus_G_wave, minus_G_flux = SpectralTools.resample(minus_G[0], minus_G[1], config["delta_resolution"])
    plus_B_wave, plus_B_flux = SpectralTools.resample(plus_B[0], plus_B[1], config["delta_resolution"])
    minus_B_wave, minus_B_flux = SpectralTools.resample(minus_B[0], minus_B[1], config["delta_resolution"])
   
    # Do the re-binning to the fiducial wavelength
    plus_T_flux = SpectralTools.interpolate_spectrum(plus_T_wave, wavelength, plus_T_flux, pad=1.0)
    minus_T_flux = SpectralTools.interpolate_spectrum(minus_T_wave, wavelength, minus_T_flux, pad = 1.0)
    plus_G_flux = SpectralTools.interpolate_spectrum(plus_G_wave, wavelength, plus_G_flux, pad = 1.0)
    minus_G_flux = SpectralTools.interpolate_spectrum(minus_G_wave, wavelength, minus_G_flux, pad = 1.0)
    plus_B_flux = SpectralTools.interpolate_spectrum(plus_B_wave, wavelength, plus_B_flux, pad = 1.0)
    minus_B_flux = SpectralTools.interpolate_spectrum(minus_B_wave, wavelength, minus_B_flux, pad = 1.0)

    # Finally compute the differential
    deltaT = (plus_T_flux - minus_T_flux)/2.0
    deltaG = (plus_G_flux - minus_G_flux)/2.0
    deltaB = (plus_B_flux - minus_B_flux)/2.0

    Temp = ax.plot(wavelength, deltaT, lw = 2.0, color = 'r', label=r'$\Delta$ Teff = %d K' % dT)
    Grav = ax.plot(wavelength, deltaG, lw = 2.0, color = 'g', label=r'$\Delta$ log g = %.1f dex' % dG)
    Bfield = ax.plot(wavelength, deltaB, lw = 2.0, color = 'b', label=r'$\Delta$ B = %.1f kG' % dB)

    ax.legend(frameon=False)

diffspecConfigFile = sys.argv[1]
config = AstroUtils.parse_config(diffspecConfigFile)

baseconfig = {}
deltaconfig = {}
for key in config.keys():
    if not('delta' in key):
        baseconfig[key] = config[key]
    else:
        deltaconfig[key] = config[key]

pyplot.rc("axes.formatter", useoffset=False)
pyplot.rc("axes", labelsize='large')
pyplot.rc("xtick.major", size=3.0)
fig = pyplot.figure(0, figsize=(12,9))
fig.clear()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.set_xlabel("Wavelength")
ax.set_ylabel("Partial Derivative")
ax.set_title("Differential Sensitivities")

generateConfigFiles(baseconfig, deltaconfig)
synthesizeSpectra()
generateDifferentials(config, ax)

fig.show()
fig.savefig(config["outbase"]+'_R%d_differentials.png' % config["delta_resolution"])
