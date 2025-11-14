from rest_framework import serializers
from .models import Employee, Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_name']

class EmployeeSerializer(serializers.ModelSerializer):
    department_name = DepartmentSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ['employee_id', 'name', 'department_name']
    
    def get_department_name(self, obj):
        departments = obj.departments.all()
        if departments.exists():
            return departments.first().department_name
        return None

class EmployeeCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    department_name = serializers.CharField(max_length=100)

    def create(self, validated_data):
        employee = Employee.objects.create(name=validated_data['name'])
        Department.objects.create(employee=employee, department_name=validated_data['department_name'])
        return employee