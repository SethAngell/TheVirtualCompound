from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from content.models import UserDocument, UserImage
from content.serializers import UserDocumentSerializer, UserImageSerializer


class api_get_update_delete_user_image(RetrieveUpdateDestroyAPIView):
    queryset = UserImage.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserImageSerializer


class api_list_create_user_images(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserImageSerializer

    def get_queryset(self):
        return UserImage.objects.filter(user=self.request.user)


class api_get_update_delete_user_document(RetrieveUpdateDestroyAPIView):
    queryset = UserDocument.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserDocumentSerializer


class api_list_create_user_documents(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDocumentSerializer

    def get_queryset(self):
        return UserDocument.objects.filter(user=self.request.user)
