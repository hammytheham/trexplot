# Welcome to trexplot

By Hamish Robertson & Tan Benjakul

We aim to deliver a LoFi plotting experience to Toughreactmech output files.

## To install

`pip install -i https://test.pypi.org/simple/ trexplot==1`

This doesn't works well yet... Will figure out some moon in the future....

Just `git clone` this repo for the time being

## To get stuff to work stuff

We supply a set of example .tec files. Move the TestFiles folder somewhere else.

`cd` into the TestFiles folder.

run `ipython ../Trexplot/trexplot.py`

This will use the trexoptions file which controls plotting located in this folder. The trex options supplied by default has all options turned on including for all .tec files.

Supported .tec files are flow data, flow vector, displacement, stress strain, aqueous concentrations, gas volfrac, mineral abundances and saturation states.

Use the trex_fig_return.py script as an example of methods to personally modify the returned graphics.

Drop a message if you want new features or have bugs
