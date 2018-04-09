from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import Button
from tethys_sdk.gizmos import MapView, MVView, MVLayer, MVLegendClass

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

    diversion_points = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': [
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [-70.8, 18.56]
                }
            },
        ]
    }

    geojson_diversion_point_layer = MVLayer(
        source='GeoJSON',
        options=diversion_points,
        legend_title="Diversion Points",
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
        legend=True
    )

    context = {
        'next_button': next_button,
        'map_view_options': map_view_options,
    }

    return render(request, 'dr_water_allocation/home.html', context)