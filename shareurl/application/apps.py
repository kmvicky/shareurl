from django.apps import AppConfig

class ApplicationConfig(AppConfig):

	name = 'shareurl.application'
	verbose_name = 'application'

	def ready(self):
		pass