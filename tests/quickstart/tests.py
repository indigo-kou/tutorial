# Create your tests here.
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Department, Employee


class EmployeeAPITestCase(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            password="adminpass",
        )
        self.user = User.objects.create_user(username="user", password="userpass")
        self.client = APIClient()
        self.url = "/api/employees/"

    def test_get_employees_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/employees/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_employee_success(self):
        emp = Employee.objects.create(name="太郎")
        Department.objects.create(employee=emp, department_name="営業")

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"employee_id": emp.employee_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "太郎")
        self.assertEqual(response.data["department"], "営業")

    def test_get_employee_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"employee_id": 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)

    def test_post_requires_admin(self):
        self.client.force_authenticate(user=self.user)
        body = {"name": "次郎", "department_name": "開発"}
        response = self.client.post(self.url, body, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_create_employee_success(self):
        self.client.force_authenticate(user=self.admin)
        body = {"name": "次郎", "department_name": "開発"}
        response = self.client.post(self.url, body, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("employee_id", response.data)

        emp_id = response.data["employee_id"]
        emp = Employee.objects.get(employee_id=emp_id)
        self.assertEqual(emp.name, "次郎")
        dep = emp.departments.first()
        self.assertIsNotNone(dep)
        self.assertEqual(dep.department_name, "開発")

    def test_post_invalid_data(self):
        self.client.force_authenticate(user=self.admin)
        body = {"name": "", "department_name": ""}
        response = self.client.post(self.url, body, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertIn("department_name", response.data)

    def test_basic_authentication(self):
        import base64

        token = base64.b64encode(b"user:userpass").decode()
        headers = {"HTTP_AUTHORIZATION": f"Basic {token}"}
        response = self.client.get("/api/employees/", **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
