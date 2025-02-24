from rest_framework import status


class APIResponse:
    def __init__(self, success: bool, data=None, message="", status=""):
        self.success = success
        self.data = data
        self.message = message
        self.status = status