import re

from accounts.models import Domain
from django.http import HttpResponseNotFound


class MultiSiteMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            domain = request.get_host().split(":")[0]
            print(domain)
            if domain == "localhost":
                domain = f"http://{domain}"
            elif re.match("([0-9]{1,3}\.){3}[0-9]{1,3}", domain):
                domain = f"http://{domain}"
            request.site = Domain.objects.get(name=domain)
        except Domain.DoesNotExist:
            request.site = None

        return self.get_response(request)
