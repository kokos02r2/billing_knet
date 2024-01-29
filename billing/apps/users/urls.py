from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import path, reverse

app_name = 'users'


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profile')


urlpatterns = [
    path(
      'login/',
      CustomLoginView.as_view(template_name='users/login.html'),
      name='login'
    ),
]
