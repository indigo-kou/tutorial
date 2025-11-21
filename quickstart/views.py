from django.shortcuts import render

# Create your views here.
import logging
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import BasicAuthentication

from .models import Employee
from .serializers import EmployeeSerializer, EmployeeCreateSerializer

logger = logging.getLogger('quickstart')

class EmployeeAPI(APIView):
    authentication_classes = [BasicAuthentication]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def post(self, request):
        serializer = EmployeeCreateSerializer(data=request.data)
        logger.info(f"Received POST data: {request.data}")
        
        if serializer.is_valid():
            employee = serializer.save()
            logger.info(f"Created employee with ID: {employee.employee_id}")
            return Response(
                {'employee_id': employee.employee_id},
                status=status.HTTP_201_CREATED
            )
        logger.warning(f"Invalid data: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        employee_id = request.query_params.get('employee_id')
        logger.info(f"Received GET request with employee_id: {employee_id}")
        
        if employee_id:
            try:
                employee = Employee.objects.prefetch_related('departments').get(employee_id=employee_id)
                serializer = EmployeeSerializer(employee)
                logger.info(f"Returning data for employee_id: {employee_id}")
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Employee.DoesNotExist:
                logger.warning(f"Employee with ID {employee_id} not found")
                return Response(
                    {'error': '指定された社員番号が見つかりません'},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            employees = Employee.objects.all().prefetch_related('departments')
            serializer = EmployeeSerializer(employees, many=True)
            logger.info("Returning data for all employees")
            return Response(serializer.data, status=status.HTTP_200_OK)