import logging
import os

from django.core.files.base import ContentFile
from django.db import models
from django.template.loader import render_to_string

from django.templatetags.static import static


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

# ✅ Modèle Sous-service
class SubService(models.Model):
    # Sous-service de base avec son nom
    name = models.CharField(max_length=100, verbose_name="Nom du sous-service")

    def __str__(self):
        return self.name
    
# ✅ Modèle Services
class Service(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to= 'images', blank=True, null=True)
    date_creation = models.DateField(auto_now=True)
    # une categorie contient plusieurs services.
    categorie = models.ForeignKey(Categorie, related_name='services', on_delete=models.CASCADE)
    # Pour recuperer tous les sous services associés à un service(optionnel)
    sub_services = models.ManyToManyField(SubService, through='ServicePricing', related_name='services')

    class Meta:
        ordering = ['-date_creation'] #LIFview
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.nom

    def get_absolute_url(self):

        return reverse('home')
    
#######################################################################

class ServicePricing(models.Model):
    # Table intermédiaire pour gérer les prix variables par service
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    sub_service = models.ForeignKey(SubService, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")

    class Meta:
        unique_together = ('service', 'sub_service')  # Évite les doublons

    def __str__(self):
        return f"{self.service} - {self.sub_service} : {self.price}"

from utilisateurs.models import User

# ✅ Modèle Demande
class DemandeService(models.Model):

    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True) # mise à jour a chaque modification
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="demandes") # est demandé N fois
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="demandes") # demande N fois
    fichier = models.FileField(upload_to='demandes/', blank=True, null=True)  # Permetre de stocke un fichier dans la demande
    sub_services = models.ManyToManyField(SubService, through='SelectedSubService', related_name='service_requests')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant total",default=0)

    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('VALIDÉ', 'Validé'),
        ('REFUSÉ', 'Refusé'),
    ]
    statut = models.CharField(max_length=12, choices=STATUT_CHOICES, default='EN_ATTENTE')

    class Meta:
        ordering = ['-date_creation']  #LIFview
        verbose_name = "DemandeService"
        verbose_name_plural = "DemandeServices"


    def __str__(self):
        return f"Demande {self.pk} - {self.statut}"
class SelectedSubService(models.Model):
    # Stockage des sous-services sélectionnés avec leur prix au moment de la demande
    service_request = models.ForeignKey(DemandeService, on_delete=models.CASCADE)
    sub_service = models.ForeignKey(SubService, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('service_request', 'sub_service')

    def __str__(self):
        return f"{self.sub_service} - {self.price}"  
############################################################################
# model devis
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location='media/devis')

class Devis(models.Model):
    demande = models.ForeignKey(DemandeService, related_name='devis', on_delete=models.CASCADE)    
    """ demande = models.OneToOneField(DemandeService, on_delete=models.CASCADE, related_name='devis') """
    fichier = models.FileField(upload_to='devis/', null=True, blank=True)  #  stocker les fichiers dans media/devis/.
    date_creation = models.DateTimeField(auto_now_add=True)
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('VALIDÉ', 'Validé'),
        ('REFUSÉ', 'Refusé'),
    ]
    statut = models.CharField(max_length=12, choices=STATUT_CHOICES, default='EN_ATTENTE')

    class Meta:
        ordering = ['-date_creation']  # LIFview
        verbose_name = "Devis"
        verbose_name_plural = "Devis"

    def __str__(self):
        return f"Devis {self.pk} - {self.demande.client.username}"
    
###############################################################

class Facture(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="factures")
    description = models.TextField(null=True, max_length=1000, blank=True)

    date_creation = models.DateField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True, null=True, blank=True)

    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    taxe = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)  # TVA optionnelle

    devis = models.OneToOneField(Devis, on_delete=models.CASCADE, related_name="facture", null=True, blank=True)

    STATUT_CHOICES = [
        ('PAYEE', 'Payée'),
        ('IMPAYEE', 'Impayée'),
    ]
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='IMPAYEE')

    INVOICE_TYPE = [
        ('R', 'RECEIPT'),
        ('P', 'PROFORMA INVOICE'),
        ('I', 'INVOICE'),
    ]
    invoice_type = models.CharField(max_length=15, choices=INVOICE_TYPE)

    fichier_pdf = models.FileField(upload_to='factures/', blank=True, null=True)  # Stocke le fichier PDF

    mode_paiement = models.CharField(
        max_length=50,
        choices=[('CB', 'Carte Bancaire'), ('VIREMENT', 'Virement'), ('CHEQUE', 'Chèque')],
        default='CB'
    )

    numero_facture = models.CharField(max_length=20, unique=True, blank=True, null=True)  # Numéro de facture unique

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Facture"
        verbose_name_plural = "Factures"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # D'abord, on sauvegarde pour générer un ID

        if not self.numero_facture:
            self.numero_facture = f"FAC-{self.pk:06d}"  # Maintenant, self.pk existe
            super().save(*args, **kwargs)  # On resauvegarde avec le numéro de facture
        self.total_ttc = self.montant + (self.montant * (self.taxe / 100)) if self.taxe else self.montant
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_facture or self.pk} - {self.montant} FCFA"

    def get_client(self):
        """Retourne le client via la relation Devis → DemandeService → Client"""
        return self.devis.demande.client if self.devis and self.devis.demande else None

    def get_service(self):
        """Retourne le service via la relation Devis → DemandeService → Service"""
        return self.devis.demande.service if self.devis and self.devis.demande else None

    def generate_pdf(self):
        """Générer un fichier PDF pour la facture."""
        context = {'facture': self}  # context à injecter dans le HTML
        html_string = render_to_string('facture_template.html', context)  # conversion en HTML
        # Inclure le CSS
        css_path = os.path.join(settings.STATIC_ROOT, 'css/facture.css')
        pdf_file = HTML(string=html_string).write_pdf(stylesheets=[CSS(css_path)])

        # Enregistrer le fichier PDF dans le modèle
        filename = f"facture_{self.pk}.pdf"
        if self.fichier_pdf:
            self.fichier_pdf.delete(save=False)  # Supprime l'ancienne version si elle existe
        self.fichier_pdf.save(filename, ContentFile(pdf_file), save=True)



####################################################################################

