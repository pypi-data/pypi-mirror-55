import requests
from requests_aws4auth import AWS4Auth
import boto3
import json
from botocore import exceptions


class GetMetadata:
    """ Makes requests to the AIS Metadata API, which fetches vessel data from the AIS Metadata Database, and returns
    those responses as json dictionaries.

    Methods
    -------
    get_current_attributes(mmsi)
        Returns the most current vessel attributes for a given MMSI
    get_timestamps(mmsi)
        Returns vessel attributes for a given MMSI with most recent timestamp for each attribute
    get_changelog(mmsi, attribute, date_start, date_end)
        Returns a list of records for each time a given attribute for a MMSI changed within the defined date range
    """

    def __init__(self):
        """
        Parameters
        ----------
        access_key : str
            AWS access key for the TA Solutions Alpha account
        secret_access_key : str
            AWS secret access key for the TA Solutions Alpha account
        auth : <class 'requests_aws4auth.aws4auth.AWS4Auth'>
            authorizes requests to AIS Metadata API
        attributes_endpoint : str
            API endpoint to get current vessel attributes
        timestamps_endpoint: str
            endpoint to get most recent timestamps for each attribute for a vessel
        changelog_endpoint : str
            API endpoint to get a log of all changes to an attribute for a vessel
        """
        try:
            session = boto3.Session(profile_name='alpha')

        except exceptions.ProfileNotFound:
            session = boto3.Session()

        access_key = session.get_credentials().access_key
        secret_access_key = session.get_credentials().secret_key
        self.auth = AWS4Auth(access_key, secret_access_key, 'us-east-1', 'execute-api')
        self.attributes_endpoint = 'https://zyqxnexqnf.execute-api.us-east-1.amazonaws.com/dev/vessels'
        self.timestamps_endpoint = 'https://zyqxnexqnf.execute-api.us-east-1.amazonaws.com/dev/timestamps'
        self.changelog_endpoint = 'https://zyqxnexqnf.execute-api.us-east-1.amazonaws.com/dev/changelog'

    # Request 1: Get the current attributes for a specific Vessel
    def get_current_attributes(self, mmsi):
        """ Gets the most recent vessel attributes for a given mmsi from the AIS Metadata API and returns those
         attributes in a json dictionary.

        Parameters
        ----------
        mmsi : str
            mmsi, or Maritime Mobile Service Identity, for vessel of interest

        Returns
        -------
        json dictionary
        """
        current_attributes = requests.get('{endpoint}/{mmsi}'.format(endpoint=self.attributes_endpoint,
                                                                     mmsi=mmsi),
                                          auth=self.auth)

        json_response = json.loads(current_attributes.content)

        try:
            current_attributes.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            print(json_response)

        if isinstance(json_response, str):
            return json_response

        else:
            return json_response[0]

    # Request 2: Get the timestamps associated with the current attributes for a specific vessel
    def get_timestamps(self, mmsi):
        """Gets the most recent timestamps for each attribute for a vessel and returns them in a json dictionary, where
        the key is the attribute and the value is the timestamp.

        Parameters
        ----------
        mmsi : str
            mmsi, or Maritime Mobile Service Identity, for vessel of interest

        Returns
        -------
        json dictionary
        """
        timestamps = requests.get('{endpoint}/{mmsi}'.format(endpoint=self.timestamps_endpoint,
                                                             mmsi=mmsi),
                                  auth=self.auth)

        json_response = json.loads(timestamps.content)

        try:
            timestamps.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            print(json_response)

        return json_response

    # Request 3: Get the change log* for a specific attribute of a specific vessel, within a specified date/time range
    def get_changelog(self, mmsi, attribute, date_start=None, date_end=None):
        """Returns a record for each time a selected attribute changed for a vessel within a given date/time range (if
        it changed). The changes will be returned as a list of of dictionaries, with the selected attribute as the key
        and the timestamp that the attribute changed as the value.

        Parameters
        ----------
        mmsi : str
            mmsi, or Maritime Mobile Service Identity, for vessel of interest
        attribute : str
            vessel attribute of interest, valid attributes: 'msg_type', 'imo', 'flag', 'vessel_name', 'vendor_id',
            'callsign', 'length', 'width', 'transponder_type', 'cargo_description'
        date_start : str, optional
            date/time to begin search for changes to an attribute, required format: %Y-%m-%dT%H:%M:%S
            (see http://strftime.org/), ex. '2019-09-10T10:00:00'
        date_end : str, optional
            date/time to end search for changes to an attribute, required format: %Y-%m-%dT%H:%M:%S
            (see http://strftime.org/), ex. '2019-09-10T10:00:00'
        Returns
        -------
        list of json dictionaries
        """
        if date_start and date_end:
            date_endpoint = 'from={date_start}&to={date_end}'.format(date_start=date_start,
                                                                     date_end=date_end)
        elif date_start:
            date_endpoint = 'from={date_start}'.format(date_start=date_start)

        elif date_end:
            date_endpoint = 'to={date_end}'.format(date_end=date_end)

        else:
            date_endpoint = None

        changelog_url = '{endpoint}/{mmsi}/{attribute}?{date_endpoint}'.format(endpoint=self.changelog_endpoint,
                                                                               mmsi=mmsi,
                                                                               attribute=attribute,
                                                                               date_endpoint=date_endpoint)

        changelog = requests.get(changelog_url,
                                 auth=self.auth)

        json_response = json.loads(changelog.content)

        try:
            changelog.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            print(json_response)

        if json_response:
            return json_response

        else:
            msg = "No change to {attribute} during defined date range".format(attribute=attribute)

            return msg
