from django.shortcuts import render

from personel.serializer import PersonnelSeriaizer
from django.db import transaction

from .models import Personnel, RoleAssignment
from rest_framework.response import Response
from rest_framework import viewsets, status

import traceback

# Create your views here.
class PersonnelViewSet(viewsets.ViewSet):
    serializer_class = PersonnelSeriaizer
    
    """[summary]
    ViewSet used to save and fetch personnel data
    """
    
    def list(self, request):
        """[summary]
        Fetch all personnels from the database
        Returns:
            [success]: [bool for showing data was passed]
            [message]: [indicates type of data passed]
            [data]: [instance of personnel in json format]
        """
        personnels = Personnel.objects.all()
        serializer = self.serializer_class(personnels, many=True, context={'request': request})
        
        return Response(dict(success=True, message="All Personnel", data=serializer.data))
    
    def employees(self, request):
        """[summary]
        Fetch all personnels under a supervisor from the database
        Args:
            request ([supervisor_id]): [unique personnel id used to identify supervisor]

        Returns:
            [success]: [bool for showing data was passed]
            [message]: [indicates type of data passed]
            [data]: [instance of employee in json format]
        """
        supervisor_id = self.request.query_params.get("supervisor")
        role = RoleAssignment.objects.get(supervisor__id=supervisor_id)
        employees = role.employees.all()
        
        serializer = self.serializer_class(employees, many=True, context={'request': request})
        
        return Response(dict(success=True, message="All Employees", data=serializer.data))
    
    def create_supervisor(self, request):
        """[summary]
        Create and saves a supervisor and role instance to the database
        Args:
            request ([account_name]): [Name of the role supervisor is overheading]
            request ([first_name]): [personnel first name]
            request ([last_name]): [personnel last name (optional)]
            request ([email]): [personnel email address]
            request ([phone_number]): [personnel phone number]

        Returns:
            [success]: [bool for showing data was passed]
            [message]: [indicates type of data passed]
            [data]: [instance of supervisor in json format]
        """
        try:
            with transaction.atomic():
                data = request.data
                # creates instance to add to database
                serializer = self.serializer_class(data=data, context={'request': request})
                serializer.is_valid()
                
                supervisor = serializer.save()
                RoleAssignment.objects.create(
                    supervisor=supervisor,
                    name=data.get('account_name')
                )
                response_data = self.serializer_class(supervisor, context={'request': request}).data
                return Response(dict(success=True, message="SuperVisior has been created", data=response_data))
        except Exception as e:
            return Response(dict(success=False, message="Could not create supervisor, please try again"), status=status.HTTP_501_NOT_IMPLEMENTED)
        
    def create(self, request):
        """[summary]
        Create and saves a employees to role instance in the database
        Args:
            request ([supervisor]): [Personnel overheading the role]
            request ([first_name]): [personnel first name]
            request ([last_name]): [personnel last name (optional)]
            request ([email]): [personnel email address]
            request ([phone_number]): [personnel phone number]

        Returns:
            [success]: [bool for showing data was passed]
            [message]: [indicates type of data passed]
            [data]: [instance of supervisor in json format]
        """
        try:
            with transaction.atomic():
                data = request.data
                # creates instance to add to database
                serializer = self.serializer_class(data=data, context={'request': request})
                serializer.is_valid()
                
                employee = serializer.save()
                role = RoleAssignment.objects.get(supervisor__id=data.get('supervisor'))
                role.employees.add(employee)
                role.save()
                
                response_data = self.serializer_class(employee, context={'request': request}).data
                return Response(dict(success=True, message="Employee has been created", data=response_data))
        except Exception as e:
            return Response(dict(success=False, message="Could not create employee, please try again"), status=status.HTTP_501_NOT_IMPLEMENTED)
        