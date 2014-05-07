"""
Moodstocks API Client
---------------------

- Copyright (C) 2014 by Moodstocks SAS.
- Licensed under MIT/X11
- See https://moodstocks.com/ for more information.

"""

DEFAULT_EP = "http://api.moodstocks.com/v2"

from requests.auth import HTTPDigestAuth
import requests
import json
import os
import base64

version = '0.1'

codes = requests.codes


def b64_encode(s):
    """
    Encode input string with base64url safe without padding scheme.
    """
    return base64.urlsafe_b64encode(s).strip("=")


def b64_decode(s):
    """
    Decode input string with base64url safe without padding scheme.
    """
    mod = len(s) % 4
    if mod >= 2:
        s += (4 - mod) * "="
    return base64.urlsafe_b64decode(s)


class APIError(Exception):
    """
    An exception raised if the API returns an unexpected response.
    """

    def __init__(self, code, body):
        self.code = code
        self.body = body

    def __str__(self):
        return "%d - %s" % (self.code, self.body)


class APIClient:
    """
    Represents a Moodstocks HTTP API Client.
    """

    def __init__(self, api_key, api_secret, ep=None):
        """
        Constructor keyword arguments:

        :param api_key: a valid Moodstocks API key
        :param api_secret: a valid Moodstocks API secret

        .. note::

            You must first create a developer account on
            `Moodstocks <https://moodstocks.com/>`_ to obtain a valid API key /
            secret pair.
        """
        self.auth = HTTPDigestAuth(api_key, api_secret)
        self.ep = ep or DEFAULT_EP

    def _request(self, method, resource, files=None, params=None, **kwargs):
        """
        Internal method for HTTP requests.
        """
        url = self.ep + resource
        r = requests.request(
            method,
            url,
            params=params,
            files=files,
            auth=self.auth
        )

        if r.status_code != codes.ok:
            raise APIError(r.status_code, r.text)

        return r.json()

    def add_image(self, image_id, filename=None, image_url=None):
        """
        Index a reference image on your API key to make it searchable.

        :param image_id: reference image unique identifier.
        :param filename: full path to the image file
        :param image_url: remote image URL

        :return: a dict, e.g `{'id': 'my_id', 'is_update': False}`

        .. note::

            This operation makes your image available **only** through
            server-side search - see :func:`search_image`. To make it available
            on the client-side local image database - thanks to the
            `Moodstocks SDK <https://moodstocks.com/docs/>`_ - you must use
            :func:`make_image_offline`.
        """
        files = None
        if filename:
            with open(filename, 'rb') as f:
                files = {'image_file': ('ref.jpg', f.read())}

        params = None
        if image_url:
            params = {'image_url': image_url}

        return self._request(
            'PUT',
            '/ref/' + image_id,
            files=files,
            params=params
        )

    def remove_image(self, image_id):
        """
        Remove a reference image from your API key.

        :param image_id: reference image unique identifier

        :return: a dict, e.g `{'existed': False, 'id': 'my_id'}`
        """
        return self._request('DELETE', '/ref/' + image_id)

    def make_image_offline(self, image_id):
        """
        Flag a reference image as *offline*.

        Use this to make a reference image synchronizable and searchable
        on-device through the local image database thanks to the
        `Moodstocks SDK <https://moodstocks.com/docs/>`_.

        :param image_id: reference image unique identifier

        :return: a dict, e.g `{'was_offline': False, 'id': 'my_id'}`
        """
        return self._request('POST', '/ref/%s/offline' % image_id)

    def remove_image_offline(self, image_id):
        """
        Unflag an offline reference image.

        This does not completely remove the reference image, i.e it will remain
        searchable only through a server-side search.

        :param image_id: reference image unique identifier

        :return: a dict, e.g `{'was_offline': True, 'id': 'my_id'}`
        """
        return self._request('DELETE', '/ref/%s/offline' % image_id)

    def image_info(self, image_id):
        """
        Show the status of a given reference image.

        This method raises a :class:`APIError` if the corresponding reference
        image does not exist.

        :param image_id: reference image unique identifier

        :return: a dict, e.g `{'is_offline': True, 'id': 'my_id'}`
        """
        return self._request('GET', '/ref/%s' % image_id)

    def list_images(self, offline=False):
        """
        Get the global number of reference images available, as well as the
        list of their IDs.

        :param offline: whether to consider offline images only or not (default)

        :return: a dict, e.g `{'count': 3, 'ids': ['my_id', 'foo', 'bar']}`
        """
        if offline:
            return self._request('GET', '/stats/offline/refs')
        else:
            return self._request('GET', '/stats/refs')

    def search_image(self, filename=None, image_url=None):
        """
        Looking up an image using a server-side search (a.k.a online image
        recognition).

        :param filename: local image file's full path
        :param image_url: image's url

        :return: a dict, e.g `{'found': True, 'id': 'my_id'}` or `{'found': False}`
        """
        files = None
        if filename:
            with open(filename, 'rb') as f:
                files = {'image_file': ('qry.jpg', f.read())}

        params = None
        if image_url:
            params = {'image_url': image_url}

        return self._request(
            'POST',
            '/search',
            files=files,
            params=params
        )

    def echo(self, params=None):
        """
        Perform an echo request with optional parameters.

        :param params: optional query string parameters

        :return: a dict, e.g `{'http_verb': 'GET', 'results': {}}`
        """
        return self._request('GET', '/echo', params=params)
