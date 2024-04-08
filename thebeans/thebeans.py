"""Main module."""
#creating a new ipyleaflet class for deploymnet
#This doc shows you how the package was built. This is where you build code 
#make sure the packages are installed in your environment


import ipyleaflet
from ipyleaflet import Map, basemaps, Marker
import ipywidgets as widgets


class Map(ipyleaflet.Map):
    """Map class that inherits from ipyleaflet.Map.

    Args:
        ipyleaflet (Map): The ipyleaflet.Map class.
    """    
    def __init__(self, basemap = basemaps.Strava.Run, center = (48.513,-120.218), zoom = 5, **kwargs):
        """Initialize the map.

        Args:
            center (list, optional): Set the center of the map. Defaults to WA [47.7511, -120.7401].
            zoom (int, optional): Set the zoom level of the map. Defaults to 6.
        """
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        #add layer control not as straight forward. Need to pass to an object and consider it as a parameter that you can pass. Ipyleaflet doesn't support.
        

        super().__init__(center = center, zoom = zoom, **kwargs)
        self.add_control(ipyleaflet.LayersControl())

        


    def add_tile_layer(self, url, name, **kwargs):
        layer = ipyleaflet.TileLayer(url=url, name=name, **kwargs)
        self.add_layer(layer)
    
    #This block means you can call up a basemap based on a string.
    #You can call up the basemap without knowing the url
    def add_basemap(self, name):
        """
        Adds a basemap to the current map.

        Args:
            name (str or object): The name of the basemap as a string, or an object representing the basemap.

        Raises:
            TypeError: If the name is neither a string nor an object representing a basemap.

        Returns:
            None
        """
    
        if isinstance(name, str):
            url = eval(f"basemaps.{name}").build_url()
            self.add_tile_layer(url, name)
        else:
            self.add(name)

    def add_layers_control(self, position='topright'):
        """Adds a layers control to the map.

        Args:
            position (str, optional): The position of the layers control. Defaults to "topright".
        """
        self.add_control(ipyleaflet.LayersControl(position=position))


    #3/18 lecuture
    def add_geojson(self, data, name="geojson", **kwargs):
        #self.add_control(ipyleaflet.GeoJSON(data=data, name=name, **kwargs))
        """Adds a GeoJSON layer to the map.

        Args:
            data (str | dict): The GeoJSON data as a string or a dictionary.
            name (str, optional): The name of the layer. Defaults to "geojson".
        """
        import json
        import requests
        import urllib.parse

#determines if the data argument is a file path, added try to avoid url error
        if isinstance(data, str):
            url = urllib.parse.urlparse(data)
            if url.scheme in ('http', 'https'):
                response = requests.get(data)
                data = response.json()
            else:
                try:
                    with open(data) as f:
                        data = json.load(f)
                except FileNotFoundError:
                    # try: 
                    data = json.loads(data)
                    # except json.JSONDecodeError:
                    #     response = requests.get(data)
                    #     data = response.json()

        if "style" not in kwargs:
          kwargs['style'] = {
              "color": "green",
              "weight": 1,
              "fillColor": "ff0000",
              "fillOpacity": 0.0
          }

        if "hover_style" not in kwargs:
            kwargs['hover_style'] = {
                "fillColor": "#ff0000",
                "fillOpacity": 0.5
            }

        layer = ipyleaflet.GeoJSON(data=data, name=name, **kwargs)
        self.add(layer)

    def add_shp(self, data, name="shp", **kwargs):
        """
        Adds a shapefile to the current map.

        Args:
            data (str or dict): The path to the shapefile as a string, or a dictionary representing the shapefile.
            name (str, optional): The name of the layer. Defaults to "shp".
            **kwargs: Arbitrary keyword arguments.

        Raises:
            TypeError: If the data is neither a string nor a dictionary representing a shapefile.

        Returns:
            None
        """
        import shapefile
        import json

        if isinstance(data, str):
            with shapefile.Reader(data) as shp:
                data = shp.__geo_interface__

        self.add_geojson(data, name, **kwargs)
    
    def add_image(self, url, bounds, name="image", **kwargs):
        """
        Adds an image to the current map.

        Args:
            url (str): The URL of the image.
            bounds (list): The bounds of the image.
            name (str, optional): The name of the image. Defaults to "image".
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        import ipyleaflet

        image = ipyleaflet.ImageOverlay(url=url, bounds=bounds, name=name, **kwargs)
        self.add_layer(image)

    def add_raster(self, data, name="raster", zoom_to_layer=True, **kwargs):
        """Adds a raster layer to the map.

        Args:
            data (str): The path to the raster file.
            name (str, optional): The name of the layer. Defaults to "raster".
        """

        try:
            from localtileserver import TileClient, get_leaflet_tile_layer
        except ImportError:
            raise ImportError("Please install the localtileserver package.")

        client = TileClient(data)
        layer = get_leaflet_tile_layer(client, name=name, **kwargs)
        self.add(layer)

        if zoom_to_layer:
            self.center = client.center()
            self.zoom = client.default_zoom
    def add_zoom_slider(self):
        """
        Adds a zoom slider to the map.
        """
        from ipyleaflet import WidgetControl

        zoom_slider = ipyleaflet.ZoomControl(position='topright')
        self.add_control(zoom_slider)




#construct slider and control in the source code, embed as a method in the Map class
#thebeans ideas - change detection from ifsar data for drawn extent, output statistics
    def add_opacity_slider(self, layer):
        """
        Adds an opacity slider to the map.

        Args:
            layer (object): The layer to which the opacity slider will be applied.
        """
        from ipywidgets import IntSlider, jslink, VBox

        layer = self.layers[layer_index]
        opacity_slider = widgets.FloatSlider(description='Opacity:', min=0, max=100, value=layer.opacity)
        #jslink((opacity_slider, 'value'), (layer, 'opacity'))
        #want to use observe because more universal than jslink

        control = WidgetControl(widget=opacity_slider, position='topright')
        self.add_control(control)
        
        def update_opacity(change):
            self.layer[layer.index].opacity, "value"
        opacity_slider.observe(update_opacity, 'value')


def add_basemap_gui(self, basemaps=None, postition = 'topright'):
    """
    Adds a basemap selector to the map.

    Args:
        basemaps (dict, optional): A dictionary of basemaps. Defaults to None.
        postition (str, optional): The position of the basemap selector. Defaults to 'topright'.
    """
    from ipywidgets import Dropdown
    from ipyleaflet import WidgetControl

    if basemaps is None:
        basemaps = {
            "OpenStreetMap": basemaps.OpenStreetMap.Mapnik,
            "ESRI": basemaps.Esri.WorldImagery,
            "Strava": basemaps.Strava.All,
            "OpenTopoMap": basemaps.OpenTopoMap.Standard
}

    dropdown = Dropdown(options=basemaps, description='Basemap:')
    control = WidgetControl(widget=dropdown, position=position)
    self.add_control(control)

    def on_click(change):
        basemap = change['new']
        self.layers = self.layers[:1]
        self.add_basemap(basemap)

    dropdown.observe(on_click, 'value')