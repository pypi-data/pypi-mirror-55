Roadmap
=======

rel. 0.3
--------
- export to csv functionality (re-implementation)
- refactoring: PEP8 compliance for gui.py
- remove error/warning "QCoreApplication::exec: The event loop is already running" (doesn't seem to
  cause functionality issues)
- define/import user data points (from csv file)
- auto-resize for constants table
- add possibility to define kwargs for plt.plot
- select scale (lin/log) for set constant generation
- add "settings" (to modify allowed imports, calls,...)
- possibility to define imports and alias (import ... as ...)
- multiple set constants definition (table widget)
- rename package to ez-plot or easy-plot?

later releases
--------------
- add parameters (constants) optimizer (in conjunction with user data points)
- convert equations to LaTeX
- guess constant's names from function definition
- create code for gnuplot?