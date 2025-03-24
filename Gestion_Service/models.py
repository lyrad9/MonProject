import gc
import logging
import os


from MySQLdb.constants.FIELD_TYPE import DECIMAL
from django.core.files.base import ContentFile
from django.db import models
from django.template.loader import render_to_string

from django.templatetags.static import static
from weasyprint import HTML, CSS

from AppGestionService import settings

logger = logging.getLogger(__name__)


# mes class => tables de ma BD


################################################## #####################################

# ✅ Modèle Catégorie
class Categorie(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(default= "")
    date_creation =models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation'] #LIFVIEW

    def __str__(self):
        return self.nom


###########################################################################

from django.urls import reverse

# ✅ Modèle Services
class Service(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to= 'images', blank=True, null=True)
    date_creation = models.DateField(auto_now=True)
    # une categorie contient plusieurs services.
    categorie = models.ForeignKey(Categorie, related_name = 'services',on_delete= models.CASCADE)

    class Meta:
        ordering = ['-date_creation'] #LIFview
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.nom

    def get_absolute_url(self):

        return reverse('home')
    
#######################################################################

from utilisateurs.models import User

# ✅ Modèle Demande
class DemandeService(models.Model):

    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True) # mise à jour a chaque modification
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="demandes") # est demandé N fois
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="demandes") # demande N fois
    fichier = models.FileField(upload_to='demandes/', blank=True, null=True)  # Permetre de stocke un fichier dans la demande lors de l'envois.

    #sattut de la demande
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('VALIDÉE', 'Validée'),
        ('REFUSÉE', 'Refusée'),
    ]
    statut = models.CharField(max_length=12, choices=STATUT_CHOICES, default='EN_ATTENTE')

    class Meta:
        ordering = ['-date_creation']  #LIFview
        verbose_name = "DemandeService"
        verbose_name_plural = "DemandeServices"


    def __str__(self):
        return f"Demande {self.pk} - {self.statut}"
    
############################################################################
# model devis
from django.core.files.storage import FileSystemStorage
from decimal import Decimal

fs = FileSystemStorage(location='media/devis')

class Devis(models.Model):

    demande = models.OneToOneField(DemandeService, on_delete=models.CASCADE, related_name='devis')
    fichier = models.FileField(upload_to='devis/', storage=fs,null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    duree = models.IntegerField(default=10,help_text="en jours")

    # Champs pour les détails de la prestation
    description = models.TextField(default="")  # Ex: "Développement d'application web avec Django et React"

    validite = models.DateField(auto_now=True)  #

    cout_backend = models.DecimalField(max_digits=15, decimal_places=2,default=0, help_text="Coût_back-end")
    cout_frontend = models.DecimalField(max_digits=15, decimal_places=2, default=0,help_text="Coût_front-end")
    cout_test = models.DecimalField(max_digits=15, decimal_places=2, default=0,help_text="Coût_test") # cout pour les tests
    cout_maintenance = models.DecimalField(max_digits=15, decimal_places=2, default=0,help_text="Coût_maintenance")

    cout_hebergement = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, help_text=" Coût_l'hébergement")
    cout_nom_de_domaine = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, help_text="Coût_nom de domaine")

    # Statut du devis
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('VALIDÉ', 'Validé'),
        ('REFUSÉ', 'Refusé'),
    ]
    statut = models.CharField(max_length=12, choices=STATUT_CHOICES, default='EN_ATTENTE')

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Devis"
        verbose_name_plural = "Devis"

    def __str__(self):
        return f"Devis {self.pk} - {self.demande.client.username}"

    # Fonctions pour calculer les montants

    def calcul_total_ht(self):
        """ Calcule le total hors taxes (HT). """
        return sum(filter(None, [ # filter(None) pour ignorer les valeurs null
            self.cout_backend,
            self.cout_frontend,
            self.cout_test,
            self.cout_maintenance,
            self.cout_hebergement,
            self.cout_nom_de_domaine

        ]))

    def calcul_tva(self):

        """ Calcule la TVA sur le total HT. Par défaut, TVA à 20%. """
        taux_tva= Decimal("0.20")
        return self.calcul_total_ht() * taux_tva

    def calcul_total_ttc(self):
        """ Calcule le total TTC (HT + TVA). """
        return self.calcul_total_ht() + self.calcul_tva()

###############################################################

