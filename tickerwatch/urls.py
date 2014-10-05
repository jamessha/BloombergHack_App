from django.conf.urls import patterns, url

from tickerwatch import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^add_stock/$', views.add_stock, name='add_stock'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^text/$', views.text, name='text'),
    url(r'^text_demo/$', views.text_demo, name='text_demo'),
)
