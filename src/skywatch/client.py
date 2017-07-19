
class Client():
    """ Main client interface to skywatch API """    

    def __init__(self, api_key=None, base_url='https://api.skywatch.co/'):
        """
        :param str api_key: API key to use. Defaults to environment variable.
        :param str base_url: The base URL to use. Optional, should not be needed.
        """
        #api_key = api_key or auth.find_api_key()
        #self.auth = api_key and auth.APIKey(api_key)
        #self.base_url = base_url


    def search(self, request):
        """ Searches the data endpoint
        :param request: see :ref:`api-search-request`
        :returns: :py:class:`skywatch.models.JSON`
        :raises skywatch.exceptions.APIException: On API error.
        """
        body = json.dumps(request)
        return None
