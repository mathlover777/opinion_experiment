from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_student$', views.add_student, name='add_student'),
    url(r'^add_opinion$', views.add_opinion, name='add_opinion'),
    url(r'^get_top_opinion_list$', views.get_top_opinion_list, name='get_top_opinion_list'),
]