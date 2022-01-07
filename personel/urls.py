from django.urls import path
from .views import PersonnelViewSet

"""
    [summary]
    Personnel Urls for viewing and creating user
"""

app_name = 'personel'
urlpatterns = [
    # To Fetch All Personnel in the database
    path('view', PersonnelViewSet.as_view({'get': 'list'}),name="personnel-view"),
    # To Fetch All Employees under a supervisor
    path('employees/view', PersonnelViewSet.as_view({'get': 'employees'}),name="personnel-employees-view"),
    # To create an employee under a supervisor
    path('employee/create', PersonnelViewSet.as_view({'post': 'create'}),name="personnel-employee-create"),
    # To create an create a supervisor linked to an employee
    path('supervisor/create', PersonnelViewSet.as_view({'post': 'create_supervisor'}),name="personnel-supervisor-create"),
]