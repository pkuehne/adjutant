""" Script to build the executable version for release """

import os
import PyInstaller.__main__

# Get the location of the spec file
spec_file = os.path.join(os.getcwd(), "adjutant.spec")

# Run PyInstaller
PyInstaller.__main__.run([spec_file])
