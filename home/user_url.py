from django.urls import path
from home import views

app_name = 'home'
urlpatterns = [
    path('', views.redirect_user, name='redirect_user'),
    path('<slug:uinfo>/', views.ViewUser, name='view_user'),
    path('<slug:uinfo>/editProfile/', views.editProfile, name='editProfile'),
    path('<slug:uinfo>/editProfile/edit/', views.edit, name='edit'),
    path('<slug:uinfo>/addProject/', views.addProject, name='addProject'),
    path('<slug:uinfo>/addProject/add/', views.add, name='add'),
    path('<slug:uinfo>/editHome/', views.editHome, name='editHome'),
    path('<slug:uinfo>/editHome/save/', views.saveHome, name='saveHome'),
    path('<slug:uinfo>/editFaq/', views.editFaq, name='editFaq'),
    path('<slug:uinfo>/editFaq/save/', views.saveFaq, name='saveFaq'),
    path('<slug:uinfo>/editContact/', views.editContact, name='editContact'),
    path('<slug:uinfo>/editContact/save/', views.saveContact, name='saveContact'),
    path('<slug:uinfo>/addNotice/', views.addNotice, name='addNotice'),
    path('<slug:uinfo>/addNotice/save/', views.saveNotice, name='saveNotice'),

]
