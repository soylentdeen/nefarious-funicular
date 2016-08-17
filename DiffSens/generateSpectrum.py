import MoogTools
import sys

moogPyConfigFile = sys.argv[1]
Moog = MoogTools.MoogStokes(moogPyConfigFile, fileBase = 'example', progressBar=True)
Moog.run(saveRaw=True)
