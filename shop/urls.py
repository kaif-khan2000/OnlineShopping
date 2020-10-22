
from django.urls import path
from . import views
from django.contrib import akyadmin
admin.site.site_title = "Protomix Admin"
admin.site.site_header = "Protomix Admin"
urlpatterns = [
    path("",views.index,name="index"),
    path("login",views.signIn,name="login"),
    path("logout",views.logoutHandler,name="logout"),
    path("signUp",views.signUp,name="signUp"),
    path("register",views.register,name="register"),
    path("searchRecommendations",views.searchRecommendations,name="searchRecommendations"),
    path("searchView",views.searchView,name="searchView"),
    path("productView/<slug>",views.productView,name="productView"),
    path("placeOrder",views.placeOrder,name="placeOrder"),
    path("orderPage",views.orderPage,name="orderPage"),
    path("cartPage",views.cartPage,name="cartPage"),
    path("addCart",views.addCart,name="addCart"),
    path("tracker/<slug>",views.tracker,name="tracker"),
]