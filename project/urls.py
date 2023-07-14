from django.contrib import admin
from django.urls import path, include
from tickets import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
router = DefaultRouter()
router.register('guests', views.viewsets_guest)
router.register('movies', views.viewsets_movie)
router.register('reservations', views.viewsets_reservation)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Functin based views
    path('rest/FBV/', views.FBV_listCreate, ),
    path('rest/FBV/<int:pk>/', views.FBV_PK, ),
    # Class based views
    path('rest/CBV/', views.CBV_ListCreate.as_view(), ),
    path('rest/CBV/<int:pk>/', views.CBV_PK.as_view(), ),
    # Mixins views
    path('rest/mixins/', views.Mixins_ListPost.as_view(), ),
    path('rest/mixins/<int:pk>/', views.Mixins_RetrieveUpdateDestroy.as_view(), ),
    # generics views
    path('rest/generics/', views.generics_ListPost.as_view(), ),
    path('rest/generics/<int:pk>/', views.generics_RetrieveUpdateDestroy.as_view(), ),
    path('rest/viewsets/', include(router.urls), ),
    path('fbv/find-movie/', views.movie_search, ),
    path('fbv/new-reservation/', views.new_reservation, ),
    # rest auth url
    path('api-auth', include('rest_framework.urls')),
    path('api-token-auth', obtain_auth_token),
    # post views
    path('rest/posts/<int:pk>', views.Post_pk.as_view()),
    
]
