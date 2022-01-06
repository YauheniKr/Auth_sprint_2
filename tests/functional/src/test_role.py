import json

import pytest as pytest
import requests


class TestsRoleApi:

    def test_role_get_detailed(self, role):
        url = f'http://auth_api:8000/api/v1/auth/role/{role.id}'
        role_answer = requests.get(url)
        assert role_answer.status_code == 200
        assert role_answer.json()['id'] == str(role.id)
        assert role_answer.json()['role_weight'] == role.role_weight
        assert role_answer.json()['role_name'] == role.role_name
        assert role_answer.json()['description'] == role.description

    def test_role_update(self, role):
        url = f'http://auth_api:8000/api/v1/auth/role/{role.id}'
        data = {"description": "test role 2"}
        json_data = json.dumps(data)
        headers = {
            'Content-Type': 'application/json'
        }
        role_answer = requests.patch(url, data=json_data, headers=headers)
        assert role_answer.status_code == 200
        assert role_answer.json()['description'] == data['description']

    def test_role_delete(self, role):
        url = f'http://auth_api:8000/api/v1/auth/role/{role.id}'
        role_answer = requests.delete(url)
        assert role_answer.status_code == 200
        role_answer = requests.get(url)
        assert role_answer.status_code == 404

    def test_role_create(self):
        url = f'http://auth_api:8000/api/v1/auth/role/'
        data = {
            "role_name": "test_role 3",
            "role_weight": 6,
            "description": "test role 2"
        }
        json_data = json.dumps(data)
        role_answer = requests.post(url, data=json_data)
        assert role_answer.status_code == 200

    def test_roles_get(self, roles):
        url = f'http://auth_api:8000/api/v1/auth/roles/'
        role_answer = requests.get(url)
        assert role_answer.status_code == 200
        assert len(role_answer.json()) == 2
