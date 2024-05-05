# Welcome to thebeans


[![image](https://img.shields.io/pypi/v/thebeans.svg)](https://pypi.python.org/pypi/thebeans)

**Python package with the beans.**

- Free software: MIT License
- Documentation: <https://phillipslucas.github.io/thebeans>

## Features

The beans is a python package developed from the bones of ipyleaflet and forged in the fire of hydrologic network analysis. With this package you can upload and interact with data in a map class and run hydrological network analysis on raster data. Some functionality may be best when run locally. The package continues to be developed and hopes to see more integration between interactive mapping and hydologic modelling in the near future.

- Create a map with a single line of code.
- Choose basemaps interactively or through code.
- Display data on the interactive map from local or online sources.
- Delineate hydrologic networks utilizing Pysheds watershed delineation tools.

## Usage

This package helps visualize data from local or online sources. It will take raster data hosted online and delineate a watershed catchment then visualize the outputs using matplotlib plots. 

### Quickstart Notebook
[![image](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/phillipslucas/TheBeans/blob/main/docs/examples/quickstart.ipynb)

<iframe width="560" height="315" src="https://www.youtube.com/embed/7JGnJvhqsJQ?si=w3uIdDbD7-VdhN0X" title="The Beans Walkthrough" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Installation Instructions

You can install `thebeans` using pip:
```bash
$ pip install thebeans
```