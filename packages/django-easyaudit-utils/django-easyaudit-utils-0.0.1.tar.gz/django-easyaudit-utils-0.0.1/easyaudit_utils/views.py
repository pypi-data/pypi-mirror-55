from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from easyaudit.models import CRUDEvent, LoginEvent, RequestEvent

from cbs.apps.core.views import PaginationMixin


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "easyaudit/index.html"


class CRUDEventListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = CRUDEvent
    paginate_by = 50


class LoginEventListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = LoginEvent  # TODO : Use Django-defender
    paginate_by = 50


class RequestEventListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = RequestEvent
    paginate_by = 50
