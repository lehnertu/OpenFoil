# OpenFoil - GUI for analyzing airfoils using OpenFOAM
---------------

This project attempts to compute the aerodynamic properties of airfoil sections
using [OpenFOAM](http://www.openfoam.com). OpenFOAM is the free, open source CFD software
released and developed primarily by OpenCFD Ltd.

The visualization ist based on [VTK](http://wwww.vtk.org) an open-source, freely available
software system for 3D computer graphics, image processing, and visualization. For the current development
under Debian-Linux a custom-compiled version 8.1.1 of the toolkit is used. We try to
maintain compatibility to older versions (in particular version 6.3 currently present
in the Debian repositories) but this depends on the availability of Python 3.x bindings
which are not provided by current Debian distributions.

Dies ist ein ganz am Anfang befindliches Projekt. Die Entwicklung konzentriert sich
im Moment auf die Analyse und Visualisierung von bereits durchgeführten Simulationsrechnungen mit OpenFOAM.
Daher sind die Ergebnisse von Rechnungen eines ausgewählten Profils bei zwei Anstellwinkeln
hier im run/ Ordner bereits zur Verfügung gestellt. In Zukunft werden genau diese
Daten zur Laufzeit des Programmes generiert.
