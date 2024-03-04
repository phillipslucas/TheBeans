"""Main module."""
#creating a new ipyleaflet class for deploymnet
#This doc shows you how the package was built. This is where you build code 
#make sure the packages are installed in your environment

import ipyleaflet

class Map(ipyleaflet.Map):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_control(ipyleaflet.LayerControl())