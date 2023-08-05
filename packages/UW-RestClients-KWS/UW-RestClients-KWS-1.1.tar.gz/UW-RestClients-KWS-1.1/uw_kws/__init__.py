"""
This is the interface for interacting with the Key Web Service.
"""

from restclients_core.exceptions import DataFailureException
from uw_kws.dao import KWS_DAO
from uw_kws.models import Key
import json

ENCRYPTION_KEY_URL = "/key/v1/encryption/{}.json"
ENCRYPTION_CURRENT_KEY_URL = "/key/v1/type/{}/encryption/current.json"


class KWS(object):
    """
    The KWS object has methods for getting key information.
    """
    def _get_resource(self, url, headers={}):
        headers["Accept"] = "application/json"

        response = KWS_DAO().getURL(url, headers)

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def get_key(self, key_id=None, url=None):
        """
        Returns a restclients.Key object for the given key ID or URL. If the
        key isn't found, or if there is an error communicating with the
        KWS, a DataFailureException will be thrown.
        """
        if key_id is not None:
            url = ENCRYPTION_KEY_URL.format(key_id)
        elif url is None:
            raise TypeError('URL is None')
        return Key.from_json(self._get_resource(url))

    def get_current_key(self, resource_name):
        """
        Returns a restclients.Key object for the given resource.  If the
        resource isn't found, or if there is an error communicating with the
        KWS, a DataFailureException will be thrown.
        """
        url = ENCRYPTION_CURRENT_KEY_URL.format(resource_name)
        return Key.from_json(self._get_resource(url))
