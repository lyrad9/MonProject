from django.contrib import admin
from .models import User


# Personnalisation de l'affichage des utilisateurs dans l'admin
class AdminUser(admin.ModelAdmin):
    list_display = ('username', 'email', 'get_role', 'date_joined', 'is_active')  # Affiche le rôle, email, etc.
    list_filter = (
    'is_staff', 'date_joined', 'is_active')  # Permet de filtrer par rôle (is_staff), date d'inscription, et état actif
    search_fields = ('username', 'email')  # Recherche par nom d'utilisateur et email
    readonly_fields = ('date_joined',)  # Champs en lecture seule

    def get_role(self, obj):
        return "Admin" if obj.is_staff else "Client"  # Affiche "Admin" si is_staff est True, sinon "Client"

    get_role.short_description = 'Rôle'  # Nom de la colonne dans l'admin


# Enregistrer le modèle User avec la personnalisation de l'admin
admin.site.register(User, AdminUser)
