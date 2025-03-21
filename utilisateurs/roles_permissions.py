from django.contrib.auth.models import Permission, Group

from django.contrib.contenttypes.models import ContentType
from django.apps import  apps


def create_role_and_permissions():
    """
    Cree les groupes et permissions pour Administrateur, employes, et client.
    """
    #GROUPES
    admin_group, _ = Group.objects.get_or_create(name= Role.ADMINISTRATEUR)
    employe_group, _ = Group.objects.get_or_create(name=Role.EMPLOYE)
    client_group, _ = Group.objects.get_or_create(name=Role.CLIENT)

    #PERMISSIONS pour utilisateurs
    #Gestion des utilisateurs (permissions admin)
    user_model = apps.get_model('auth', 'User')
    admin_permissions = Permission.objects.filter( content_type=ContentType.objects.get_for_model(user_model))

    # Permissions spécifiques à Employé
    devis_model = apps.get_model("devis", "Devis")
    projects_model = apps.get_model("projets", "Projet")
    tache_model = apps.get_model("taches", "Tache")
    employe_permissions = Permission.objects.filter(
        content_type__in=[
            ContentType.objects.get_for_model(devis_model),
            ContentType.objects.get_for_model(projects_model),
            ContentType.objects.get_for_model(tache_model),
        ]
    )

    # Permissions spécifiques au Client
    devis_permissions = Permission.objects.filter(
        content_type=ContentType.objects.get_for_model(devis_model), codename__startswith='view_'
    )
    facture_permissions = Permission.objects.filter(
        content_type=ContentType.objects.get_for_model(facture_model), codename__startswith='view_'
    )
    projet_permissions = Permission.objects.filter(
        content_type=ContentType.objects.get_for_model(projects_model), codename__startswith='view_'
    )

    # Combiner toutes les permissions pour les clients
    client_permissions = list(devis_permissions) + list(facture_permissions) + list(projet_permissions)

    # ASSIGNATION DES PERMISSIONS AUX GROUPES
    admin_group.permissions.set(admin_permissions)  # Tout accès pour administrateurs
    employe_group.permissions.set(employe_permissions)  # Employés spécifiques
    client_group.permissions.set(client_permissions)  # Clients spécifiques

    print("Rôles et permissions créés avec succès !")