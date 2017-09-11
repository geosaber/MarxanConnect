Marxan with Connectivity
================

Marxan with Connectivity (henceforth the â€œappâ€) is a Graphical User Interface (GUI) to help conservationists include â€œconnectivityâ€ in their protected area network planning.

The term â€œconnectivityâ€ has a variety of definitions (i.e. larval connectivity, genetic connectivity, landscape connectivity, etc) and protected area networks can be optimized for various connectivity objectives. The app is intended to guide conservationists through the process of identifying important aspects of connectivity for their conservation scenarios as well as highlighting the necessary data.

The app also includes be a fully functional python module (in progress) that is operated via command line that can be used to reproduce an analysis using the project file generated by the GUI.

Installing
----------

### Windows Installer:

(**WARNING! Marxan with Connectivity is 'pre-alpha' and is not yet fully operational, download at your own risk**)

Please download the latest [MarxanConnectSetupWindows.exe](https://github.com/remi-daigle/MarxanConnect/releases) installer file, run it, and follow the instructions. Alternatively (for advanced users only), follow the [Building from source](https://github.com/remi-daigle/MarxanConnect#building-from-source) instructions to use the latest bleeding edge version of the app.

### Mac and Linux Installers:

(in progress)

Building from source
--------------------

Building from source is only necessary if you plan to contribute to the project (see [Contributing](https://github.com/remi-daigle/MarxanConnect/blob/master/README.md#Contributing) section below) or if you want to use the bleeding edge version of the app

Building this repository has only been tested on Python 3.5.2 64-bit on a machine running Windows 10, your mileage may vary! (*Please note, I could not build the repository using Anaconda*).

-   Download this repository
-   If necessary, edit the hard coded file paths in [setup.py](https://github.com/remi-daigle/MarxanConnect/blob/master/setup.py) and [Marxan with Connectivity.nsi](https://github.com/remi-daigle/MarxanConnect/blob/master/Marxan%20with%20Connectivity.nsi)
-   open a terminal or `cmd` window (or git bash) in the project directory and type:

<!-- -->

    make

### Prerequisites (for building from source)

-   [Python 3.5.2 64-bit](https://www.python.org/downloads/release/python-352/)
-   [wxFormBuilder](https://github.com/wxFormBuilder/wxFormBuilder)
-   [NSIS](http://nsis.sourceforge.net/Main_Page)
-   [NSIS Quick Setup Script Generator](http://nsis.sourceforge.net/NSIS_Quick_Setup_Script_Generator)

It also assumes you have all the pre-requisite python modules installed, i.e.:

    #!/bin/bash
    # for basic GUI
    pip install wxpython
    pip install matplotlib
    pip install matplotlib.basemap
    pip install geopandas
    pip install descartes
    pip install python-igraph
    pip install networkx

    # for compiling executable
    pip install cx_Freeze
    pip install sys
    pip install os

Built With
----------

The `gui.py` file was built using the fantastic [wxFormBuilder](https://github.com/wxFormBuilder/wxFormBuilder).

The windows installer was built using [NSIS](http://nsis.sourceforge.net/Main_Page) and the [NSIS Quick Setup Script Generator](http://nsis.sourceforge.net/NSIS_Quick_Setup_Script_Generator)

Contributing
------------

Please read [CONTRIBUTING.md](https://github.com/remi-daigle/MarxanConnectGUI/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

Versioning
----------

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/remi-daigle/MarxanConnectGUI/tags).

Authors
-------

-   **Remi Daigle** - *Initial work, development, maintenance* - [remi-daigle](https://github.com/remi-daigle)
-   **Arieanna Balbar** - *Consultation, Mac installer development*
-   **Anna Metaxas** - *Consultation*
-   **Maria Beger** - *Consultation*

See also the list of [contributors](https://github.com/remi-daigle/MarxanConnectGUI/contributors) who participated in this project.

License
-------

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/remi-daigle/MarxanConnectGUI/blob/master/LICENSE) file for details

Acknowledgments
---------------

-   Funding for the development of this sotware was provided Canadian Healthy Oceans Network [(CHONe)](https://chone2.ca/) a Natural Sciences and Engineering Research Council of Canada [(NSERC)](http://www.nserc-crsng.gc.ca/index_eng.asp) Strategic Network.
-   This project builds on the existing [Marxan](http://marxan.net/) (Ball et al. 2009) software and would not be possible without the hard work of Ian Ball, Hugh Possingham, and Matt Watts.

References
----------

Ball, I.R., H.P. Possingham, and M. Watts. 2009. Marxan and relatives: Software for spatial conservation prioritisation. Chapter 14: Pages 185-195 in Spatial conservation prioritisation: Quantitative methods and computational tools. Eds Moilanen, A., K.A. Wilson, and H.P. Possingham. Oxford University Press, Oxford, UK.
