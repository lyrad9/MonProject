import os
import logging
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from Gestion_Service.models import DemandeService, Service, Devis, ServicePricing
from utilisateurs.models import User
from .forms import ServiceRequestForm

# Create your views here.

""" @login_required """
def create_service_request(request, service_id):
    """
    Vue pour créer une nouvelle demande de service
    """
    service = get_object_or_404(Service, id=service_id)
    subservices = ServicePricing.objects.filter(service=service)
    data = [{'id': ss.sub_service.id, 'name': ss.sub_service.name, 'price': str(ss.price)} for ss in subservices]

    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Créer la demande sans la sauvegarder
            service_request = form.save(commit=False)
            service_request.service = service
            service_request.client = request.user
            service_request.statut = 'EN_ATTENTE'
            
            # Calculer le montant total
            selected_subservices = ServicePricing.objects.filter(
                service=service,
                sub_service__id__in=request.POST.getlist('sub_services')
            )
            service_request.price = sum(ss.price for ss in selected_subservices)
            
            # Sauvegarder la demande
            service_request.save()
            
            # Ajouter les sous-services sélectionnés
            for pricing in selected_subservices:
                service_request.sub_services.add(pricing.sub_service, through_defaults={'price': pricing.price})
            
            messages.success(request, 'Votre demande a été créée avec succès !')
            """return redirect('request_detail', pk=service_request.pk)"""
        else:
            messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
    else:
        form = ServiceRequestForm()
    
    return render(request, 'services/create_request.html', {
        'form': form,
        'service': service,
        'subservices': data,
    })

def service_comptabilite(request):
    # Ici, tu peux récupérer les informations spécifiques du client (comme entreprise).

    return render(request, 'services/service_comptabilite.html')

def service_gl(request):

    services = Service.objects.all()
   

    return render(request, 'services/service_gl.html',{'services':services})


# pour traiter une demande de service
def devis_form(request):
    # Récupérer tous les services disponibles pour le formulaire
    services = Service.objects.all()
    show_modal = False  # Par défaut, ne pas afficher la modale

    # Si la méthode HTTP est POST, cela signifie que le formulaire a été soumis
    if request.method == "POST":
        # Récupérer les données soumises par l'utilisateur
        description = request.POST.get("details")
        service_id = request.POST.get("service")
        fichier = request.FILES.get("fichier")

        # Vérification de la validité du service
        try:
            service = Service.objects.get(id=int(service_id))
        except (ValueError, Service.DoesNotExist):
            messages.error(request, "Service invalide.")
            return render(request, "devis.html", {"services": services})

        # Si l'utilisateur n'est pas connecté, stocker la demande en session (request. session).
        if not request.user.is_authenticated:
            request.session['demandeservice_temp'] = {
                'description': description,
                'service_id': service_id,
                'fichier': fichier.name if fichier else None  # Stocke seulement le nom du fichier
            }

            show_modal = True  # Activer la fenêtre modale
            # Afficher un message et rediriger l'utilisateur pour qu'il se connecte ou s'inscrive
            messages.info(request, "Veuillez vous inscrire ou vous connecter pour soumettre votre demande.")

            return render(request, "devis.html", {"show_modal": show_modal, "services": services})  # Afficher une fenêtre modale

        # Si l'utilisateur est connecté, traiter normalement la demande
        else:
            # Récupérer les données soumises par l'utilisateur depuis le formulaire
            description = request.POST.get("details")
            service_id = request.POST.get("service")
            fichier= request.FILES.get("fichier")

            print("Service ID reçu :", service_id)  # Débogage : afficher l'ID du service
            print("fichier envoyer:",fichier)

            # Vérification que l'ID du service est valide
            try:
                service = Service.objects.get(id=int(service_id))  # Récupérer l'objet Service correspondant à l'ID
            except (ValueError, Service.DoesNotExist):  # Si l'ID n'est pas valide ou si le service n'existe pas
                messages.error(request, "Service invalide.")
                return render(request, "devis.html", {"services": services})  # Réafficher le formulaire

            # Créer la demande de service (DemandeService) dans la base de données
            demandeservice_temp = DemandeService.objects.create(
                description=description,
                service=service,
                fichier=fichier,  # stockage du fichier
                montant=0,  # Le montant sera mis à jour plus tard
                client=request.user,  # Associe la demande à l'utilisateur (client) qui l'a soumise
                statut='EN_ATTENTE'  # La demande est initialement en attente
            )

            # Vérifier si l'utilisateur est un administrateur ou un client
            if request.user.is_staff:  # Si l'utilisateur est un administrateur
                messages.info(request, "Un nouveau devis a été soumis par un client.")
                return redirect('/admin/Gestion_Service/demandeservice/')

            # Rediriger l'admin vers son espace d'administration

            else:  # Si l'utilisateur est un client

                messages.success(request, "Votre demande de service a été envoyée avec succès !")
                return redirect("client_dashbord")

                # Si la méthode HTTP n'est pas POST (c'est-à-dire que la page est juste visitée ou que le formulaire a échoué).
    return render(request, "devis.html", {"services": services})

