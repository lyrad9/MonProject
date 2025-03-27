# Ce fichier contient tous les chemins d\'acces pour les differents comptes.

from django.urls import  path

from utilisateurs.views import client_dashbord, contact_view
from utilisateurs.views import register, logOut, logIn, activate_account, apropos, home
from django.contrib.auth import views as  auth_views

urlpatterns  = [

    path('', home, name='home'),

    path('register',register,name='register'),
    path('login',logIn,name='login'),

    path('apropos/', apropos, name='apropos'),
    path('contact/', contact_view, name='contact_view'),

    path('client_dashbord/', client_dashbord, name='client_dashbord'),

    path('logout', logOut, name='logout'),
    path('activate/<uidb64>/<token>/',activate_account,name='activate'),

# Page pour saisir l'email
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="auth/reset_password.html"), name="reset_password"),

    # Message de confirmation que l'email a été envoyé
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="auth/reset_password_sent.html"), name="password_reset_done"),

    # Formulaire pour saisir le nouveau mot de passe
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="auth/reset_password_form.html"), name="password_reset_confirm"),

    # Message indiquant que le mot de passe a été changé
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="auth/reset_password_complete.html"), name="password_reset_complete"),

    #path('test-email/', test_email, name='test-email')
]



