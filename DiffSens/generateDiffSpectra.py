import MoogTools
import AstroUtils
import Moog960
import sys
import os
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

def generateDifferentials(config, deriv_ax, fiducial_ax):
    base_filename = config["outbase"]
    base_dir = config["outdir"]

    T = config["Teff"]
    G = config["logg"]
    B = config["Bfield"]
    V = config["vsini"]
    dT = config["delta_T"]
    dG = config["delta_logg"]
    dB = config["delta_B"]

    
    differentials = Moog960.Score(directory=base_dir+base_filename)

    fiducial_fn = base_dir+base_filename+'_fiducial_T%d_G%.2f_B%.2f_raw.fits' % (T, G, B)
    plus_T_fn = base_dir+base_filename+'_plusT_T%d_G%.2f_B%.2f_raw.fits' % (T+dT, G, B)
    minus_T_fn = base_dir+base_filename+'_minusT_T%d_G%.2f_B%.2f_raw.fits' % (T-dT, G, B)
    plus_G_fn = base_dir+base_filename+'_plusG_T%d_G%.2f_B%.2f_raw.fits' % (T, G+dG, B)
    minus_G_fn = base_dir+base_filename+'_minusG_T%d_G%.2f_B%.2f_raw.fits' % (T, G-dG, B)
    plus_B_fn = base_dir+base_filename+'_plusB_T%d_G%.2f_B%.2f_raw.fits' % (T, G, B+dB)
    minus_B_fn = base_dir+base_filename+'_minusB_T%d_G%.2f_B%.2f_raw.fits' % (T, G, B-dB)

    fiducial = Moog960.SyntheticMelody(filename=fiducial_fn)
    plus_T = Moog960.SyntheticMelody(filename=plus_T_fn)
    minus_T = Moog960.SyntheticMelody(filename=minus_T_fn)
    plus_G = Moog960.SyntheticMelody(filename=minus_T_fn)
    minus_G = Moog960.SyntheticMelody(filename=minus_G_fn)
    plus_B = Moog960.SyntheticMelody(filename=plus_B_fn)
    minus_B = Moog960.SyntheticMelody(filename=minus_B_fn)

    fiducial.selectPhrases(selectAll=True)
    fiducial_Labels = fiducial.rehearse(vsini=V, R=config["resolving_power"], returnLabels=True)
    fiducial_Spectrum, blah = fiducial.perform(label=fiducial_Labels[0])
    
    plus_T.selectPhrases(selectAll=True)
    plus_T_Labels = plus_T.rehearse(vsini=V, R=config["resolving_power"], observedWl=fiducial_Spectrum.wl, returnLabels=True)
    plus_T_Spectrum, blah = plus_T.perform(label=plus_T_Labels[0])

    minus_T.selectPhrases(selectAll=True)
    minus_T_Labels = minus_T.rehearse(vsini=V, R=config["resolving_power"], observedWl=fiducial_Spectrum.wl, returnLabels=True)
    minus_T_Spectrum, blah = minus_T.perform(label=minus_T_Labels[0])

    plus_G.selectPhrases(selectAll=True)
    plus_G_Labels = plus_G.rehearse(vsini=V, R=config["resolving_power"], observedWl=fiducial_Spectrum.wl, returnLabels=True)
    plus_G_Spectrum, blah = plus_G.perform(label=plus_G_Labels[0])

    minus_G.selectPhrases(selectAll=True)
    minus_G_Labels = minus_G.rehearse(vsini=V, R=config["resolving_power"], observedWl=fiducial_Spectrum.wl, returnLabels=True)
    minus_G_Spectrum, blah = minus_G.perform(label=minus_G_Labels[0])

    plus_B.selectPhrases(selectAll=True)
    plus_B_Labels = plus_B.rehearse(vsini=V, R=config["resolving_power"], observedWl=fiducial_Spectrum.wl, returnLabels=True)
    plus_B_Spectrum, blah = plus_B.perform(label=plus_B_Labels[0])

    minus_B.selectPhrases(selectAll=True)
    minus_B_Labels = minus_B.rehearse(vsini=V, R=config["resolving_power"], observedWl=fiducial_Spectrum.wl, returnLabels=True)
    minus_B_Spectrum, blah = minus_B.perform(label=minus_B_Labels[0])


    # Finally compute the differential
    deltaT = (plus_T_Spectrum - minus_T_Spectrum)/2.0
    deltaG = (plus_G_Spectrum - minus_G_Spectrum)/2.0
    deltaB = (plus_B_Spectrum - minus_B_Spectrum)/2.0

    deltaT.plot(ax=deriv_ax, lw=2.0, color = 'r', label=r'$\Delta$ Teff = %d K' % dT)
    deltaG.plot(ax=deriv_ax, lw=2.0, color = 'g', label=r'$\Delta$ log g = %.1f dex' % dG)
    deltaB.plot(ax=deriv_ax, lw=2.0, color = 'b', label=r'$\Delta$ B = %.1f kG' % dB)
    fiducial_Spectrum.plot(ax=fiducial_ax, lw=2.0, color = 'k', label=r'Teff = %d, log g = %.1f, B = %.1f kG' % (T, G, B))

    deriv_ax.legend(frameon=False)
    fiducial_ax.legend(frameon=False)

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
deriv_ax = fig.add_axes([0.1, 0.1, 0.8, 0.4])
deriv_ax.set_xlabel("Wavelength")
deriv_ax.set_ylabel("Partial Derivative")
deriv_ax.set_title("Differential Sensitivities")

fiducial_ax = fig.add_axes([0.1, 0.5, 0.8, 0.4])
fiducial_ax.set_xlabel("")
fiducial_ax.set_ylabel("Fiducial Flux")


generateConfigFiles(baseconfig, deltaconfig)
synthesizeSpectra()
generateDifferentials(config, deriv_ax, fiducial_ax)

fig.show()
fig.savefig(config["outbase"]+'_R%d_differentials.png' % config["resolving_power"])
