#!/usr/bin/env python3
from PyQt5.QtWidgets import *
import sys
from . import xrd


def main():
    """ Main function for graphical application start """
    app = QApplication(sys.argv)
    form = xrd.XrdWindow()
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
