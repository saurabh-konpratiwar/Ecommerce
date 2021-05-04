from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path("about",views.about,name="About"),
    path("contact",views.contact,name="Contact"),
    path("tracker",views.tracker,name="Tracker"),
    path("search",views.search,name="Search"),
    path("products/<int:myid>",views.productview,name="ProductView"),
    path("showcatprod/<str:catname>",views.showcatprod,name="showcatprod"),
    path("checkout",views.checkout,name="checkout"),
    path("handlerequest",views.handlerequest,name='Handlerequest'),
    #path("login",views.handlelogin,name='handlelogin'),
    #path("logout",views.handlelogout,name="handlelogout"),
    #path("signup",views.handlesignup,name='handlesignup')
]