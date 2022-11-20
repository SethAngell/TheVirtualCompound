from xml import dom

from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import Context
from django.template.loader import get_template

from .forms import CustomUserCreationForm, NewInvitationForm, NewUserFromInviteForm
from .models import CustomUser, Domain, Invitation


def create_new_invite(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NewInvitationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
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


def validate_invited_user(request):
    errors = ""
    if request.method == "POST":
        form = NewUserFromInviteForm(request.POST)

        if form.is_valid():
            user_email = form.cleaned_data["email"].lower()
            invite_code = form.cleaned_data["invite_code"]

            try:
                invitation = Invitation.objects.get(email=user_email)

            except Invitation.DoesNotExist:
                invitation = None

                errors = "Invalid Email: No email address found, make sure you use the same email that your invitation was sent to"
                context = {"form": form, "errors": errors}
                return render(request, "accounts/accept_invite.html", context)

            if invitation is not None and (
                invite_code != str(invitation.invitation_code)
            ):
                print(
                    f"IN  Code: {invitation.invitation_code} and {len(invitation.invitation_code)}"
                )
                print(f"OUT Code: {invite_code} and {len(invite_code)}")
                errors = "Invalid Invite Code: Make sure you copied that code properly!"
            elif invitation is not None and invite_code == str(
                invitation.invitation_code
            ):

                user_creation_errors, new_user = _create_user(request)
                if new_user is not None:
                    invitation.linked_domain.user = new_user
                    invitation.linked_domain.save()

                    invitation.delete()

                else:
                    if "password2" in user_creation_errors.as_data().keys():
                        errors = (
                            "Password: Oof, that password was way to simple. Try again?"
                        )
                    else:
                        errors = "Invalid User: Failed to create new user. Go bug seth"

            if len(errors) == 0:
                redirect("home")

        else:
            errors = form.errors

    form = NewUserFromInviteForm()
    context = {"form": form, "errors": errors}

    return render(request, "accounts/accept_invite.html", context)


def send_invite_email(new_invitation):

    plaintext = get_template("accounts/emails/plaintext-invite.txt")
    htmly = get_template("accounts/emails/styled-invite.html")

    d = {"invite": new_invitation}

    subject, from_email, to = "Welcome!", "seth@doublel.studio", new_invitation.email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# ====================================================================================== #
# Helper Functions


def _create_user(request):
    NewUserForm = CustomUserCreationForm(request.POST)

    if NewUserForm.is_valid():
        user = NewUserForm.save()
        raw_password = NewUserForm.cleaned_data.get("password1")
        user = authenticate(request, email=user.email, password=raw_password)

        if user is not None:
            login(request, user)

        return (None, user)
    else:
        return (NewUserForm.errors, None)
