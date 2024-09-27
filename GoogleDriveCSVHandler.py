import io
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

class GoogleDriveCSVHandler:
    def __init__(self, service_account_file, scopes):
        self.scopes = scopes
        self.service_account_file = service_account_file
        self.credentials = service_account.Credentials.from_service_account_file(
            self.service_account_file, scopes=self.scopes)
        self.service = build('drive', 'v3', credentials=self.credentials)
        self.file_id = None

    # List files on Google Drive
    def list_drive_files(self):
        results = self.service.files().list(
            pageSize=100, fields="nextPageToken, files(id, name)").execute()
        return results.get('files', [])

    # Find the file ID for a specific file by name
    def find_file_id(self, file_name):
        items = self.list_drive_files()
        for item in items:
            if item['name'] == file_name:
                self.file_id = item['id']
                return item['id']
        return None

    # Read the CSV file from Google Drive
    def read_csv(self, file_name):
        if self.find_file_id(file_name):
            request = self.service.files().get_media(fileId=self.file_id)
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()

            file_content.seek(0)
            return pd.read_csv(file_content)
        else:
            print(f"File '{file_name}' not found.")
            return None

    # Update the CSV file back to Google Drive
    def update_csv(self, df, file_name):
        if self.file_id:
            # Save DataFrame to a temporary local CSV file
            temp_file_path = 'temp.csv'
            df.to_csv(temp_file_path, index=False)

            # Upload the updated file to Google Drive
            media = MediaFileUpload(temp_file_path, mimetype='text/csv')
            self.service.files().update(fileId=self.file_id, media_body=media).execute()
            print(f"File '{file_name}' updated successfully.")
        else:
            print(f"File '{file_name}' not found or not loaded.")
# import io
# import pandas as pd
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

# class GoogleDriveCSVHandler:
#     def __init__(self, service_account_file, scopes):
#         self.scopes = scopes
#         self.service_account_file = service_account_file
#         self.credentials = service_account.Credentials.from_service_account_file(
#             self.service_account_file, scopes=self.scopes)
#         self.service = build('drive', 'v3', credentials=self.credentials)
#         self.file_id = None

#     # List files on Google Drive
#     def list_drive_files(self):
#         results = self.service.files().list(
#             pageSize=100, fields="nextPageToken, files(id, name)").execute()
#         return results.get('files', [])

#     # Find the file ID for a specific file by name
#     def find_file_id(self, file_name):
#         items = self.list_drive_files()
#         for item in items:
#             if item['name'] == file_name:
#                 self.file_id = item['id']
#                 return item['id']
#         return None

#     # Read the CSV file from Google Drive
#     def read_csv(self, file_name):
#         if self.find_file_id(file_name):
#             request = self.service.files().get_media(fileId=self.file_id)
#             file_content = io.BytesIO()
#             downloader = MediaIoBaseDownload(file_content, request)

#             done = False
#             while not done:
#                 status, done = downloader.next_chunk()

#             file_content.seek(0)
#             return pd.read_csv(file_content)
#         else:
#             print(f"File '{file_name}' not found.")
#             return None

#     # Update the CSV file back to Google Drive and verify updates
#     def update_csv(self, df, file_name):
#         if self.file_id:
#             # Save DataFrame to a temporary local CSV file
#             temp_file_path = 'temp.csv'
#             df.to_csv(temp_file_path, index=False)

#             # Upload the updated file to Google Drive
#             media = MediaFileUpload(temp_file_path, mimetype='text/csv')
#             self.service.files().update(fileId=self.file_id, media_body=media).execute()

#             # Verify the update by checking the updated length of the 'Number of Followers' column
#             updated_df = self.read_csv(file_name)
#             if updated_df is not None:
#                 followers_col_length = updated_df['Number of Followers'].notna().sum()
#                 print(f"File '{file_name}' updated successfully. Updated length of 'Number of Followers': {followers_col_length}")
#                 return followers_col_length
#             else:
#                 print(f"Error reading the updated file '{file_name}'.")
#                 return None
#         else:
#             print(f"File '{file_name}' not found or not loaded.")
#             return None
