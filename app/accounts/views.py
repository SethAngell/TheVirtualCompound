from xml import dom

from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template

from .forms import NewInvitationForm
from .models import Domain, Invitation


def create_new_invite(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NewInvitationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print("Hi!")
            new_invite = form.save()
            send_invite_email(new_invite)
            # redirect to a new URL:
            return HttpResponseRedirect("/")
        else:
            print(form.errors)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewInvitationForm()

    domains = Domain.objects.filter(user=None)
    context = {"form": form, "domains": domains}

    return render(request, "accounts/invite_user.html", context)


def send_invite_email(new_invitation):
    print("email sent!")
    plaintext = get_template("accounts/emails/plaintext-invite.txt")
    htmly = get_template("accounts/emails/styled-invite.html")

    d = {"invite": new_invitation}

    subject, from_email, to = "Welcome!", "seth@doublel.studio", new_invitation.email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
