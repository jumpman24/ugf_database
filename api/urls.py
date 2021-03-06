from django.conf.urls import url

from .views import *

# Create your urls here.

app_name = 'api'
urlpatterns = [
    url(r'^upload/active_rating_list/$', upload_active_rating_list, name='upload_active_rating_list'),
    url(r'^upload/inactive_rating_list/$', upload_inactive_rating_list, name='upload_inactive_rating_list'),

    url(r'^upload/egd_tournament/$', upload_egd_tournament, name='upload_egd_tournament'),
    url(r'^upload/ufgo_ratings/$', upload_ufgo_ratings, name='upload_ufgo_ratings'),

    url(r'^tournament_rating_calculator/(?P<pk>[\d]+)/$', tournament_rating_calculator, name='tournament_rating_calculator'),
    url(r'^update_rating_list/$', update_rating_list, name='update_rating_list'),

    url(r'^upload/pin_list/$', upload_egd_pins, name='upload_egd_pins'),
    url(r'^download/rating_list/$', download_rating_list, name='download_rating_list'),

    url(r'^json/player_list/$', json_player_list, name='player_list'),
    url(r'^json/calculated_rating/$', json_calculated_rating, name='calculated_rating'),

    url(r'^mod_wsgi_reload/$', mod_wsgi_reload, name='mod_wsgi_reload'),
]
