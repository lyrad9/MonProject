from django import views
from django.urls import path


<<<<<<< HEAD
from Gestion_Service.views import create_service_request, service_comptabilite, service_gl, devis_form, dashboard, refresh_dashboard, \
    generate_devis_pdf, voir_devis, telecharger_facture, facture_pdf_view, request_detail
=======
from Gestion_Service.views import service_comptabilite, service_gl, devis_form, dashboard, refresh_dashboard, \
    generate_devis_pdf, voir_devis, telecharger_facture, facture_pdf_view, voir_demandes_par_statut, modifier_demande, \
    supprimer_demande, voir_facture
>>>>>>> a7a94a373523b68f79fb08a05a44dd64ee988bb5

urlpatterns = [
    path('create_service_request/<int:service_id>/', create_service_request, name='create_service_request'),
    path('service_comptabilite/', service_comptabilite, name='service_comptabilite'),
    path('service_gl/', service_gl, name='service_gl'),

    path('devis_form/', devis_form, name='devis_form'),

    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/refresh/', refresh_dashboard, name='refresh_dashboard'),

    path('demandes/<str:statut>/', voir_demandes_par_statut, name='voir_demandes_par_statut'),
    path('demandes/modifier/<int:demande_id>/', modifier_demande, name='modifier_demande'),
    path('demandes/supprimer/<int:demande_id>/', supprimer_demande, name='supprimer_demande'),

    path('devis/generer/<int:demande_id>/', generate_devis_pdf, name='generate_devis_pdf'),
    path('devis/<str:statut>/', voir_devis, name='voir_devis'),

    path('facture/pdf/<int:facture_id>/', facture_pdf_view, name='facture_pdf'),
    path('facture/<str:statut>/', voir_facture, name='voir_facture'),
    path('facture/<int:facture_id>/download/', telecharger_facture, name='telecharger_facture'),
<<<<<<< HEAD
    path('service/<int:service_id>/create-request/', create_service_request, name='create_service_request'),
    path('request/<int:pk>/', request_detail, name='request_detail'),
    #path('demande/modifier/<int:demande_id>/', views.edit_demande_service, name='edit_demande_service'),
    #path('demande/valider/<int:demande_id>/', views.validate_demande_service, name='validate_demande_service'),
=======
>>>>>>> a7a94a373523b68f79fb08a05a44dd64ee988bb5


]
