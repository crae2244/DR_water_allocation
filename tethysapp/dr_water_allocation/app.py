from tethys_sdk.base import TethysAppBase, url_map_maker


class DrWaterAllocation(TethysAppBase):
    """
    Tethys app class for DR Water Allocation.
    """

    name = 'DR Water Allocation'
    index = 'dr_water_allocation:home'
    icon = 'dr_water_allocation/images/icon.gif'
    package = 'dr_water_allocation'
    root_url = 'dr-water-allocation'
    color = '#5575e8'
    description = 'Shows effects of different water distribution scenarios'
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
        )

        return url_maps