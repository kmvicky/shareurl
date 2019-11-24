from django.urls import reverse
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin


class AccessControlMixin(LoginRequiredMixin):


	def dispatch(self, request, *args, **kwargs):

		try:

			requested_view = self.__class__.__name__

			if not request.user.is_authenticated:
				return redirect(reverse('application:login'))


			return super(AccessControlMixin, self).dispatch(request, *args, **kwargs)

		except Exception as e:
			print(e)
			raise PermissionDenied()