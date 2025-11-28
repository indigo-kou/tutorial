import uuid

from django.db import models


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.employee_id}: {self.name}"


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(
        Employee, related_name="departments", on_delete=models.CASCADE
    )
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.employee.name} - {self.department_name}"
