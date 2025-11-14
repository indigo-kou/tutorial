from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, Department
from .serializers import EmployeeSerializer

class EmployeeAPI(APIView):

    def post(self, request):
        name = request.data.get('name')
        department_name = request.data.get('department')

        if not name or not department_name:
            return Response({"error": "nameとdepartmentは必須です。"}, status=status.HTTP_400_BAD_REQUEST)

        employee = Employee.objects.create(name=name)
        Department.objects.create(employee=employee, department=department_name)

        return Response({"employee_id": employee.employee_id}, status=status.HTTP_201_CREATED)

    def get(self, request):
        employee_id = request.query_params.get('employee_id')

        if employee_id:
            try:
                employee = Employee.objects.prefetch_related('departments').get(employee_id=employee_id)
                serializer = EmployeeSerializer(employee)
            except Employee.DoesNotExist:
                return Response({"error": "指定された社員が存在しません。"}, status=status.HTTP_404_NOT_FOUND)
        else:
            employees = Employee.objects.prefetch_related('departments').all()
            serializer = EmployeeSerializer(employees, many=True)

        return Response(serializer.data)

