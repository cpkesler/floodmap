from tethys_sdk.base import TethysAppBase, url_map_maker


class Floodmap(TethysAppBase):
    """
    Tethys app class for floodmap.
    """

    name = 'floodmap'
    index = 'floodmap:home'
    icon = 'floodmap/images/flood.jpg'
    package = 'floodmap'
    root_url = 'floodmap'
    color = '#2ecc71'
    description = 'Place a brief description of your app here.'
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