from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import Button, DataTableView
from tethys_sdk.gizmos import MapView, MVView, MVLayer, MVLegendClass
from model import get_all_dams, get_all_diversions

@login_required()
def home(request):
    """
    Controller for the app home page.
    """

    compute_button = Button(
        display_text='Compute',
        name='compute-button',
        href=reverse('dr_water_allocation:results'),
    )

    diversion_points_list = get_all_diversions()
    features = []

    for item in diversion_points_list:
        diversion_point_feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [item.latitude, item.longitude],
            },
            'properties':{
                'point_name':item.name,
                'demand':item.demand,
                'efficiency':item.efficiency,
                'priority':item.priority
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
        controls=['Rotate', 'FullScreen',
                  {'MousePosition': {'projection': 'EPSG:4326'}},
                  {'ZoomToExtent': {'projection': 'EPSG:4326', 'extent': [-130, 22, -65, 54]}}],
        layers=[geojson_diversion_point_layer],
        view=view_options,
        basemap='OpenStreetMap',
    )

    context = {
        'compute_button': compute_button,
        'map_view_options': map_view_options,
    }

    return render(request, 'dr_water_allocation/home.html', context)


def results(request):

    back_button = Button(
        display_text='Back',
        name='back-button',
        href=reverse('dr_water_allocation:home'),
    )

    datatable_results = DataTableView(
        column_names=('Name', 'Demand', 'Priority', "Water Diverted"),
        rows=[('SanJuan', 4, 'High', 4)],
        searching=False,
        orderClasses=False,
    )

    context = {
        'back_button': back_button,
        'datatable_results': datatable_results,
    }
    return render(request, 'dr_water_allocation/results.html', context)