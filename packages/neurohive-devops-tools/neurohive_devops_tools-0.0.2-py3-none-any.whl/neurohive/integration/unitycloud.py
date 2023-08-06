

class UnityCloudException(Exception):
    pass


class UnityCloud:
    def __init__(self, org_id):
        self.base_url = 'https://build-api.cloud.unity3d.com/api/v1'
        self.auth_headers = {
            'Authorization': 'Basic ' + unity_api_key
        }
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + unity_api_key
        }
        self.organization_id = org_id
        self.project_name = project_name
        self._set_project_id()
        self.target_name = target_name
        self._set_target_id()

