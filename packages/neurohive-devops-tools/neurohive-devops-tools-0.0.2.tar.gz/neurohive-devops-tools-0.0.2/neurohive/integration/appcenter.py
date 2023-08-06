import requests


class AppCenterWrapperException(Exception):
    pass


class AppCenter:
    def __init__(self, token: str, owner: str) -> None:
        self.token = token
        self.owner = owner
        self.headers = {
            'Content-Type': 'application/json',
            'X-API-Token': self.token
        }
        self.base_url = 'https://api.appcenter.ms'

    def get_new_idids(self, app_name: str, distr_grp_name: str) -> list():
        url = f'{self.base_url}/v0.1/apps/{self.owner}/{app_name}/distribution_groups/{distr_grp_name}/devices'
        req = requests.get(url, headers=self.headers)
        to_provision = [d for d in req.json() if d.get('status') != 'provisioned']
        return to_provision


if __name__ == '__main__':
    pass
