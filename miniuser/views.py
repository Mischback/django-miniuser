# -*- coding: utf-8 -*-
"""django-miniuser: views"""

# Django imports
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

# app imports
from miniuser.forms import MiniUserSignUpForm


class MiniUserSignUpView(CreateView):
    """foobar"""

    form_class = MiniUserSignUpForm
    success_url = reverse_lazy('miniuser:login')
    template_name = 'miniuser/signup.html'
