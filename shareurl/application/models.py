import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.contrib.postgres.fields import ArrayField, JSONField


class ShareableLink(models.Model):

	uuid 			= models.UUIDField(default=uuid.uuid4)
	title 			= models.CharField(max_length=128)
	original_text 	= models.TextField(null=True, blank=True)
	encrypted_text 	= models.TextField(null=True, blank=True)
	secret_key 		= models.CharField(max_length=128, null=True, blank=True)
	created_by 		= models.ForeignKey(User, related_name='creator', 
						on_delete=models.CASCADE)
	created_on 		= models.DateTimeField(auto_now_add=True)
	modified_by 	= models.ForeignKey(User, related_name='modifier',
						on_delete=models.CASCADE)
	modified_on		= models.DateTimeField(auto_now=True)
	encryption_info = JSONField(default=dict)

	def __str__(self):

		return '{}'.format(str(self.uuid))



