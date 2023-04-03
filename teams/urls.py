from django.urls import path

from teams.views import TeamView
from teams.views import TeamIdView

urlpatterns = [
    path("teams/", TeamView.as_view()),
    path("teams/<int:team_id>/", TeamIdView.as_view())
]