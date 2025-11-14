from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Employee
from .serializers import EmployeeSerializer, EmployeeCreateSerializer

class EmployeeAPI(APIView):

    def post(self, request):
        serializer = EmployeeCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            employee = serializer.save()
            return Response(
                {'employee_id': employee.employee_id},
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        employee_id = request.query_params.get('employee_id')
        
        if employee_id:
            try:
                employee = Employee.objects.prefetch_related('departments').get(
                    employee_id=employee_id
                )
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Employee.DoesNotExist:
                return Response(
                    {'error': '指定された社員番号が見つかりません'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            employees = Employee.objects.all().prefetch_related('departments')
            serializer = EmployeeSerializer(employees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)