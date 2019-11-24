import application.views as views

from django.urls import include, path, re_path

app_name = 'application'

urlpatterns = [
	
	path('', 
		views.SharealbleLinks.as_view(),
		 name='links'),

	path('login', 
		views.Login.as_view(),
		 name='login'),

	path('logout', 
		views.Logout.as_view(),
		 name='logout'),

	path('register', 
		views.RegisterUser.as_view(),
		 name='register'),

	re_path(r'^create-link/$',
		views.CreateUpdateShareableLink.as_view(),
		 name='create-link'),

	re_path(r'^update-link/(?P<suid>[-\w]+)$',
		views.CreateUpdateShareableLink.as_view(),
		 name='update-link'),

	re_path(r'^show-text/$',
		views.ShowSharedText.as_view(),
		 name='show-text'),
]