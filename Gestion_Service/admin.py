
from django.contrib import admin
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
    list_display = ('montant', 'devis' ,'get_client', 'get_service', 'date_creation','statut','bouton_generer_facture')
    list_filter = ('statut', 'devis')
    search_fields = ('statut',)
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
    list_display = ('service', 'statut', 'client','date_creation','fichier_link')
    list_filter = ('statut', 'date_creation')
    search_fields = ('statut',)
    readonly_fields = ('date_creation',)

    def fichier_link(self, obj):
        if obj.fichier:
            return format_html('<a href="{}" target="_blank">Télécharger</a>', obj.fichier.url)  # Correction ici
        return "Aucun fichier"
    
    fichier_link.short_description = "Fichier"

    actions = ['marquer_comme_traite']

    def marquer_comme_traite(self, request, queryset):
        queryset.update(statut='Traité')
        self.message_user(request, "Les demandes ont été marquées comme traitées.")
    marquer_comme_traite.short_description = "Marquer comme traité"


#############################################################################
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

