from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect

from Gestion_Service.models import Service, DemandeService
from utilisateurs.token import generate_confirmation_token, verify_confirmation_token

User = get_user_model()  # ✅ utilisation de mon model : User

#function pour la page d'accueil
def home(request):

    services = Service.objects.all()

    return render(request, 'index.html',{'services' : services})

###############################################################################

def client_dashbord(request):

# Vérifier si une demande est en attente dans la session
    if 'demandeservice_temp' in request.session:
        demandeservice_data = request.session.pop('demandeservice_temp')

        # Créer la demande de service dans la base de données
        service = Service.objects.get(id=int(demandeservice_data['service_id']))
        DemandeService.objects.create(
            description=demandeservice_data['description'],
            service=service,
            client=request.user,
            statut='EN_ATTENTE',
        )
        #messages.success(request, "Votre demande de service a été enregistrée avec succès !")
        return render(request, 'client_dashboard.html', {'show_modal': True})

    return render(request, "users/clients.html",{'show_modal': False})

#####################################################################################
#  function : Connexion
@csrf_protect
def logIn(request):

    #recuperation des donnees de l'utilisateur avec la methode post.
    if request.method == 'POST':
        username = request.POST['username']  # ✅ Correction
        password = request.POST['password']  # ✅ Correction

        user = authenticate(request, username=username, password=password)

        if user is not None: # s'il existe  alors
            login(request, user)
            # Vérifier si une demande de service est stockée en session
            demandeservice_temp = request.session.get('demandeservice_temp')
            if demandeservice_temp:
                try:
                    service = Service.objects.get(id=int(demandeservice_temp['service_id']))
                    # Créer la demande en base de données
                    DemandeService.objects.create(
                        description=demandeservice_temp['description'],
                        service=service,
                        client=user,
                        statut='EN_ATTENTE'
                    )
                    messages.success(request, "Votre demande a été enregistrée après connexion.")
                    del request.session['demandeservice_temp']  # Supprimer les données stockées
                except Service.DoesNotExist:
                    messages.error(request, "Le service associé à votre demande n'existe plus.")

            #return redirect("client_dashbord")
            return render(request,'users/clients.html')  # Redirection vers le tableau de bord des clients
        else:
            messages.error(request, 'Nom d’utilisateur ou mot de passe incorrect')
            return redirect('login')

    return render(request, 'login.html')


#####################################################################################
# function :Inscription
def register(request):

    # recuperation des donnees de l'utilisateur par la methode POST.
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        adresse= request.POST['adresse']
        entreprise = request.POST['entreprise']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        #verifiction de l'authentification des infos des users

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ce nom est déjà utilisé')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Cet email est déjà utilisé')
            return redirect('register')

        if password1 != password2:
            messages.error(request, 'Les deux mots de passe ne correspondent pas')
            return redirect('register')
        
         

# creation d'un utilisateur inactif ################################################

        utilisateur = User.objects.create_user(username=username, email=email,password=password2)

        utilisateur.adresse = adresse  # Assure-toi que tu as un champ `adresse` dans le modèle User ou une extension
        utilisateur.entreprise = entreprise

        utilisateur.is_active = False
        utilisateur.save()      

# envois de l'e-mail de bienvenue ########################################################

        send_mail(
        subject = 'bienvenu sur la plateforme  🎉🎉🎉🎉🎉',

        message ='Merci  ' + utilisateur.username + ',  de vous être inscrit !'+ '\n \n nous sommes heureux de vous comptez comme un de nos client ! \n \n'
        'Veuillez confirmer votre adresse e-mail pour activer votre compte',

        from_email = settings.EMAIL_HOST_USER,  # destinataire qui est email de l'administrateur.
        recipient_list = [utilisateur.email],
        fail_silently= False, #
        )

#Generer le lien de Confirmation ###############################################

        uidb64, token = generate_confirmation_token(utilisateur)
        #server_ip = "192.168.229.97"  # Remplace par l’IP de ton PC
        #activation_link = f"http://{server_ip}{reverse('activate', kwargs={'uidb64': uidb64, 'token': token})}"
        activation_link = request.build_absolute_uri(reverse('activate', kwargs={'uidb64': uidb64, 'token': token}))

        #Envois de l'e-mail de Confirmation ########################################################

        email_subject = 'Confirmed your e-mail 📩'
        email_body = render_to_string('confirmation_email.html',{'activate_link': activation_link})

        send_mail(
            subject=email_subject,
            message="Veuillez consulter l'email en HTML.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[utilisateur.email],
            fail_silently=False,
            html_message=email_body
              # ✅ permet d'envoyer email en html.
        )

        print(f"Email envoyé à {utilisateur.email}")

        messages.success(request,' Un e-mail de confirmation vous a été envoyé. Veuillez vérifier votre boîte de réception.')

        # Vérification s'il y a demande de service (avant la redirection)
        demandeservice = request.session.get('demandeservice')  # Renommé ici
        if demandeservice:
            # Traitement de la demande de service ici (exemple : enregistrer une demande)
            # Assurez-vous de bien avoir le modèle pour la demande de service
            DemandeService.objects.create(client=utilisateur, service=demandeservice['service'],
<<<<<<< HEAD
                                   description=demandeservice['description'])
=======
                                   description=demandeservice['description'], fichier=demandeservice['fichier'])
>>>>>>> a7a94a373523b68f79fb08a05a44dd64ee988bb5
            del request.session['demandeservice']  # Supprimer la demande après traitement

        return redirect('login')

    return render(request, 'register.html')




########################################################################################

# function : Déconnexion.
def logOut(request):
    logout(request)
    messages.success(request, 'Vous êtes déconnecté.')
    return redirect('home')

#############################################################################################
#Vue activation du compte

def activate_account(request, uidb64, token):
    # verifier la validiter du token.
    user= verify_confirmation_token(uidb64, token)

    if user is not None:
        # le token est valide, activer l'utilisateur.
        user.is_active =True
        user.save()
        messages.success(request,'Votre compte a été activé avec succès ! Vous pouvez maintenant vous connecter.')
        return redirect('login')
    else:
        messages.error(request,'Lien d\'activation invalide ou expiré.')
        return redirect('home')

#################################################################
# vue Django pour permettre la mise à jour automatique


#######################################################################

def apropos(request):
    # Ici, tu peux récupérer les informations spécifiques du client (comme entreprise).

        return render(request, 'home/apropos.html')

###################################################################################

def contact_view(request):
    print("Méthode reçue :", request.method)  # Debug

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")  # Correction ici

        print("Données reçues :", name, email, message)  # Debug


        if not name or not email or not message:
            messages.error(request, "Tous les champs sont obligatoires.")
            return render(request, "home/contact.html")  # Afficher la page avec les erreurs

        try:
            send_mail(
                subject=f"Message de {name} depuis le formulaire de contact",
                message=f"Nom: {name}\nEmail: {email}\nMessage: {message}",
                from_email=email,
                recipient_list=['edjabeadam1@gmail.com'],  # Mets ton email ici
                fail_silently=False,
            )
            messages.success(request, "Votre message a été envoyé avec succès !")
            return render(request, "home/contact.html", {"show_modal": True})  # Affichage de la modal


        except Exception as e:
            messages.error(request, "Erreur lors de l'envoi du message. Réessayez.")
            return render(request, "home/contact.html")

    return render(request, "home/contact.html")  # Charge la page avec le formulaire'''