class Facture(models.Model):

    description = models.TextField(null=True, max_length=1000, blank=True)

    date_creation = models.DateField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True, null=True, blank=True)

    validite = models.DateField(auto_now=True)  # LE delai de paiment

    devis = models.OneToOneField(Devis, on_delete=models.CASCADE, related_name="facture", null=True, blank=True)

    STATUT_CHOICES = [
        ('PAYEE', 'Payée'),
        ('IMPAYEE', 'Impayée'),
        ('EN_ATTENTE', 'En attente'),
    ]
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='EN_ATTENTE')

    quantite = models.IntegerField(default=10,help_text="en jours")  # nombre de temps pour rendre le service

    invoice_type = models.CharField(max_length=15,default='FACTURE',  help_text='type_document')

    fichier_pdf = models.FileField(upload_to='factures/', blank=True, null=True)  # Stocke le fichier PDF

    numero_facture = models.CharField(max_length=20, unique=True, blank=True, null=True)  # Numéro de facture unique

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Facture"
        verbose_name_plural = "Factures"

    def save(self, *args, **kwargs):
        if not self.numero_facture:
            super().save(*args, **kwargs)  # D'abord, on sauvegarde pour obtenir un ID
            self.numero_facture = f"FAC-{self.pk:06d}"  # Génération du numéro
        super().save(*args, **kwargs)  # Sauvegarde finale

    def __str__(self):
        return f"{self.numero_facture or self.pk} - {self.montant_ttc} FCFA"

        # ✅ Propriétés pour récupérer les valeurs du devis
    @property
    def montant_ht(self):
            return self.devis.calcul_total_ht() if self.devis else Decimal("0.00")

    @property
    def montant_tva(self):
            return self.devis.calcul_tva() if self.devis else Decimal("0.00")

    @property
    def montant_ttc(self):
            return self.devis.calcul_total_ttc() if self.devis else Decimal("0.00")

    def get_client(self):
        """Retourne le client via la relation Devis → DemandeService → Client"""
        if self.devis and self.devis.demande:
            return self.devis.demande.client
        return None  # Evite les erreurs

    def get_service(self):
        """Retourne le service via la relation Devis → DemandeService → Service"""
        if self.devis and self.devis.demande:
            return self.devis.demande.service
        return None  # Evite les erreurs

############################################################################################

    def generate_pdf(self):
        """Générer un fichier PDF pour la facture."""

        # On suppose que 'self' est l'instance de la facture
        client = self.get_client()  # Assure-toi que 'get_client' existe dans ton modèle Facture

        context = {
            # Informations du client
            "client_nom": client.username if client else "Inconnu",
            "client_email": client.email if client else "inconnu@example.com",
            "client_entreprise": client.entreprise if client else "Nom entreprise non défini",
            # Si c'est le nom de l'entreprise
            "client_adresse": client.adresse if client else "Pas d'adresse mentionnée",

            # Informations de la facture
            "validite": self.validite,
            "description": self.description,
            "duree": self.quantite,
            "date_creation": self.date_creation,

            # Coûts détaillés
            "total_ht": self.montant_ht,
            "tva": self.montant_tva,
            "total_ttc": self.montant_ttc,

            # Assurer que la facture actuelle est dans le contexte
            "facture": self.numero_facture
        }

        try:
            # Charger le template HTML et passer le contexte
            html_string = render_to_string('facture_template.html', context)

            print("🧐 Contexte envoyé au template:", context)

            print("🔎 HTML généré avant PDF:\n", html_string)

            # Vérifier que le fichier CSS existe
            css_path = os.path.join(settings.BASE_DIR, 'static/css/facture.css')

            # verifier si le fichier existe
            if not os.path.exists(css_path):
                print("⚠️ Le fichier CSS est introuvable")
                return False  # Échec de la génération du PDF
#########################################################################
            from django.templatetags.static import static


            # Générer le PDF à partir du HTML en incluant le css
            pdf_file = HTML(string=html_string).write_pdf(stylesheets=[CSS(css_path)])

            # Nom du fichier PDF
            filename = f"facture_{self.pk}.pdf"

            # Supprimer l'ancienne version du fichier PDF s'il existe
            if self.fichier_pdf:
                self.fichier_pdf.close() # ferme le fichier s'il est ouvert
                self.fichier_pdf.delete(save=True)  # Supprime l'ancienne version et enregistre

                print(self.fichier_pdf ,"supprime")

                # Sauvegarder le fichier PDF
            self.fichier_pdf.save(filename, ContentFile(bytes(pdf_file)), save=False)
            self.save()
            return True  # Succès de la génération

        except Exception as e:
            import traceback
            print("❌ Erreur lors de la génération du PDF :", str(e))
            print(traceback.format_exc())

####################################################################################