####################################################################################3
#  fonction pour recuperer les devis et clients connecte
from django.contrib.auth.decorators import login_required
from .models import  Facture, ServicePricing
from django.shortcuts import render
from .models import Facture, Devis, DemandeService


@login_required
def dashboard(request):
    user = request.user

    # Récupérer les demandes de l'utilisateur
    demandes_attente = DemandeService.objects.filter(client=user, statut='EN_ATTENTE').count()
    demandes_validees = DemandeService.objects.filter(client=user, statut='VALIDÉ').count()
    demandes_refusees = DemandeService.objects.filter(client=user, statut='REFUSÉ').count()

    #On récupère les Devis en filtrant via demande__client=user.
    devis_attente = Devis.objects.filter(demande__client=user, statut='EN_ATTENTE').count()
    devis_validees = Devis.objects.filter(demande__client=user, statut='VALIDÉ').count()
    devis_refusees = Devis.objects.filter(demande__client=user, statut='REFUSÉ').count()


    # Récupérer les factures de l'utilisateur
    factures_impayees = Facture.objects.filter(devis__demande__client=user, statut='IMPAYEE').count()
    factures_payees = Facture.objects.filter(devis__demande__client=user, statut='PAYEE').count()


    context = {
        'demandes_attente': demandes_attente,
        'demandes_validees': demandes_validees,
        'demandes_refusees': demandes_refusees,
        'devis_attente': devis_attente,
        'devis_validees': devis_validees,
        'devis_refusees': devis_refusees,
        'factures_impayees': factures_impayees,
        'factures_payees': factures_payees
    }

    return render(request, 'users/clients.html', context)

####################################################################################
# vue Django pour fournir des statistiques sur les demandes de service et les factures de l'utilisateur connecté.

from django.http import JsonResponse, FileResponse  # classe permet de renvoyer une réponse HTTP au format JSON



@login_required
def refresh_dashboard(request):
    #récupèration de l'utilisateur actuellement connecté a partir de l'objet request
    user = request.user

#dictionnaire Python qui contient différentes statistiques basées sur les demandes de service et les factures de l'utilisateur connecté.
    data = {
        "demandes_en_attente": DemandeService.objects.filter(client=user, statut='EN_ATTENTE').count(),
        "demandes_validees": DemandeService.objects.filter(client=user, statut='VALIDÉ').count(),
        "demandes_refusees": DemandeService.objects.filter(client=user, statut='REFUSÉ').count(),
        "devis_attente": Devis.objects.filter(demande__client=user, statut='EN_ATTENTE').count(),
        "devis_validees": Devis.objects.filter(demande__client=user, statut='VALIDÉ').count(),
        "devis_refusees": Devis.objects.filter(demande__client=user, statut='REFUSÉ').count(),
        "factures_impayees": Facture.objects.filter(devis__demande__client=user, statut='IMPAYEE').count(),
        "factures_payees": Facture.objects.filter(devis__demande__client=user, statut='PAYEE').count(),


    }
#renvoie le dictionnaire data au format JSON
    return JsonResponse(data)


#######################################################################
#vue Django qui génère un devis en PDF pour une demande de service spécifique, 
# le stocke dans la base de données, et renvoie un lien pour le télécharger.

from django.http import HttpResponse
from django.core.files.base import ContentFile
# from weasyprint import HTML, CSS
from django.conf import settings


