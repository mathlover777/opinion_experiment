from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_student$', views.add_student, name='add_student'),
    url(r'^add_opinion$', views.add_opinion, name='add_opinion'),
    url(r'^get_top_opinion_list$', views.get_top_opinion_list, name='get_top_opinion_list'),
    url(r'^get_latest_opinion$', views.get_latest_opinion, name='get_latest_opinion'),
    url(r'^get_neighbors_with_influence_values$', views.get_neighbors_with_influence_values, name='get_neighbors_with_influence_values'),
    url(r'^reset_and_download_data$', views.reset_and_download_data, name='reset_and_download_data'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^download_data$', views.download_data, name='download_data'),
]