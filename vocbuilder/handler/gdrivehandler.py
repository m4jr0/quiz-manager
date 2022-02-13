import pathlib

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GDriveHandler:
    SCOPE_SHEET_READONLY = (
        "https://www.googleapis.com/auth/spreadsheets.readonly"
    )

    SCOPE_SHEET = "https://www.googleapis.com/auth/spreadsheets"
    SCOPE_DRIVE_READONLY = "https://www.googleapis.com/auth/drive.readonly"
    SCOPE_DRIVE_FILE = "https://www.googleapis.com/auth/drive.file"
    SCOPE_DRIVE = "https://www.googleapis.com/auth/drive"

    __creds = None
    __is_initialized = False
    __scopes = []
    __service = None
    __sheet_service = None

    def __repr__(self):
        return "GDriveHandler[__is_initialized: {is_initialized}]".format(
            is_initialized=self.__is_initialized,
        )

    def __str__(self):
        return "GDriveHandler[{label}]".format(
            label="Loaded" if self.__is_initialized else "Not loaded",
        )

    def __init__(
        self,
        token_path=None,
        scopes=None,
    ):
        self.__token_path = (
            pathlib.Path(token_path) if token_path is not None else None
        )
        self.__scopes = (
            [self.SCOPE_SHEET_READONLY] if scopes is None else scopes
        )

    def reset(self):
        if self.__token_path is not None:
            self.__token_path.unlink(True)

        self.__scopes = [self.SCOPE_SHEET_READONLY]

    def log_in(self):
        if self.__token_path is not None and self.__token_path.is_file():
            self.__creds = (
                service_account.Credentials.from_service_account_file(
                    self.__token_path
                )
            )

    def initialize(self):
        self.log_in()
        self.__service = build("sheets", "v4", credentials=self.__creds)
        self.__sheet_service = self.__service.spreadsheets()

    def fetch_values(
        self,
        sheet_id,
        range,
    ):
        result = (
            self.__sheet_service.values()
            .get(
                spreadsheetId=sheet_id,
                range=range,
            )
            .execute()
        )

        return result.get("values", [])
