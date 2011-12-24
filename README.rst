MetaSCons
=========

This project uses SCons to build other "external" packages.  It uses
scons to work out the dependencies.  The basic idea is that all
supported packages have a ``metascons.wrapper.Package`` which defines
a ``metascons.wrapper.Wrapper`` class that takes care of what is
needed to 

* download,
* configure,
* make and
* install the package

The base class provides some default methods assuming the package is
actually built by autoconf.

This class also declares any dependencies on other external packages.

The final result is an installation area layed out like:

::

  install_area/PACKAGE/VERSION/PLATFORM/

Configuration
=============

A INI-style configuration file is used.  And example is in
cfg/example.cfg which builds some tiny test packages (which happen to
use SCons themselves).  The test requires the ``webcache/`` directory
to be available on the web somewhere.

Configuration items in the DEFAULTS section can also be specified on
the command line.

Running
=======

To run the example::

  scons -f metascons.scons --build-config=cfg/example.cfg 


To Do
=====

* Add shell setup code emission so users can have ``PATH``,
  ``LD_LIBRARY_PATH``, etc, setup to point into ``install_area``.

Inspiration
===========

I have implemented a similar build system using the LCGCMT project
from CERN's SPI for the Daya Bay experiment where I wrote a layer of
automation.  I've since reimplemented that layer (see
http://www.phy.bnl.gov/trac/garpi/) but after learning a bit about
SCons I thought I could greatly simplify things and remove the LCGCMT
layer.
