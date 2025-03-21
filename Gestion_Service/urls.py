
from django.urls import path


from Gestion_Service.views import service_comptabilite, service_gl, devis_form, dashboard, refresh_dashboard, \
    generate_devis_pdf, voir_devis, telecharger_facture, facture_pdf_view

urlpatterns = [

    path('service_comptabilite/', service_comptabilite, name='service_comptabilite'),
    path('service_gl/', service_gl, name='service_gl'),
    path('devis_form/', devis_form, name='devis_form'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/refresh/', refresh_dashboard, name='refresh_dashboard'),
    path('devis/generer/<int:demande_id>/', generate_devis_pdf, name='generate_devis_pdf'),
    path('devis/<str:statut>/', voir_devis, name='voir_devis'),
    path('facture/pdf/<int:facture_id>/', facture_pdf_view, name='facture_pdf'),
    path('facture/<int:facture_id>/download/', telecharger_facture, name='telecharger_facture'),
    #path('demande/modifier/<int:demande_id>/', views.edit_demande_service, name='edit_demande_service'),
    #path('demande/valider/<int:demande_id>/', views.validate_demande_service, name='validate_demande_service'),


]
