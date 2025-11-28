from rest_framework import serializers

from .models import Department, Employee


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["department_name"]


class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ["employee_id", "name", "department"]

    def get_department(self, obj):
        first_dep = obj.departments.first()
        return first_dep.department_name if first_dep else None


class EmployeeCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    department_name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        employee = Employee.objects.create(name=validated_data["name"])
        Department.objects.create(
            employee=employee,
            department_name=validated_data["department_name"],
        )
        return employee
