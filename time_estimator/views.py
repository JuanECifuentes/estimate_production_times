"""
Views for the time estimator application
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from .services import TimeEstimationService, ExcelProcessingError
from .serializers import FileUploadSerializer
import logging

logger = logging.getLogger(__name__)


class ProcessTimeStudyAPIView(APIView):
    """
    API endpoint for processing time-study Excel files.
    
    POST /api/process-time-study/
    - Accepts multipart/form-data with an Excel file
    - Returns the processed Excel file with production estimates
    """
    
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {
                    'error': 'Invalid request',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_file = serializer.validated_data['file']
        
        try:
            service = TimeEstimationService()
            
            # Validate file size
            if hasattr(uploaded_file, 'size'):
                service.validate_file_size(uploaded_file.size)
            
            # Process the file
            output_file, summary = service.process_file(uploaded_file, uploaded_file.name)
            
            # Prepare response
            response = HttpResponse(
                output_file.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="estimacion_produccion.xlsx"'
            response['X-Summary'] = str(summary)
            
            return response
            
        except ExcelProcessingError as e:
            logger.error(f"Excel processing error: {str(e)}")
            return Response(
                {
                    'error': 'Processing error',
                    'details': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return Response(
                {
                    'error': 'Internal server error',
                    'details': 'An unexpected error occurred while processing the file'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UploadPageView(View):
    """
    Simple web interface for uploading files
    """
    
    def get(self, request):
        return render(request, 'time_estimator/upload.html')
    
    def post(self, request):
        """Handle file upload from web interface"""
        if 'file' not in request.FILES:
            return JsonResponse(
                {'error': 'No file provided'},
                status=400
            )
        
        uploaded_file = request.FILES['file']
        
        try:
            service = TimeEstimationService()
            
            # Validate file size
            if hasattr(uploaded_file, 'size'):
                service.validate_file_size(uploaded_file.size)
            
            # Process the file
            output_file, summary = service.process_file(uploaded_file, uploaded_file.name)
            
            # Return the processed file
            response = HttpResponse(
                output_file.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="estimacion_produccion.xlsx"'
            
            return response
            
        except ExcelProcessingError as e:
            logger.error(f"Excel processing error: {str(e)}")
            return JsonResponse(
                {'error': str(e)},
                status=400
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return JsonResponse(
                {'error': 'An unexpected error occurred while processing the file'},
                status=500
            )

