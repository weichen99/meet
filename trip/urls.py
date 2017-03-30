from django.conf.urls import url
from . import views

app_name = 'trip'

urlpatterns = [
    #/
    url(r'^$', views.IndexView.as_view(), name='index'),

    #register
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    #log in
    url(r'^login/$', views.UserLogIn.as_view(), name='login'),

    #log out
    url(r'^logout/$', views.UserLogOut.as_view(), name='logout'),

    #/{pk}/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    #/trip/add/
    url(r'^trip/add/$', views.TripCreate.as_view(), name='trip_add'),

    #/trip/{pk}/
    url(r'^trip/(?P<pk>[0-9]+)/$', views.TripUpdate.as_view(), name='trip_update'),

    # /trip/{pk}/delete/
    url(r'^trip/(?P<pk>[0-9]+)/delete/$', views.TripDelete.as_view(), name='trip_delete'),

    #/{pk}/attend_trip
    url(r'^(?P<trip_id>[0-9]+)/attend_trip/$', views.attend_trip, name='attend_trip'),

    #/user/trips/
    url(r'^user/trips/$', views.UserTripsView.as_view(), name='user_trips'),

]
