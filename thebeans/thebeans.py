"""Main module."""
#creating a new ipyleaflet class for deploymnet
#This doc shows you how the package was built. This is where you build code 
#make sure the packages are installed in your environment

#For Ipyleaflet and Ipywidgets
import ipyleaflet
from ipyleaflet import Map, basemaps, Marker, WidgetControl
import ipywidgets as widgets
from ipywidgets import Layout



class Map(ipyleaflet.Map):
    """Map class that inherits from ipyleaflet.Map.

    Args:
        ipyleaflet (Map): The ipyleaflet.Map class.
    """    
    def __init__(self, basemap = "OpenStreetMap", center = (0,0), zoom = 1, **kwargs):
        """Initialize the map.

        Args:
            center (list, optional): Set the center of the map. Defaults to WA [47.7511, -120.7401].
            zoom (int, optional): Set the zoom level of the map. Defaults to 6.
        """
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        #add layer control not as straight forward. Need to pass to an object and consider it as a parameter that you can pass. Ipyleaflet doesn't support.
        
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        if "add_layer_control" not in kwargs:
            layer_control_flag = True
        else:
            layer_control_flag = kwargs["add_layer_control"]
        kwargs.pop("add_layer_control", None)

        super().__init__(center=center, zoom=zoom, **kwargs)
        if layer_control_flag:
            self.add_layers_control()

        #self.add_toolbar()


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



    
    def add_geojson(self, data, name="geojson", **kwargs):
        """Adds a GeoJSON layer to the map.

        Args:
            data (str | dict): The GeoJSON data as a string or a dictionary.
            name (str, optional): The name of the layer. Defaults to "geojson".
        """
        

        if isinstance(data, str):
            with open(data) as f:
                data = json.load(f)

        if "style" not in kwargs:
            kwargs["style"] = {"color": "blue", "weight": 1, "fillOpacity": 0}

        if "hover_style" not in kwargs:
            kwargs["hover_style"] = {"fillColor": "#ff0000", "fillOpacity": 0.5}

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



    # def add_vector(self, data, name = "vector", **kwargs):
    #     """Adds a vector layer to the map.

    #     Args:
    #         data (str): The path to the vector file.
    #         name (str, optional): The name of the layer. Defaults to "vector".
    #     """
    #     import geopandas as gpd
    #     if isinstance(data, str):


    # def add_vector(self, data, name="vector", **kwargs):
    #     """
    #     Adds a vector data layer to the map.

    #     Parameters:
    #         data (str or GeoDataFrame): The vector data to be added. It can be either a file path to a vector data file (GeoJSON, shapefile, etc.) or a GeoDataFrame object.
    #         name (str): The name of the vector data layer. Default is "vector".
    #         **kwargs: Additional keyword arguments to pass to the add_geojson() method.

    #     Raises:
    #         None

    #     Returns:
    #         None
    #     """
    #     if isinstance(data, str):
    #         try:
               
    #             vector_data = gpd.read_file(data)
    #         except Exception as e:
    #             print(f"Error reading vector data from file: {e}")
    #             return
    #     elif isinstance(data, gpd.GeoDataFrame):
           
    #         vector_data = data
    #     else:
    #         print("Unsupported vector data format.")
    #         return

        
    #     geojson_data = vector_data.__geo_interface__

      
    #     self.add_geojson(geojson_data, name, **kwargs)
    


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

        image = ipyleaflet.ImageOverlay(url=url, bounds=bounds, name="image", **kwargs)
        self.add_layer(image)



    def add_raster(self, data, name="raster", zoom_to_layer=True, **kwargs):
        """Adds a raster layer to the map.

        Args:
            data (str): The path to the raster file.
            name (str, optional): The name of the layer. Defaults to "raster".
        """
        import localtileserver
        
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




    def add_widget(self, widget, position="topright"):
        """Adds a widget to the map.

        Args:
            widget (object): The widget to be added.
            position (str, optional): The position of the widget. Defaults to "topright".
        """
        control = ipyleaflet.WidgetControl(widget=widget, position=position)
        self.add(control)




    def add_opacity_slider(
         self, layer_index=-1, description="Opacity", position="topright"
    ):
        """Adds an opacity slider to the map.

        Args:
            layer (object): The layer to which the opacity slider is added.
            description (str, optional): The description of the opacity slider. Defaults to "Opacity".
            position (str, optional): The position of the opacity slider. Defaults to "topright".
        """
        layer = self.layers[layer_index]
        opacity_slider = widgets.FloatSlider(
            description=description,
            min=0,
            max=1,
            value=layer.opacity,
            style={"description_width": "initial"},
        )

        def update_opacity(change):
            layer.opacity = change["new"]

        opacity_slider.observe(update_opacity, "value")

        control = ipyleaflet.WidgetControl(widget=opacity_slider, position=position)
        self.add(control)






    #basemap dropdown menu widget and behavior
    def add_basemap_gui(self, basemaps=None, position="topright"):
        """Adds a basemap GUI to the map.

        Args:
            position (str, optional): The position of the basemap GUI. Defaults to "topright".
        """
        #Creates list of all available basemaps for selection, many KeyErrors
        # from ipyleaflet import basemaps as base

        # options = []

        # for i in base:
        #     options.append(i)

        #dropdown gizmo
        basemap_selector = widgets.Dropdown( 
            options= [
                "OpenStreetMap",
                "OpenTopoMap",
                "Esri.WorldImagery",
                "Esri.NatGeoWorldMap",
                "NASAGIBS.ModisTerraTrueColorCR",
                "NASAGIBS.ModisTerraBands367CR",
                "NASAGIBS.ModisTerraBands721CR",
                "NASAGIBS.ModisAquaTrueColorCR",
                "NASAGIBS.ModisAquaBands721CR",
                "NASAGIBS.ViirsEarthAtNight2012",
            ],
            value = "OpenStreetMap",
            description="Basemap",
        )

        #close button for dropdown menu
        close_button = widgets.Button(
            description= "",
            button_style = "primary",
            tooltip = "Dropdown Toggle",
            icon = "times",
            layout = Layout(width ="35px") #less than 35 add noise
        )
        
        basebox = widgets.HBox([basemap_selector, close_button]) #widget box

        #actions for buttons and button control
        def on_click(change):
            self.add_basemap(change["new"])
        basemap_selector.observe(on_click, "value")

        def close_click(change):
            basemap_selector.close()
            close_button.close()
    

        close_button.on_click(close_click)


        control = ipyleaflet.WidgetControl(widget=basebox, position=position)
        self.add(control)





    def add_toolbar(self, position="topright"): #add toolbar functionality, basemap gui button, how keep toolbar from disappearing, remove basemap widget
        """Adds a toolbar to the map.

        Args:
            position (str, optional): The position of the toolbar. Defaults to "topright".
        """

        padding = "0px 0px 0px 5px"  # upper, right, bottom, left

        toolbar_button = widgets.ToggleButton(
            value=False,
            tooltip="Toolbar",
            icon="wrench",
            layout=widgets.Layout(width="28px", height="28px", padding=padding),
        )

        close_button = widgets.ToggleButton(
            value=False,
            tooltip="Close the tool",
            icon="times",
            button_style="primary",
            layout=widgets.Layout(height="28px", width="28px", padding=padding),
        )

        toolbar = widgets.VBox([toolbar_button])


        def close_click(change):
            if change["new"]:
                toolbar_button.close()
                close_button.close()
                toolbar.close()

        close_button.observe(close_click, "value")

        rows = 2
        cols = 2
        grid = widgets.GridspecLayout(
            rows, cols, grid_gap="0px", layout=widgets.Layout(width="65px")
        )

        icons = ["folder-open", "map", "info", "question"]

        for i in range(rows):
            for j in range(cols):
                grid[i, j] = widgets.Button(
                    description="",
                    button_style="primary",
                    icon=icons[i * rows + j],
                    layout=widgets.Layout(width="28px", padding="0px"),
                )


        #click signal to backend/frontend
        def on_click(change):
            if change["new"]:
                toolbar.children = [widgets.HBox([close_button, toolbar_button]), grid]
            else:
                toolbar.children = [toolbar_button]

        toolbar_button.observe(on_click, "value")
        toolbar_ctrl = WidgetControl(widget=toolbar, position="topright")
        self.add(toolbar_ctrl)

        #output widget confirming button click
        output = widgets.Output()
        output_control = WidgetControl(widget=output, position="bottomright")
        self.add(output_control)





        def toolbar_callback(change): #links to actions to buttons,
            if change.icon == "folder-open":
                with output:
                    output.clear_output()
                    print(f"You can open a file")
            elif change.icon == "map":
                self.add_basemap_gui() #call basemap selector
                with output:
                    output.clear_output()
                    print("change the basemap")
            elif change.icon == "info":
                with output:
                    output.clear_output()
                    print("There is no info here.")
            elif change.icon == "question":
                with output:
                    output.clear_output()
                    print("There is no help here.")
            else:
                with output:
                    output.clear_output()
                    print(f"Icon: {change.icon}")

        for tool in grid.children:
            tool.on_click(toolbar_callback)




# # output of output_control?
#     def add_textbox(self, **kawrgs) #want dec deg output for selected area/marker
#         def handle_interactions(**kwargs):
#             latlon = kwargs.get('coordinates')
#             latlon = [round(x,4) for x in latlon]
#             if kwargs.get("type") == "click":
#                 with textbox:
#                     textbox.clear_output()
#                     print(f"Coordinates: {latlon}")
#             self.on_interaction(handle_interactions)

#         textbox = widgets.Output()

#         with textbox:
#             textbox.clear_output()

            
#             display(textbox)



