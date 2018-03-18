# -*- coding: utf-8 -*-
"""django-miniuser: views"""

# Django imports
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

# app imports
from miniuser.forms import MiniUserSignUpForm


class MiniUserSignUpView(FormView):
    """foobar"""

    form_class = MiniUserSignUpForm
    success_url = reverse_lazy('miniuser:login')
    template_name = 'miniuser/signup.html'
