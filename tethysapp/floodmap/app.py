from tethys_sdk.base import TethysAppBase, url_map_maker


class Floodmap(TethysAppBase):
    """
    Tethys app class for floodmap.
    """

    name = 'Tuscaloosa HAND Flood Map'
    index = 'floodmap:home'
    icon = 'floodmap/images/flood.jpg'
    package = 'floodmap'
    root_url = 'floodmap'
    color = '#00BFFF'
    description = 'Display possible floods and flood forecasts for Tuscaloosa, Alabama.'
    enable_feedback = False
    feedback_emails = []

        
    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='floodmap',
                           controller='floodmap.controllers.home'),
        )

        return url_maps