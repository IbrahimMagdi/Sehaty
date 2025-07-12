from django.urls import path, include
from .sign_in import urls as sign_in_urls
from .sign_up import urls as sign_up_urls
from .forgot_password import urls as forgot_password_urls

urlpatterns = [
   path('sign-in/', include(sign_in_urls)),
   path('sign-up/', include(sign_up_urls)),
   path('forgot-password/', include(forgot_password_urls)),
]

