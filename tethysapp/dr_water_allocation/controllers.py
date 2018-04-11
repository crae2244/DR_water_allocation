from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import Button
from tethys_sdk.gizmos import MapView, MVView, MVLayer, MVLegendClass
from model import read_points_from_csv

@login_required()
def home(request):
    """
    Controller for the app home page.
    """

    next_button = Button(
        display_text='Compute',
        name='next-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'next'
        }
    )

    diversion_points_list = read_points_from_csv()
    features = []

    for item in diversion_points_list:
        diversion_point_feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [item[2], item[3]],
            },
            'properties':{
                'point_name':[item[0]],
                'demand':[item[1]],
                'efficiency':[.6],
                'priority':'High'
            }
        }
        features.append(diversion_point_feature)

    diversion_points_collection = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': features,
    }

    geojson_diversion_point_layer = MVLayer(
        source='GeoJSON',
        options=diversion_points_collection,
        legend_title="Diversion Points",
        feature_selection=True,
        layer_options={
            'style': {
                'image': {
                    'circle': {
                        'radius': 6,
                        'fill': {'color': '#d84e1f'},
                        'stroke': {'color': '#ffffff', 'width': 1},
                    }
                }
            }
        }
    )
    print geojson_diversion_point_layer
    view_options = MVView(
        projection='EPSG:4326',
        center=[-70.8, 18.56],
        zoom=10,
        maxZoom=18,
        minZoom=2
    )

    map_view_options = MapView(
        height='100%',
        width='100%',
        controls=[ 'Rotate', 'FullScreen',
                  {'MousePosition': {'projection': 'EPSG:4326'}},
                  {'ZoomToExtent': {'projection': 'EPSG:4326', 'extent': [-130, 22, -65, 54]}}],
        layers=[geojson_diversion_point_layer],
        view=view_options,
        basemap='OpenStreetMap',
    )

    context = {
        'next_button': next_button,
        'map_view_options': map_view_options,
    }

    return render(request, 'dr_water_allocation/home.html', context)