@login_required
def generate_devis_pdf(request, demande_id):  #http://127.0.0.1:8000/devis/generer/20/ id du devis dans la BD/
    """
    Génère un devis en PDF, le stocke dans la base de données et retourne un lien de téléchargement.
    """

    # 🔹 1. Vérifier si un devis existe déjà pour cette demande et récupérer la demande de service correspondant à l'ID (demande_id).
    try:
        # Récupérer la demande
        demande = get_object_or_404(DemandeService, id=demande_id)
    except DemandeService.DoesNotExist:
        return HttpResponse("Demande de service non trouvée", status=404)

    # Vérifier si la demande est liée à un utilisateur (client)
    if not demande.client:
        return HttpResponse("Erreur : cette demande n'a pas de client associé.", status=404)

    
    # Affichage des informations de la demande et de l'utilisateur pour déboguer
    print(demande.client)
    print("Demande Service ID:", demande.id)
    print("Client associé : ", demande.client.username)

    # récupérer un devis existant pour cette demande. S'il n'existe pas, on en crée un nouveau.
    # "created" = booléen qui indique si le devis a été créé (True) ou s'il existait déjà (False).
    devis, created = Devis.objects.get_or_create(demande=demande)

    # Si un devis existe déjà et qu'il a déjà un fichier PDF associé, on renvoie un lien pour télécharger ce fichier.
    if not created and devis.fichier:
        return HttpResponse(f"Devis déjà existant ! <a href='{devis.fichier.url}' target='_blank'>Télécharger</a>")


    #2.dictionnaire context qui contient toutes les informations nécessaires pour générer le devis (nom du client, email, entreprise, etc.).

    client = demande.client

    context = {
        "client_nom": client.username,
        "client_email": client.email,
        "client_entreprise": client.first_name,
        "devis": devis,
        
    }

    # 🔹 3. générer le contenu HTML du devis en utilisant le contexte défini précédemment.

    html_content = render(request, 'devis/devis_template.html', context).content.decode()

    # 🔹 4. convertit le contenu HTML en fichier PDF en utilisant une bibliothèque comme WeasyPrint
    pdf_file = HTML(string=html_content).write_pdf()

#################### Enregistrement du fichier PDF

    # 🔹 5. Définir le chemin et enregistrer le fichier
    devis_filename = f"devis_{demande.id}.pdf"
    devis_path = os.path.join(settings.MEDIA_ROOT, 'devis', devis_filename)

    # S'assurer que le dossier existe
    os.makedirs(os.path.dirname(devis_path), exist_ok=True)

    '''Écrire le fichier sur le disque
    with open(devis_path, 'wb') as f:
        f.write(pdf_file)'''

    # Si un fichier PDF existait déjà pour ce devis, on le supprime avant d'enregistrer le nouveau.
    if devis.fichier:
        devis.fichier.delete(save=False)

    # Cela supprime le fichier précédent, et enregistrer la modification dans la base de données

    # 🔹 6. On enregistre le fichier PDF dans le champ fichier du modèle Devis.
    devis.fichier.save(devis_filename, ContentFile(pdf_file), save=True)

    # envoyer email à l'utilisateur correspondant

    if devis.demande:
        service_nom = devis.demande.service.nom
    else:
        service_nom = "service inconnu"


    send_mail(
        subject='devis envoye',
        message=f"Votre devis pour un {service_nom} a ete envoyer. /n Veuillez vous connectez pour le voir.",
        from_email=settings.ADMIN_EMAIL,
        recipient_list=[demande.client.email],
        fail_silently=False,
    )

    print(f"Email envoyé à {demande.client.email}")

    # 🔹 7. renvoie une réponse HTTP avec un lien pour télécharger le fichier PDF.
    pdf_url = settings.MEDIA_URL + f"devis/{devis_filename}"
    return HttpResponse(f"Devis généré avec succès ! <a href='{pdf_url}' target='_blank'>Télécharger le PDF</a>")


######################################################
# methode pour supprimer l'ancien fichier lorsqu'un devis est supprime.

def delete(self, *args, **kwargs):
    if self.fichier:
        self.fichier.delete(save=False)
    super().delete(*args, **kwargs)

###################################################3
# vue Django qui permet à un utilisateur connecté de voir la liste des devis associés à son compte,
#  en fonction d'un statut spécifique (par exemple, "EN_ATTENTE", "VALIDÉ", ou "REFUSÉ").

@login_required
def voir_devis(request, statut):  
    """
    Affiche les devis de l'utilisateur en fonction de leur statut (EN_ATTENTE, VALIDÉ, REFUSÉ)
    """
    user = request.user
    
    #Filtrage des devis par utilisateur et statut
    #On utilise le modèle Devis pour récupérer tous les devis qui correspondent à deux critères (le client associe a la demande et le statut)
    devis_list = Devis.objects.filter(demande__client=user, statut=statut,)

    #fonction "render"  pour afficher un template HTML (devis/voir_devis.html) en lui passant un contexte (un dictionnaire de données).

    return render(request, 'devis/voir_devis.html', {'devis_list': devis_list, 'statut': statut,})


