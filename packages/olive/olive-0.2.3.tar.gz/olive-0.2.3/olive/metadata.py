import requests
from requests_aws4auth import AWS4Auth
import boto3
from botocore import exceptions


class GetMetadata:
    def __init__(self):
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
        current_attributes = requests.get('{endpoint}/{mmsi}'.format(endpoint=self.attributes_endpoint,
                                                                     mmsi=mmsi),
                                          auth=self.auth)

        if isinstance(current_attributes, str):
            return current_attributes

        else:
            attributes_json = current_attributes.json()

            if isinstance(attributes_json, list):
                return attributes_json[0]

            else:
                return attributes_json

    # Request 2: Get the timestamps associated with the current attributes for a specific vessel
    def get_timestamps(self, mmsi):
        timestamps = requests.get('{endpoint}/{mmsi}'.format(endpoint=self.timestamps_endpoint,
                                                             mmsi=mmsi),
                                  auth=self.auth)

        return timestamps.json()

    # Request 3: Get the change log* for a specific attribute of a specific vessel, within a specified date range
    def get_changelog(self, mmsi, attribute, date_start=None, date_end=None):
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

        return changelog.json()
