import time
import base64

from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseNotFound

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from shareurl.application.forms import *
from shareurl.application.models import *
from shareurl.application.mixins import *
from shareurl.application.responses import *

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class Login(TemplateView):

	'''
		Login TemplateView is a standard django login view.
	
		Args:
			*args: Arbitrary number of arguments
			**kwargs: Arbitrary number of named arguments

		Returns:
			After successfull login user is returned to the application homepage(Links).

	'''

	def get(self, request, *args, **kwargs):

		try:
			self.template_name = 'application/login.html'

			action = reverse('application:login')

			context = {
				'action': action
			}

			return self.render_to_response(context)

		except Exception as e:
			raise e



	def post(self, request, *args, **kwargs):

		try:
			data = request.POST.dict()

			username = data.get('username')
			password = data.get('password')

			user = authenticate(request, username=username, password=password)

			context = dict()

			if user is not None:
				login(request, user)

				context.update({
					'redirect': reverse('application:links')
				})

				return success(context)
			
			else:
				return bad_request(message='Username or password is incorrect')
			
		except Exception as e:
			print(e)
			return exception(message='Could not be logged in, Please try again')



class Logout(View):

	'''
		Logout view is a standard django logout view which logs out an authenticated user.
	
		Args:
			*args: Arbitrary number of arguments
			**kwargs: Arbitrary number of named arguments

		Returns:
			It returns user to login page after a successful logout.

	'''

	@method_decorator(login_required)
	def get(self, request, *args, **kwargs):

		try:
			user = request.user

			if request.user.is_authenticated:
				logout(request)
			
			return redirect(reverse('application:login'))
			
		except Exception as e:
			raise e
		


class RegisterUser(TemplateView):

	def get(self, request, *args, **kwargs):

		context = {
			'action': reverse('application:register')
		}

		self.template_name = 'application/register.html'

		return self.render_to_response(context)

	def post(self, request, *args, **kwargs):

		try:

			data = request.POST.dict()

			context = dict()

			email = data.get('email')
			password = data.get('password')
			last_name = data.get('lastname')
			first_name = data.get('firstname')

			if not email:
				return bad_request(message='Please provide email address')

			if not first_name:
				return bad_request(message='Please provide first name')

			if not last_name:
				return bad_request(message='Please provide last name')

			if not password:
				return bad_request(message='Please provide password for the user')

			data = {
				'email': email,
				'username': email,
				'last_name': last_name,
				'first_name': first_name
			}

			if not User.objects.filter(email=email).exists():
				user = User.objects.create(**data)

				user.set_password(password)
				user.save()
			else:
				return bad_request(message='Provided email address is already registered, Please provide a different email address')

			context.update({
				'redirect': reverse('application:login')
			})

			return success(context)

		except Exception as e:
			print(e)
			return exception(message='User could not be registered')



class SharealbleLinks(AccessControlMixin, TemplateView):

	def get(self, request, *args, **kwargs):

		try:

			self.template_name = 'application/links.html'
			
			links = list()

			created_links = ShareableLink.objects.filter(created_by=request.user)

			shared_links = ShareableLink.objects.exclude(created_by=request.user)

			links.extend(created_links)
			links.extend(shared_links)

			context = {
				'links': links
			}

			return self.render_to_response(context)

		except Exception as e:
			print(e)
			return exception(message='Links Could not be fetched')



class CreateUpdateShareableLink(AccessControlMixin, TemplateView):

	def get(self, request, suid=None, *args, **kwargs):

		try:
			self.template_name = 'application/create-update-link.html'

			requestor = request.user

			if suid:
				link = ShareableLink.objects.get(uuid=suid)
				action = reverse('application:update-link', args=(suid,))

			else:
				link = None
				action = reverse('application:create-link')

			context = {
				'link': link,
				'action': action,
				'requestor': requestor
			}

			return self.render_to_response(context)

		except Exception as e:
			raise e



	def post(self, request, suid=None, *args, **kwargs):

		try:
			data = request.POST.dict()

			original_text = data.get('text', None)
			secret_key = data.get('secretKey', None)
			title = data.get('title', None)

			if not original_text:
				return bad_request(message='Please provide text')


			if not title:
				return bad_request(message='Please provide title for the link')

			link_data = {
				'title': title,
				'original_text': original_text,
				'encrypted_text': None,
				'secret_key': secret_key,
				'created_by': request.user,
				'modified_by': request.user

			}

			context = dict()

			if secret_key:

				if len(secret_key)%16 != 0:
					return bad_request(message='Secret Key should be multiple of length of 16')

				# === Encrypt ===
				text = original_text.encode('utf-8')
				# text = base64.b64encode(original_text)

				# Create the cipher object and encrypt the data
				cipher_encrypt = AES.new(secret_key.encode('utf-8'), AES.MODE_CFB, secret_key.encode('utf-8'))
				encrypted_text = cipher_encrypt.encrypt(text)

				# encryption_info = {
				# 	'iv': cipher_encrypt.iv.decode('utf-8'),
				# 	'ciphered_data': encrypted_text.decode('utf-8')
				# }

				link_data.update({
					'encrypted_text': encrypted_text
				})

			if suid:
				link = ShareableLink.objects.get(uuid=suid)

				link.title = title
				link.secret_key = secret_key
				link.modified_by = request.user
				link.original_text = original_text
				# link.encryption_info = encryption_info
				link.encrypted_text = link_data.get('encrypted_text')
				link.save()

			else:
				link = ShareableLink.objects.create(**link_data)

			context.update({
				'redirect': reverse('application:links')
			})

			return success(context)
			
		except Exception as e:
			print(e)
			return exception(message='Link could not be created')



class ShowSharedText(AccessControlMixin, View):

	def get(self, request, *args, **kwargs):

		try:

			requestor = request.user

			data = request.GET.dict()

			print('data = ', data)

			secret_key = data.get('secret_key')
			uuid = data.get('uuid')

			link = ShareableLink.objects.filter(uuid=uuid, secret_key=secret_key)

			if link:
				link = link[0]
			else:
				return bad_request(message='Provided key is not valid, please check and try again')

			context = {
				'original_text': link.original_text
			}

			return success(context)

		except Exception as e:
			print(e)
			return exception(message='Data could not be fetched')