########################################################

# modifier le devis

# views.py


''''@login_required
def edit_devis(request, devis_id):
    """
    Permet au client de modifier son devis
    """
    devis = get_object_or_404(Devis, id=devis_id)

    # Vérifier que le devis appartient à l'utilisateur connecté
    if devis.demande.client != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à modifier ce devis.")
        return redirect('client_dashboard')

    if request.method == 'POST':
        # Récupération des données du formulaire HTML
        nouveau_montant = request.POST.get("montant")
        nouvelle_description = request.POST.get("description")

        if nouveau_montant and nouvelle_description:
            devis.montant = float(nouveau_montant)  # Conversion en float pour éviter les erreurs
            devis.description = nouvelle_description
            devis.save()

            # Envoyer un email à l'administrateur pour informer de la modification
            send_mail(
                'Devis modifié',
                f'Le devis avec l\'ID {devis.id} a été modifié par {request.user.username}.',
                request.user.email,  # email du client
                [settings.ADMIN_EMAIL],  # email de l'admin défini dans settings
                fail_silently=False,
            )

            messages.success(request, "Votre devis a été modifié avec succès !")
            return redirect('client_dashboard')

        else:
            messages.error(request, "Veuillez remplir tous les champs.")

    return render(request, 'devis/edit_devis.html', {'devis': devis})

#############################################################
#valider le devis

# views.py

@login_required
def validate_devis(request, devis_id):
    """
    Permet au client de valider son devis
    """
    devis = get_object_or_404(Devis, id=devis_id)

    # Vérifier que le devis appartient à l'utilisateur connecté (le client)
    if devis.demande.client != request.user:
        messages.success(request, "Votre demande a echouée !")
        return redirect('client_dashbord')  # Rediriger si ce n'est pas le bon client

    # Mettre à jour le statut du devis à "validé"
    devis.status = 'VALIDÉ'  # Assurer que le statut 'VALIDÉ' existe dans ton modèle
    devis.save()

    # Envoyer un email à l'administrateur pour l'informer que le devis a été validé
    send_mail(
        'Devis validé',
        f'Le devis avec l\'ID {devis.id} a été validé par le client.',
        request.user.email,
        [settings.ADMIN_EMAIL],
        fail_silently=False,
    )
    messages.success(request,'votre devis a ete valide avec success. ')
    return redirect('client_dashbord')  # Rediriger après validation'''


###############################3###########################
#GENERER LA FACTURE

def facture_pdf_view(request, facture_id):
    """Vue pour générer et afficher une facture en PDF."""
    facture = Facture.objects.filter(pk=facture_id).first()
    if not facture:
        return HttpResponse("Facture introuvable", status=404)

    context = {'facture': facture}
    html_string = render_to_string('facture_template.html', context)

    # ✅ Vérification avant d'utiliser STATIC_ROOT
    css_path = os.path.join(settings.STATIC_ROOT, 'css/facture.css') if settings.STATIC_ROOT else None

    # ✅ Vérifie que le fichier CSS existe avant de l'ajouter
    stylesheets = [CSS(css_path)] if css_path and os.path.exists(css_path) else []

    pdf_file = HTML(string=html_string).write_pdf(stylesheets=stylesheets)

    '''   if facture.devis:
        service_nom = facture.devis.demande.service.nom
    else:
        service_nom = "service inconnu"

    send_mail(
        subject='devis envoye',
        message=f"Votre devis pour un {service_nom} a ete envoyer. /n Veuillez vous connectez pour le voir.",
        from_email=settings.ADMIN_EMAIL,
        recipient_list=[devis.client.email],
        fail_silently=False,
    )

    print(f"Email envoyé à {demande.client.email}")'''

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="facture_{facture.pk}.pdf"'
    return response

#####################################

def telecharger_facture(request, facture_id): # http://127.0.0.1:8000/facture/1/download/.

    """Permet de télécharger une facture en PDF."""
    facture = Facture.objects.get(pk=facture_id)
    if facture.fichier_pdf:
        return FileResponse(facture.fichier_pdf.open(), content_type='application/pdf')
    else:
        return HttpResponse("Facture non disponible", status=404)

@login_required
def request_detail(request, pk):
    """
    Vue pour afficher les détails d'une demande de service
    """
    demande = get_object_or_404(DemandeService, pk=pk, client=request.user)
    
    context = {
        'demande': demande,
        'subservices': demande.sub_services.all(),
    }
    
    return render(request, 'services/request_detail.html', context)


