from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy as reverse
from django.contrib import messages
from django.contrib.auth import logout
from django.utils import translation
from django.conf import settings
from django.core.urlresolvers import resolve


class RedirectMiddleware(object):
    def is_have_access(self, path):
        try:
            resolver_match = resolve(path)
            return resolver_match.view_name in settings.ALLOWED_EXTERNAL_ACCESS_VIEW
        except:
            pass

    def process_request(self, request):
        current_language = translation.get_language()
        current_url = str(request.get_full_path())
        if self.is_have_access(current_url):
            return
        if not request.user.is_authenticated():
            login_url = str(reverse('login'))

            if request.path != login_url:
                url = current_url
                if str(reverse('logout')) in url:
                    url = reverse('login')
                return redirect(login_url + '?next={}'.format(url))

        if request.user.is_authenticated():
            user = request.user
            try:
                if user.profile.language != current_language:
                    translation.activate(user.profile.language)
                    request.session[translation.LANGUAGE_SESSION_KEY] = user.profile.language
            except:
                pass

            if not user.is_active:
                logout(request)
                msg = u"Invalid user session"
                messages.add_message(request, messages.ERROR, msg)
                return redirect("home")
