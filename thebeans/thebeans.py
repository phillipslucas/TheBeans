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

    def ad_layers_control(self, position='topright'):
        self.add_control(ipyleaflet.LayersControl(position=position))


#3/18 lecuture
    def add_geojson(self, data, name="geojson", **kwargs):
        self.add_control(ipyleaflet.GeoJSON(data=data, name=name, **kwargs))

        import json

        if isinstance(data, str):
            with open(data) as f:
            data = json.load(f)
        
        if "hover_style" not in kwargs:
          kwargs['hover_style'] = {
              "color": "green",
              "weight": 1,
              "fillColor": "green",
              "fillOpacity": 0.5
          }

        if "style" not in kwargs:
            kwargs['style'] = {
                "color": "#ff0000",
                "weight": 1,
                "fillColor": "green",
                "fillOpacity": 0.5
            }

        layer = ipyleaflet.GeoJSON(data=data, name=name, **kwargs)
        self.add(layer)