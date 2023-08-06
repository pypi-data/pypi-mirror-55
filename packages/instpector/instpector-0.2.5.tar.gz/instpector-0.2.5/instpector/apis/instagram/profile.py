from ..exceptions import ParseDataException
from .base_api import BaseApi
from .parser import Parser


class Profile(BaseApi):

    def __init__(self, instance):
        super().__init__("https://www.instagram.com", instance)

    def of_user(self, username):
        params = {
            "__a": 1
        }
        try:
            data = super().get(f"/{username}/", params=params, headers={
                "DNT": "1"
            })
            if data:
                return Parser.profile(data)
        except ParseDataException:
            print(f"Invalid data for username {username}")
        return None
