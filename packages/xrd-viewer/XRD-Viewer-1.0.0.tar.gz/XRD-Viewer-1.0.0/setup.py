# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['xrd_viewer']

package_data = \
{'': ['*'], 'xrd_viewer': ['assets/*']}

install_requires = \
['PyQt5>=5.0,<6.0',
 'h5py>=2.9,<3.0',
 'matplotlib>=3.0,<4.0',
 'numpy>=1.15,<2.0']

entry_points = \
{'console_scripts': ['xrd-viewer = xrd_viewer.__main__:main']}

setup_kwargs = {
    'name': 'xrd-viewer',
    'version': '1.0.0',
    'description': 'Simple analysis tool for NeXus data files',
    'long_description': '# xrd-viewer\nSimple analysis tool for NeXus data files measured at the SIXS beamline at synchrotron Soleil. <br>\nWritten in Python with Qt5 Gui\n\n# Installation \nPlease install the `python3-pyqt5` package of your distribution and then run <br>\n```pip install xrd-viewer```<br>\n\nthen start the program by running `xrd-viewer`\n\n# Usage\nOnce you opened the program, you will be greeted by the default interface with an logo on the top plot and an empty plot on the bottom.\n\nThe (optional) first step is to __load a mask file__ via `File > Load Mask...`\nAfter file selection a preview of the mask file is presented on the upper plot. The program adds an automatic correction of the borders of the detector chips to the mask (hard coded factor of 0.4 will change in the future). The mask can not be unloaded. So please restart the program for a empty mask.\n\nThen `File > Open...` the __folder of the measurements__. It will list all measurement files in the list on the left. There you can select one or multiple files to analyse. If you select mutiple, only one can be visualized on the top plot. The name of this file is visible in the window title bar of the program.\n\nAfter selection of the measurement file the __analysis plot__ on the bottom gets updated. You can select which attributes to assign to each axis. The possible attributes are exctracted from the measurement file. There are two special attributes added: `xpad_image` and `slices`. The `xpad_image` corresponds to the region of interest (see below) and `slices` corresponds to the scan frame in the measurement (slider on the top of the upper plot).\nThe typical setting is `omega` vs `xpad_image`.\n\nThe __region of interest__ (ROI) can be selected in the upper plot window. Click the `Edit regions...` button to open the extended region editor. By default it has two regions. The first region is the background region and all regions afterwards are ROIs. By default the second region (= the first ROI) is the active region. The active region is displayed as red rectangle and can be manipulated by moving the edges to the desired positions. The region editor can also be used to refine the region (values are in pixels). A new ROI can be added by `New Region` button.\n\n## Tips for analysis of measurements\n* If the background region should not be applied. You can move it to the upper left corner with an width and length of 1. (In this corner is typically a shadow in the measurements, so zero counts.)\n* You can move the cursor in the bottom plot my draging the mouse. The upper plot gets updated. This also sets the focus on the frame slider, so you can move the cursor by pressing left and right.\n* Typically the first frames of a measurement are corrupted, you can set an value in the bottom input box to ignore them.\n* After selecting a measurement `File > Save Graph...` becomes enabled. You can save the current analysis plot as image in `*.JPG`,`*.PNG` or `*.PDF` format (the cursor and indicator will be removed) or as plain text `*.TXT` for further analysis. The plain text file will have some metadata about the measurement file, the mask file and the selected regions.',
    'author': 'Sebastian Schenk',
    'author_email': 'sebastian.schenk@physik.uni-halle.de',
    'url': 'https://gitlab.com/merrx/xrd-viewer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
