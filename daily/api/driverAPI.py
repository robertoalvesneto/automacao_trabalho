from importlib.metadata import metadata
from importlib.resources import Resource
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


class DriverAPI:
    """
    API to handle google driver
    """
    

    def __init__(self) -> None:
        # If modifying these scopes, delete the file token.json.
        self.scopes = ['https://www.googleapis.com/auth/drive']
        self.drive_service = self.__connect()

    def __create_folder(self, folder_id: str, name: str) -> str:
        """
        Description:
        Create folder on correct father folder and return ID for new
        folder

        Parameters:
        :folder_id:   (str) id of parent
        :name:        (str) name of folder that will be created

        :return:    (str) id of folder
        """

        file_metadata = {
            'name': f'{name}',
            'parents': [folder_id],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.drive_service.files().create(body=file_metadata,
                                                 fields='id').execute()

        return file.get('id')

    def __upload_file(
            self, folder_id: str, name: str, file_path: str, file_type: str
    ) -> str:
        """
        Description:
        Upload a generic file for correct folder

        Parameters:
        :folder_id:   (str) id of folder to save file
        :name:        (str) name of file that will be created
        :file_path:   (str) path of file in my computer
        :file_type:   (str) (driver types) type of file

        :return:    (str) id of file
        """

        file_metadata = {
            'name': name,
            'parents': [folder_id]
        }

        media = MediaFileUpload(file_path,
                                mimetype=file_type)
        file = self.drive_service.files().create(body=file_metadata,
                                                 media_body=media,
                                                 fields='id').execute()

        return file.get('id')

    def __get_folder_id(self, name: str, folder_id: str = None) -> list:
        """
        Description:
        Get and return id of folder by name

        Parameters:
        :name:        (str) name of file that will be created
        :folder_id:   (str) id of parent folder

        :return:    (list[str, str]) text of status and id, if exist
        """
        
        metadata = f"mimeType = 'application/vnd.google-apps.folder' and name='{name}'"

        page_token = None
        while True:
            response = self.drive_service.files().list(q=metadata,
                                                       spaces='drive',
                                                       fields='nextPageToken, files(id, name)',
                                                       pageToken=page_token).execute()
            for file in response.get('files', []):
                return 'success', file.get('id')
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        return 'dont found', None

    def __connect(self) -> Resource:
        """
        Description:
        Connect to my google driver using credentials.json file in first
        entry or token.json in the others.

        :return:    (Resource) connection object
        """
        creds = None

        if os.path.exists('api/token.json'):
            creds = Credentials.from_authorized_user_file(
                'api/token.json', self.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'api/credentials.json', self.scopes)
                creds = flow.run_local_server(port=0)
            with open('api/token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('drive', 'v3', credentials=creds)

            return service
        except HttpError as error:
            raise Exception(f'An error occurred: {error}')

    def upload_image(self, folder_name, image_name, image_path):
        """
        Description:
        Get and return id of folder by name

        Parameters:
        :image_name:    (str) name of file that will be created
        :folder_name:   (str) name of folder to add an image. If this
                        folder doesn't exist, it will be created
        :image_path:    (str) path of image file
        """
        status, folder_id = self.__get_folder_id('registros daily')

        if status == 'success':
            status2, folder_id2 = self.__get_folder_id(folder_name)
            if status2 == 'success':
                self.__upload_file(folder_id2,
                                   image_name, image_path, 'image/jpeg')
            else:
                folder_id = self.__create_folder(folder_id, folder_name)
                self.__upload_file(folder_id,
                                   image_name, image_path, 'image/jpeg')
        else:
            raise Exception('Folder dont found')