import os
import requests
import json
import pandas as pd
from io import StringIO


class Sharepoint():
    def __init__(self, site, sharepoint_directory, token_directory, site_id, tenant_id, client_id, client_secret):
        """
        :param site: site resource provides the metadata and relationships for a Sharepoint site. e.g. companyname.sharepoint.com
        :param sharepoint_directory: storage location of the to be uploaded file
        :param token_directory: location of the stored tokens that are needed to refresh the access token
        :param site_id: The unique identifier (guid) for the item's site collection. So the id accompanying the aforementioned site.
        :param tenant_id: currently authenticated organization, which is defined as a collection of exactly one record.
        :param client_id: used to identify the application. When building an App that would like to access Sharepoint APIs; register the app and it will give you a client ID.
        :param client_secret: True secret key, which is stored on server side securely and not available to the public.
        """
        self.site = site
        self.sharepoint_directory = sharepoint_directory
        self.token_directory = token_directory
        self.siteid = site_id
        self.tenantid = tenant_id
        self.clientid = client_id
        self.clientsecret = client_secret

    def get_access_token(self):
        """
        This method is used to retrieve the access token needed to be able to upload files to sharepoint.
        Refresh token is needed to be able to refresh the access token when needed.
        :return: returns the access token that can be used for file retrieval and uploads
        """
        if not os.path.exists(f'{self.token_directory}'):
            refresh_token = input('refresh_token: ')
        else:
            with open(f'{self.token_directory}', 'r') as file:
                tokens = file.read()
                tokens = json.loads(tokens)
                refresh_token = tokens['refresh_token']
        url_tokens = f'https://login.microsoftonline.com/{self.tenantid}/oauth2/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        body = {
            "grant_type": "refresh_token",
            "client_id": self.clientid,
            "client_secret": self.clientsecret,
            "refresh_token": refresh_token
        }
        response = requests.post(url=url_tokens, headers=headers, data=body)
        token = response.json()
        if 200 <= response.status_code < 300:
            with open(f'{self.token_directory}', 'w') as f:
                json.dump(token, f)
        else:
            raise Exception('Got status_code {response.status_code} from sharepoint')
        return token['access_token']

    def get_driveid(self):
        """
        This method is used to derive the driveid to which the files have to be uploaded. Needed in the upload url for file upload.
        :return: returns the needed driveid
        """
        access_token = self.get_access_token()
        url = f'https://graph.microsoft.com/v1.0/sites/{self.site},{self.siteid}/drives'
        headers = {'Authorization': f'Bearer {access_token}'}
        driveid = requests.get(url, headers=headers).json()['value'][0]['id']
        return driveid

    def upload_files(self, filename, documentlibrary):
        """
        This method performs the actual file upload to the formerly derived site + drive.
        filename: name of the file to be uploaded. For example test.csv
        documentlibrary: folder on sharepoint where it can be found. For example: Documenten or UploadFiles
        :return: File uploaded to sharepoint drive
        """
        access_token = self.get_access_token()
        driveid = self.get_driveid()
        url = f'https://graph.microsoft.com/v1.0/sites/{self.site},{self.siteid}/drives/{driveid}/root:/{documentlibrary}/{filename}:/createUploadSession'
        headers = {'Authorization': f'Bearer {access_token}'}
        upload_url = requests.post(url, headers=headers).json()['uploadUrl']

        with open(f'{self.sharepoint_directory}/{filename}', 'rb') as file_input:
            file_bytes = os.path.getsize(f'{self.sharepoint_directory}/{filename}')
            headers_upload = {'Content-Type': 'application/json',
                              'Content-Length': f'{file_bytes}',
                              'Content-Range': f'bytes 0-{file_bytes - 1}/{file_bytes}'}
            response_upload = requests.put(url=upload_url, headers=headers_upload, data=file_input)
            return response_upload

    def download_files(self, filename, documentlibrary):
        """
        This method can be used to download an existing file from Sharepoint into a pandas dataframe that can be used
        and manipulated in python.
        :param filename: name of the file that you want to download
        :param documentlibrary: name of the document library in Sharepoint where this file can be found. For example, when the driveid
        refers to a given drive like Documenten binnen BI, and the to be downloaded
        :return:
        """
        access_token = self.get_access_token()
        driveid = self.get_driveid()
        url = f'https://graph.microsoft.com/v1.0/sites/{self.site},{self.siteid}/drives/{driveid}/root:/{documentlibrary}/{filename}'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(url=url, headers=headers)
        download_url = response.json()['@microsoft.graph.downloadUrl']

        response_download = requests.get(url=download_url, headers=headers)
        response_text = response_download.text
        df = pd.read_csv(StringIO(response_text), sep=';')
        return df
