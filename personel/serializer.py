from django.db.models import fields
from rest_framework import serializers
from .models import Personnel, RoleAssignment

class PersonnelSeriaizer(serializers.ModelSerializer):
    """[summary]
    Serializer for saving and fetching personnel data
    Args:
        serializers ([first_name]): [personnel first name]
        serializers ([last_name]): [personnel last name (optional)]
        serializers ([email]): [personnel email address]
        serializers ([phone_number]): [personnel phone number]

    Returns:
        serializers ([id]): [personnel unique id]
        serializers ([first_name]): [personnel first name]
        serializers ([last_name]): [personnel last name (optional)]
        serializers ([email]): [personnel email address]
        serializers ([phone_number]): [personnel phone number]
    """
    
    class Meta:
        model = Personnel
        fields = '__all__'
        
    def to_representation(self, instance):
        """[summary]
        Used to manipulate json return values
        Args:
            instance ([type]): [description]

        Returns:
            [role]: [personnel assigned role]
        """
        representation = super().to_representation(instance)
        current_role = RoleAssignment.objects.filter(employees=instance).first()
        if not current_role:
            current_role = RoleAssignment.objects.filter(supervisor=instance).first()
        representation['role'] = current_role.name
        
        return representation