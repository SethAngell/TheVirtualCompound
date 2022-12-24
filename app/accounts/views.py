from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer

# API Views
@api_view(["POST"])
def api_create_custom_user(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
