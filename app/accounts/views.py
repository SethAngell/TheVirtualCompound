from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from accounts.models import CustomUser, Domain
from accounts.serializers import CustomUserSerializer, DomainSerializer

# API Views
@api_view(["POST"])
def api_create_custom_user(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class api_get_registered_domain_mappings(ListAPIView):
    queryset = Domain.objects.all()
    permission_classes = [AllowAny]
    serializer_class = DomainSerializer
