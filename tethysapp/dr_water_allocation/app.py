from tethys_sdk.base import TethysAppBase, url_map_maker


class DrWaterAllocation(TethysAppBase):
    """
    Tethys app class for DR Water Allocation.
    """

    name = 'DR Water Allocation'
    index = 'dr_water_allocation:home'
    icon = 'dr_water_allocation/images/flag-waving-250.png'
    package = 'dr_water_allocation'
    root_url = 'dr-water-allocation'
    color = '#98a50d'
    description = 'Shows different water distribution scenarios'
    tags = 'DR'
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='dr-water-allocation',
                controller='dr_water_allocation.controllers.home'
            ),
            UrlMap(
                name='results',
                url='dr-water-allocation/results',
                controller='dr_water_allocation.controllers.results'
            ),
        )

        return url_maps
