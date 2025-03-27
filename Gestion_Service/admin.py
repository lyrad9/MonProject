from django.conf import settings
from django.contrib import admin
from django.core.mail import send_mail

from Gestion_Service.models import Facture, DemandeService, Service, Categorie, Devis


#Affichage des MODELS dans ADMIN ############################################

class AdminService(admin.ModelAdmin):
    list_display = ('nom', 'date_creation','categorie')
    list_filter = ('categorie',)
    search_fields = ('nom','description')

#################################################################
class AdminCategorie(admin.ModelAdmin):
    list_display = ('nom','date_creation')
    search_fields = ('nom',)


####################################################################
class AdminFacture(admin.ModelAdmin):
    list_display = ('devis' ,'get_client', 'get_service', 'date_creation','statut','bouton_generer_facture')
    list_filter = ('statut', 'devis')
    readonly_fields = ('date_creation',)
    actions = ['generer_pdf']


    def get_client(self, obj):
        return obj.get_client()
    get_client.short_description = "Client"

    def get_service(self, obj):
        return obj.get_service()
    get_service.short_description = "Service"
#
    def bouton_generer_facture(self, obj):
        """Ajoute un bouton pour générer la facture en PDF directement depuis l'admin."""
        if obj.pk:  # Vérifie que la facture a bien un ID
            url = reverse("facture_pdf", args=[obj.pk])  # Génère l'URL vers la vue de génération PDF

            # format_html() est utilisé pour afficher un bouton cliquable.
            return format_html('<a class="button" href="{}" target="_blank">📄 Générer PDF</a>', url)
        return "Pas de facture"

    bouton_generer_facture.short_description = "Générer la facture PDF"

    def generer_pdf(self, request, queryset):
        """Générer les factures PDF pour les factures sélectionnées."""
        for facture in queryset:
            facture.generate_pdf() # appele de la fonction qui genere la facture
        self.message_user(request, "Factures générées avec succès.")

    generer_pdf.short_description = "Générer les factures PDF"

##############################################################################

class AdminDemandeService(admin.ModelAdmin):
    # Définition des colonnes visibles dans la liste des demandes
    list_display = ('service', 'statut', 'client', 'date_creation', 'fichier_link')

    # Ajout de filtres pour faciliter la recherche
    list_filter = ('statut', 'date_creation')

    # Les champs en lecture seule (l'admin ne peut pas les modifier directement)
    readonly_fields = ('date_creation',)

    # Ajout des actions personnalisées
    actions = ['valider_demandes', 'refuser_demandes']

    def fichier_link(self, obj):
        """
        Affiche un lien de téléchargement si un fichier est joint à la demande.
        """
        if obj.fichier:
            return format_html('<a href="{}" target="_blank">Télécharger</a>', obj.fichier.url)
        return "Aucun fichier"

    # Nom personnalisé pour la colonne dans l'admin
    fichier_link.short_description = "Fichier"

    def valider_demandes(self, request, queryset):
        """
        Action permettant de valider plusieurs demandes en une seule fois.
        - Met à jour le statut des demandes en "VALIDÉE"
        - Envoie un email automatique aux clients concernés
        """
        #QuerySet (une liste d'objets Django).

        queryset.update(statut='VALIDÉE')  # Met à jour toutes les demandes sélectionnées

        for demande in queryset:
            self.envoyer_email_notification(demande, "validée")  # Envoi d'un email au client

        self.message_user(request, "Les demandes sélectionnées ont été validées avec succès.")

    # Nom affiché dans le menu des actions admin
    valider_demandes.short_description = "Valider les demandes sélectionnées"

    def refuser_demandes(self, request, queryset):
        """
        Action permettant de refuser plusieurs demandes en une seule fois.
        - Met à jour le statut des demandes en "REFUSÉE"
        - Envoie un email automatique aux clients concernés
        """
        queryset.update(statut='REFUSÉE')  # Met à jour toutes les demandes sélectionnées

        for demande in queryset:
            self.envoyer_email_notification(demande, "refusée")  # Envoi d'un email au client

        self.message_user(request, "Les demandes sélectionnées ont été refusées.")

    # Nom affiché dans le menu des actions admin
    refuser_demandes.short_description = "Refuser les demandes sélectionnées"

    def envoyer_email_notification(self, demande, statut):
        """
        Envoie un email au client lorsque sa demande est validée ou refusée.
        - Paramètres :
            - demande : L'objet DemandeService concerné
            - statut : "validée" ou "refusée"
        """
        sujet = f"Votre demande a été {statut}"
        message = f"""
        Bonjour {demande.client.username},

        Votre demande de service a été {statut} par l'administrateur.

        Détails de votre demande :
        - ID : {demande.id}
        - Service : {demande.service.nom}
        - Date de création : {demande.date_creation.strftime('%d/%m/%Y')}

        Merci de votre confiance.
        """
        # Envoi de l'email au client
        send_mail(sujet, message, settings.DEFAULT_FROM_EMAIL, [demande.client.email])


############################################################################################
from django.urls import reverse
from django.utils.html import format_html


class AdminDevis(admin.ModelAdmin):
    list_display = ('id','demande', 'fichier','date_creation','bouton_generer_devis',)
    search_fields = ('fichier',)
    readonly_fields = ('date_creation',)

    def bouton_generer_devis(self, obj):
        if obj.demande:
            url = reverse("generate_devis_pdf", args=[obj.demande.id])  # URL vers la vue de génération, 
            return format_html('<a class="button" href="{}">Générer le PDF</a>', url)
        return "Pas de demande liée"
    
    bouton_generer_devis.short_description = "Générer le devis"



# Register your models here. ###################################################
admin.site.register(Categorie,AdminCategorie)
admin.site.register(Service,AdminService)
admin.site.register(DemandeService,AdminDemandeService)
admin.site.register(Facture,AdminFacture)
admin.site.register(Devis,AdminDevis)

