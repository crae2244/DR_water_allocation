from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import Button
from tethys_sdk.gizmos import MapView, MVDraw, MVView, MVLayer, MVLegendClass

@login_required()
def home(request):
    """
    Controller for the app home page.
    """

    next_button = Button(
        display_text='Next',
        name='next-button',
        attributes={
            'data-toggle':'tooltip',
            'data-placement':'top',
            'title':'Next'
        }
    )

    view_options = MVView(
        projection='EPSG:4326',
        center=[-100, 40],
        zoom=3.5,
        maxZoom=18,
        minZoom=2
    )

    map_view_options = MapView(
        height='600px',
        width='100%',
        controls=['ZoomSlider', 'Rotate', 'FullScreen',
                  {'MousePosition': {'projection': 'EPSG:4326'}},
                  {'ZoomToExtent': {'projection': 'EPSG:4326', 'extent': [-130, 22, -65, 54]}}],
        view=view_options,
        basemap='OpenStreetMap',
        legend=True
    )

    context = {
        'next_button': next_button,
        'map_view_options': map_view_options,
    }

    return render(request, 'dr_water_allocation/home.html', context)