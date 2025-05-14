# fmi-cli
Python program for fetching current weather from Finnish Meteorological Institute's open data.<br/>
Prints selected data in "\[parameter description\] : \[value\] \[unit\]" format.

Uses [open data](https://en.ilmatieteenlaitos.fi/open-data) by [Finnish Meteorological Institute](https://en.ilmatieteenlaitos.fi/) which is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## Usage
Edit `params` string to include the parameters you want in the printout.

Edit `place` string to the location you want information from.

`timestep` and `offset` variables should only be edited if the programs occasionally fails to fetch data. The default 10 minutes offset seems to work reliably.

Run the program: `python3 fmi-cli.py`