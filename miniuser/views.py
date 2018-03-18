# -*- coding: utf-8 -*-
"""django-miniuser: views"""

# Django imports
from django.views.generic.edit import FormView

# app imports
from miniuser.forms import MiniUserSignUpForm


class MiniUserSignUpView(FormView):
    """foobar"""

    form_class = MiniUserSignUpForm
    success_url = None
    template_name = 'miniuser/signup.html'
