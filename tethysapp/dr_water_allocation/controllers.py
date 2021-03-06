from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import Button, DataTableView
from tethys_sdk.gizmos import MapView, MVView, MVLayer, MVLegendClass
from model import get_all_dams, get_all_diversions, DiversionPoints, Dams
from django.http import HttpResponse
from sqlalchemy.orm import sessionmaker
from django.views.decorators.csrf import csrf_exempt
import json

from .app import DrWaterAllocation as app
import json

@login_required()
def home(request):
    """
    Controller for the app home page.
    """

    compute_button = Button(
        display_text='Calcular',
        name='compute-button',
        href=reverse('dr_water_allocation:results'),
        attributes={
            "onclick": compute_water()
        }
    )

    diversion_points_list = get_all_diversions()
    dam_list = get_all_dams()
    features = []
    features_dam = []

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
                'priority':item.priority,
                'type':'diversion'
            }
        }
        features.append(diversion_point_feature)

    for item in dam_list:
        dam_point_feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [item.latitude, item.longitude],
            },
            'properties':{
                'point_name':item.name,
                'output': item.output,
                'type': 'dam'
            }
        }
        features_dam.append(dam_point_feature)

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

    dam_points_collection = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': features_dam,
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

    geojson_dam_point_layer = MVLayer(
        source='GeoJSON',
        options=dam_points_collection,
        legend_title="Diversion Points",
        feature_selection=True,
        layer_options={
            'style': {
                'image': {
                    'circle': {
                        'radius': 6,
                        'fill': {'color': '#f9f32f'},
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
        layers=[geojson_diversion_point_layer, geojson_dam_point_layer],
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
        display_text='Atras',
        name='back-button',
        href=reverse('dr_water_allocation:home'),
    )
    diversion_points_list = get_all_diversions()
    points_in_table = []
    for item in diversion_points_list:
        if item.priority == 1:
            priority = 'High'
        elif item.priority == 2:
            priority = 'Medium'
        else:
            priority = 'Low'

        if item.water_diverted > 0:
            percent_demand = int((item.demand / item.water_diverted)*100)
        else:
            percent_demand = 0

        table_entry = (
            item.name,
            item.demand,
            priority,
            item.efficiency,
            item.water_diverted,
            percent_demand
        )
        points_in_table.append(table_entry)

    datatable_results = DataTableView(
        column_names=('Nombre', 'Demanda', 'Prioridad', 'Eficiencia', 'Agua Recibida', 'Por Ciento'),
        rows=points_in_table,
        searching=False,
        orderClasses=False,
    )

    context = {
        'back_button': back_button,
        'datatable_results': datatable_results,
    }
    return render(request, 'dr_water_allocation/results.html', context)


def update_persistent_store_point(request):
    place_name_ajax = request.POST.get('place_name')
    demand_ajax = request.POST.get('demand')
    priority_ajax = request.POST.get('priority')
    efficiency_ajax = request.POST.get('efficiency')

    Session = app.get_persistent_store_database('main_db', as_sessionmaker=True)
    session = Session()

    target = session.query(DiversionPoints).filter_by(name=place_name_ajax).first()

    target.demand = demand_ajax
    target.priority = priority_ajax
    target.efficiency = efficiency_ajax

    session.commit()
    session.close()

    return HttpResponse('Changes Made')

def update_persistent_store_dam(request):
    place_name_ajax = request.POST.get('place_name')
    output_ajax = request.POST.get('output')

    Session = app.get_persistent_store_database('main_db', as_sessionmaker=True)
    session = Session()

    target = session.query(Dams).filter_by(name=place_name_ajax).first()

    target.output = output_ajax

    session.commit()
    session.close()

    return HttpResponse('Changes Made')


def compute_water():

    # Algorithm diverting the waters based on demand and priority

    Session = app.get_persistent_store_database('main_db', as_sessionmaker=True)
    session = Session()

    dams = get_all_dams()
    diversions = get_all_diversions()

    total_supply = 0
    total_demand = 0
    demand_1 = 0
    demand_2 = 0
    demand_3 = 0

    for dam in dams:
        total_supply += dam.output

    print total_supply

    for diversion in diversions:
        if diversion.priority == 1:
            demand_1 += diversion.demand
        elif diversion.priority == 2:
            demand_2 += diversion.demand
        else:
            demand_3 += diversion.demand
        total_demand += diversion.demand

    print "subdemand"
    print demand_1
    print demand_2
    print demand_3

    print total_demand

    if total_supply > total_demand:

        print "Enough Water"

        for diversion in diversions:
            target = session.query(DiversionPoints).filter_by(name=diversion.name).first()
            target.water_diverted = diversion.demand
        session.commit()

    else:

        print "Water Shortage"
        if total_supply < demand_1:
            for diversion in diversions:
                if diversion.priority == 1:
                    #point gets portion of remaining water
                    proportionate_allocation = total_supply/demand_1
                    target = session.query(DiversionPoints).filter_by(name=diversion.name).first()
                    target.water_diverted = diversion.demand * proportionate_allocation

                elif diversion.priority == 2:
                    target = session.query(DiversionPoints).filter_by(name=diversion.name).first()
                    target.water_diverted = 0

                else:
                    target = session.query(DiversionPoints).filter_by(name=diversion.name).first()
                    target.water_diverted = 0
        elif (total_supply > demand_1) and (total_supply < (demand_1+demand_2)):
            for diversion in diversions:
                if diversion.priority == 1:
                    target = session.query(DiversionPoints).filter_by(name=diversion.name).first()
                    target.water_diverted = target.water_diverted = diversion.demand

                elif diversion.priority == 2:
                    # point gets portion of remaining water
                    proportionate_allocation = (total_supply- demand_1)/demand_2
                    target = session.query(DiversionPoints).filter_by(name=diversion.name).first()
                    target.water_diverted = diversion.demand * proportionate_allocation

                else:
                    target = session.query(DiversionPoints).filter_by(name=diversion.name).first()
                    target.water_diverted = 0
        else:
            for diversion in diversions:
                if diversion.priority == 1:
                    proportionate_allocation = total_supply / demand_1
                    target = session.query(DiversionPoints).filter_by(name=diversion.name).first()
                    target.water_diverted = target.water_diverted = proportionate_allocation * diversion.demand

                elif diversion.priority == 2:
                    target = session.query(DiversionPoints).filter_by(name=diversion.name).first()
                    target.water_diverted = diversion.demand

                else:
                    # point gets portion of remaining water"
                    target = session.query(DiversionPoints).filter_by(name=diversion.name).first()
                    target.water_diverted = 0
    session.commit()
    session.close()

