from django.urls import path
from . import views

urlpatterns = [ 
    path('HomePage', views.HomePage, name='HomePage'),
    path("",views.SignIn,name="SignIn"),
    path("AdminIndex",views.AdminIndex,name="AdminIndex"),  
    path("staff_index",views.staff_index,name="staff_index"),  
    path("SignUp",views.SignUp,name="SignUp"),
    path("SignOut",views.SignOut,name="SignOut"),
    path("user_admin",views.user_admin,name="user_admin"),
    path("user_update/<int:id>",views.user_update,name="user_update"),
    path("user_delete/<int:id>",views.user_delete,name="user_delete"),

    path("staff_admin",views.staff_admin,name="staff_admin"),
    path("staff_update/<int:id>",views.staff_update,name="staff_update"),
    path("staff_delete/<int:id>",views.staff_delete,name="staff_delete"),
    path("complaints_admin",views.complaints_admin,name="complaints_admin"),
    path("view_complaint_admin/<int:id>",views.view_complaint_admin,name="view_complaint_admin"),
    path("add_status/<int:id>",views.add_status,name="add_status"),
    path("close_complaint_admin/<int:id>",views.close_complaint_admin,name="close_complaint_admin"),
    path("diapose_alart_admin/<int:pk>",views.diapose_alart_admin,name="diapose_alart_admin"),
    path("view_details/<int:pk>",views.view_details,name="view_details"),

    path("diapose_alart_staff/<int:pk>",views.diapose_alart_staff,name="diapose_alart_staff"),
    path("view_details_staff/<int:pk>",views.view_details_staff,name="view_details_staff"),

    

    path("complaints_staff",views.complaints_staff,name="complaints_staff"),
    path("view_complaint_staff/<int:id>",views.view_complaint_staff,name="view_complaint_staff"),


    path("profile",views.profile,name="profile"),
    path("compliant_portal",views.compliant_portal,name="compliant_portal"),
    path("complaint_details/<int:pk>",views.complaint_details,name="complaint_details"),
    

    path("sent_emergency_alert",views.sent_emergency_alert,name="sent_emergency_alert"),
    path("alartpage",views.alartpage,name="alartpage"),

    
   
]