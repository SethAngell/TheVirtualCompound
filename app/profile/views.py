from django.db.models import Case, When
from django.shortcuts import render

from .models import Experience, LandingPage


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
