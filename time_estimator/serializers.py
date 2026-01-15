"""
Serializers for the time estimator API
"""

from rest_framework import serializers


class FileUploadSerializer(serializers.Serializer):
    """Serializer for file upload"""
    file = serializers.FileField(required=True)
    
    def validate_file(self, value):
        """Validate the uploaded file"""
        if not value.name.lower().endswith('.xlsx'):
            raise serializers.ValidationError(
                "Invalid file format. Only .xlsx files are allowed."
            )
        return value
