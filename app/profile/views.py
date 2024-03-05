from django.db.models import Case, When
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    ListCreateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from utils.permissions import IsOwner
from profile.models import Experience, LandingPage, Design, Map, FavoriteThing
from profile.serializers import (
    DesignSerializer,
    MapSerializer,
    FavoriteThingSerializer,
    ExperienceSerializer,
    LandingPageSerializer,
)


# Create your views here.
def LandingPageView(request):
    user = request.site.user

    landing = LandingPage.objects.get(user=user)

    experience = (
        Experience.objects.filter(user=user)
        .annotate(
            current_job=Case(When(present=True, then=("start_year")), default=None),
            past_job=Case(When(present=False, then=("start_year")), default=None),
        )
        .order_by(
            "-past_job",
            "-current_job",
        )
    )

    timeline = {}

    for job in experience:
        if job.present:
            timeline[job.pk] = f"{job.start_year} - Present"
        else:
            timeline[job.pk] = f"{job.start_year} - {job.end_year}"

    context = {
        "landing": landing,
        "experience": experience,
        "meta": {"url": request.site.name, "name": str(user)},
        "timeline": timeline,
    }

    if landing.template is not None:
        template = f"profile/{landing.template.template_name}"
        print(template)
    else:
        template = "profile/SethHome.html"

    return render(request, template, context)


# === API Views === #
class api_get_available_designs(ListAPIView):
    queryset = Design.objects.all()
    permission_classes = [AllowAny]
    serializer_class = DesignSerializer


class api_get_available_maps(ListAPIView):
    queryset = Map.objects.all()
    permission_classes = [AllowAny]
    serializer_class = MapSerializer


class api_get_available_favorite_things(ListAPIView):
    queryset = FavoriteThing.objects.all()
    permission_classes = [AllowAny]
    serializer_class = FavoriteThingSerializer


class api_get_update_delete_experience(RetrieveUpdateDestroyAPIView):
    queryset = Experience.objects.all()
    permission_classes = [IsOwner]
    serializer_class = ExperienceSerializer


class api_create_experience(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExperienceSerializer

    def get_queryset(self):
        return Experience.objects.filter(user=self.request.user)


class api_get_update_delete_landing_page(RetrieveUpdateDestroyAPIView):
    queryset = LandingPage.objects.all()
    permission_classes = [IsOwner]
    serializer_class = LandingPageSerializer


class api_create_landing_page(CreateAPIView):
    permission_class = [IsAuthenticated]
    serializer_class = LandingPageSerializer


class api_get_profile_picture(APIView):
    def get(self, request, pk, format=None):
        print(pk)
        try:
            profile = LandingPage.objects.get(user=pk)
            profile_pic_url = request.build_absolute_uri(profile.avatar.url)
            return Response({"url": profile_pic_url})
        except LandingPage.DoesNotExist:
            raise NoLandingPageConfiguredException


class NoLandingPageConfiguredException(APIException):
    status_code = 404
    default_detail = (
        "NoLandingPageConfiguredExpection: No Profile exists for provided user"
    )
    default_code = "profile_not_found"
