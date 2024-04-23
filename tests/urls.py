from django.urls import path

from tests import views

urlpatterns = [
    path("movie-detail/", views.MovieDetail.as_view(), name="movie_detail"),
]
