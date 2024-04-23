from django.views.generic import TemplateView


class MovieDetail(TemplateView):
    template_name = "tests/movie_detail.html"
