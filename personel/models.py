from django.db import models

# Create your models here.
class Personnel(models.Model):
    """[summary]
    Personnel table used to access employee and supervisor data
    """
    email = models.EmailField(verbose_name="Personnel Email", max_length=254, unique=True)
    first_name = models.CharField(verbose_name="First Name", max_length=100)
    last_name = models.CharField(verbose_name="Last Name", max_length=100, null=True, blank=True)
    phone_number = models.CharField(verbose_name="Phone Number", max_length=50)

    class Meta:
        ordering = ['-id']
        db_table = 'db_personnel'
        verbose_name = "Personnel"
        verbose_name_plural = "Personnels"
        
class RoleAssignment(models.Model):
    """[summary]
    Asignment Table used to assign employee to different supervisors
    """
    name = models.CharField(verbose_name="Role Name", max_length=100)
    supervisor = models.OneToOneField("personel.Personnel", related_name="personnel_supervisor",verbose_name="SuperVising Personnel", on_delete=models.CASCADE)
    employees = models.ManyToManyField("personel.Personnel", related_name="personnel_employee", verbose_name="Employees", blank=True)
    
    class Meta:
        ordering = ['-id']
        db_table = 'role_assignment'
        verbose_name = "RoleAssignment"
        verbose_name_plural = "RoleAssignments"