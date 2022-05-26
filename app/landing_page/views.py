from django.db.models import Case, When
from django.shortcuts import render

from .models import Experience, LandingPage

# Create your views here.


def LandingPageView(request):
    user = request.site.user
    print(f"{user = }")

    landing = LandingPage.objects.get(user=user)
    print(f"{landing = }")

    print(landing.headline)

    # experience = Experience.objects.all().order_by('-start_year')
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
    context = {
        "landing": landing,
        "experience": experience,
        "meta": {"url": request.site.name, "name": str(user)},
    }

    if landing.template is not None:
        template = f"landing_page/{landing.template.template_name}"
    else:
        template = "landing_page/SethHome.html"

    return render(request, template, context)
