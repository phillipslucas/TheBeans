import folium

class Map(folium.Map):
    def __init__(self, center = [20,0], zoom = 2, **kwargs):
        super().__init__(location=center, zoom_start = zoom, **kwargs)



#the whole point is to adapt conventions in case one package doesn't work in a given area. if ipyleaflet doesn't work then you can import the thebeans.foliummap module
# copy in modules for original module and adapt in this module
# can export maps to .html and add to any website server
    
#folium doesn't allow widgets but when you render a html can use widgets outside map

    
    def add_raster(self, data, name="raster", **kwargs):
            """Adds a raster layer to the map.

            Args:
                data (str): The path to the raster file.
                name (str, optional): The name of the layer. Defaults to "raster".
            """
            import localtileserver
            
            try:
                from localtileserver import TileClient, get_folium_tile_layer
            except ImportError:
                raise ImportError("Please install the localtileserver package.")

            client = TileClient(data)
            layer = get_folium_tile_layer(client, name=name, **kwargs)
            self.add(layer)

            if zoom_to_layer:
                self.center = client.center()
                self.zoom = client.default_zoom