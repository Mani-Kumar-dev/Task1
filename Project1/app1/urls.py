from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
   path("signup/",views.signup,name="signup"),
   path("admin_signup/",views.admin_signup,name="admin_signup"),
   path("handlelogin/",views.handlelogin,name="handlelogin"),
   path("addreq/",views.addreq,name="addreq"),
   path("accept_request/<slug:request_id>/",views.accept_request,name="accept_request"),
   path("reject_request/<slug:request_id>/",views.reject_request,name="reject_request"),
   
   
   
   
   
]