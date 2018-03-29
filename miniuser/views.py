# -*- coding: utf-8 -*-
"""django-miniuser: views

Includes all app-specific views. Most of the app's views will be re-used Django
views, so this file only contains the absolute minimum.

Logical fragments will be in the respective form classes or the app's main
model."""

# Django imports
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

# app imports
from miniuser.forms import MiniUserSignUpForm


class MiniUserSignUpView(CreateView):
    """This class based view handles the registration of new users."""

    form_class = MiniUserSignUpForm
    success_url = reverse_lazy('miniuser:login')
    template_name = 'miniuser/signup.html'
