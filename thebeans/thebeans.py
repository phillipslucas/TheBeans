"""Main module."""
#creating a new ipyleaflet class for deploymnet
#This doc shows you how the package was built. This is where you build code 
#make sure the packages are installed in your environment

import ipyleaflet
from ipyleaflet import basemaps

class Map(ipyleaflet.Map):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_control(ipyleaflet.LayerControl())

    def add_tile_layer(self, url, name, **kwargs):
        layer = ipyleaflet.TileLayer(url=url, name=name, **kwargs)
        self.add_layer(layer)
    
    #This block means you can call up a basemap based on a string.
    #You can call up the basemap without knowing the url
    def add_basemap(self, name):

        if isinstance(name, str):
            basemap = eval(f"basemaps.{name}").build_url()
            self.add(basemap)
        else:
            self.add(name)

