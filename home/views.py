from django.shortcuts import render, redirect
from .forms import UserAddForm,  UserUpdateForm, ClientForm, EmergencyContactForm, ComplaintForm, ComplaintStatusForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import admin_only, unauthenticated_user, allowed_users
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .models import Client, EmergencyContact, Complaint, EmergencyAlert
from django.core.mail import send_mail

# Create your views here.
@admin_only
def HomePage(request):
    return render(request, 'index.html', {})


@unauthenticated_user
def SignIn(request):
    if request.method == "POST":
        uname = request.POST['uname']
        password = request.POST["pswd"]
        user = authenticate(request,username= uname, password = password)
        if user is not None:
            login(request,user)
            return redirect('HomePage')
        else:
            messages.error(request,"Username or Password Incorrect")
            return redirect('SignIn')
    return render(request,"login.html")
 

@login_required(login_url="SignIn")
def AdminIndex(request):
    form = UserAddForm()
    alert = EmergencyAlert.objects.filter(dispose = False)
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            clint = Client(user=user)
            clint.save()

            messages.success(request,"User Registration Successful")
            return redirect("AdminIndex")
        else:
            messages.error(request,"Something went Wrong!!! Try To use password Includes (UPPERCASE, Numbers, Sepecial Characters and Minimum Legth 8  Characters) or User or email id Already Exists")
            return redirect("AdminIndex")
    context = {
        "form":form,
        "alert":alert
        
    }
    return render(request,"admin/index.html",context)


def staff_index(request):
    alert = EmergencyAlert.objects.filter(dispose = False)
    context = {
       
        "alert":alert
        
    }
    return render(request,"staff/index.html",context)


@unauthenticated_user
def SignUp(request):
    form = UserAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            clint = Client(user=user)
            clint.save()
            messages.success(request,"Registration Successful")
            return redirect("SignIn")
        else:
            messages.error(request,form.errors)
            return redirect("SignUp")
    
    context = {"form":form}
    return render(request,"register.html",context)


def SignOut(request):
    logout(request)
    return redirect("SignIn")



# users administartive funtion sfor admin 


def user_admin(request):
    form = UserAddForm()
   
    users  = User.objects.exclude(groups__isnull=False)
    if request.method == "POST":
        form = UserAddForm(request.POST)
      
        if form.is_valid() :
            user = form.save()
            user.set_password(user.password)
            user.save()
    
            messages.success(request,"User Registration Successful")
            return redirect("user_admin")
        else:
            messages.error(request,f"Something went Wrong!!! Try To use password Includes (UPPERCASE, Numbers, Special Characters and Minimum Legth 8  Characters) or User or email id Already Exists <br> {form.errors}")
            return redirect("user_admin")
    context = { "form":form,"users":users}   
    return render(request,"admin/users_admin.html",context)


def user_update(request,id):
    user = User.objects.get(id=id)
    try:
        client = Client.objects.get(user=user)
    except:
        client = Client.objects.create(user=user, phone="0000000000", address="address", location="location")
        client.save()
    form1 = UserUpdateForm(instance=user)
    form2 = ClientForm(instance=client)
    if request.method == "POST":
        form1 = UserUpdateForm(request.POST, instance=user)
        form2 = ClientForm(request.POST, instance=client)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.success(request,"user Updated Successfully")
            return redirect("user_admin")
        else:
            messages.error(request,"Something went Wrong!!!")
            return redirect("user_admin")
    context = {"form1":form1,"form2":form2, "client":user}
    return render(request,"admin/users_update.html",context)

def user_delete(request,id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request,"User Deleted Successfully")
    return redirect("user_admin")


def complaints_admin(request):
    registered_complaints = Complaint.objects.filter(judgment_status = False )
    completed_complaints = Complaint.objects.filter(judgment_status = True )

    context = {
        "registered_complaints":registered_complaints,
        "completed_complaints":completed_complaints
    }
    return render(request,"admin/complaints.html",context)


def view_complaint_admin(request,id):
    complaint = Complaint.objects.get(id = id)
    form = ComplaintStatusForm()
    if request.method == "POST":
        form = ComplaintStatusForm(request.POST, request.FILES)
        if form.is_valid() :
            data = form.save(commit=False)
            data.complaint =  complaint
            data.save()

            complaint.status = data.status
            complaint.save()
    
            messages.success(request,"Status update success")
            return redirect("view_complaint_admin", id = id)


    context = {
        "complaint":complaint,
        "form":form
    }
    return render(request,"admin/view_complaint.html",context)

def add_status(request,id):

    return redirect("view_complaint_admin", id = id)

def close_complaint_admin(request, id):
    com = Complaint.objects.get(id = id)
    com.status = "closed"
    com.judgment_status = True
    com.save()
    messages.success(request,"Status update success")
    return redirect("complaints_admin")



# staff administartive funtion sfor admin 


def staff_admin(request):
    form = UserAddForm()
    users  = User.objects.filter(groups__name='staff')
    if request.method == "POST":
        form = UserAddForm(request.POST)
      
        if form.is_valid() :
            user = form.save()
            user.set_password(user.password)
            user.save()

           
            group = Group.objects.get(name="staff")
            user.groups.add(group)
            user.save()
            clint = Client(user=user)
            clint.save()
    
            messages.success(request,"User Registration Successful")
            return redirect("staff_admin")
        else:
            messages.error(request,f"Something went Wrong!!! Try To use password Includes (UPPERCASE, Numbers, Special Characters and Minimum Legth 8  Characters) or User or email id Already Exists <br> {form.errors}")
            return redirect("staff_admin")
    context = { "form":form,"staff":users}   
    return render(request,"admin/staff_admin.html",context)


def staff_update(request,id):
    user = User.objects.get(id=id)
    try:
        client = Client.objects.get(user = user)
    except:
        client = Client.objects.create(user=user, phone="0000000000", address="address", location="location")
        client.save()
    form1 = UserUpdateForm(instance=user)
    form2 = ClientForm(instance=client)
    
    if request.method == "POST":
        form1 = UserUpdateForm(request.POST, instance=user)
        form2 = ClientForm(request.POST, instance=client)
       
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.success(request,"user Updated Successfully")
            return redirect("staff_admin")
        else:
            messages.error(request,f"Something went Wrong!!! {form1.errors} {form2.errors}")
            return redirect("staff_admin")
    context = {"form1":form1,"form2":form2, "client":user}
    return render(request,"admin/staff_update.html",context)

def staff_delete(request,id):
    user = User.objects.get(id=id)
    user.delete()
    messages.success(request,"User Deleted Successfully")
    return redirect("staff_admin")

def complaints_staff(request):
    registered_complaints = Complaint.objects.filter(judgment_status = False )
    completed_complaints = Complaint.objects.filter(judgment_status = True )

    context = {
        "registered_complaints":registered_complaints,
        "completed_complaints":completed_complaints
    }
    return render(request,"staff/complaints.html",context)


def view_complaint_staff(request,id):
    complaint = Complaint.objects.get(id = id)
    form = ComplaintStatusForm()
    if request.method == "POST":
        form = ComplaintStatusForm(request.POST, request.FILES)
        if form.is_valid() :
            data = form.save(commit=False)
            data.complaint =  complaint
            data.save()

            complaint.status = data.status
            complaint.save()
    
            messages.success(request,"Status update success")
            return redirect("view_complaint_staff", id = id)


    context = {
        "complaint":complaint,
        "form":form
    }
    return render(request,"staff/view_complaint.html",context)



# user functions 

@login_required(login_url="SignIn")
def profile(request):
    user = request.user
    try:
        client = Client.objects.get(user=user)
    except:
        client = Client.objects.create(user=user, phone="0000000000", address="address", location="location")
        client.save()
    try:
        em_contact = EmergencyContact.objects.get(client=user)
    except:
        em_contact = EmergencyContact.objects.create(client=user, name = " ", address=" ", phone=1,email = " ")
        em_contact.save()

    form1 = UserUpdateForm(instance= user)
    form2 = ClientForm( instance= client)
    form3 = EmergencyContactForm(instance= em_contact)

    if request.method == "POST":
        form2 = ClientForm(request.POST, request.FILES,  instance= client)
        form3 = EmergencyContactForm(request.POST,instance= em_contact)
        if form3.is_valid() and form2.is_valid():
            form3.save()
            form2.save()
            messages.success(request,"Data Updated Successfully")
            return redirect("profile")
        else:
            messages.error(request,f"Something went Wrong!!! {form1.errors} {form2.errors}")
            return redirect("profile")
        
    context = {
        "form1":form1,
        "form2":form2,
        "form3":form3,
    }
    return render(request,"profile.html",context)


def compliant_portal(request):
    registered_complaints = Complaint.objects.filter(user = request.user,judgment_status = False )
    completed_complaints = Complaint.objects.filter(user = request.user,judgment_status = True )
    form  = ComplaintForm()
    if request.method =="POST":
        form  = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            com = form.save(commit=False)
            com.user = request.user
            com.save()
            messages.success(request,"Compliant Registered")
            return redirect("compliant_portal")


    context = {
        "form":form,
        "registered_complaints":registered_complaints,
        "completed_complaints":completed_complaints
    }
    return render(request,"compliant_portal.html",context)


def complaint_details(request, pk):
    complaint = Complaint.objects.get(id = pk)
    context = {
        "complaint":complaint
    }
    return render(request,"complaint_details.html",context)


from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

@login_required(login_url="SignIn")
def sent_emergency_alert(request):
    alert = EmergencyAlert(user = request.user)
    alert.save()
    emc = EmergencyContact.objects.get(client = request.user)
    email = emc.email
    current_site = get_current_site(request)
    mail_subject = 'Emergency Alert'
    path = "SignUp"
    message = render_to_string('emailbody.html', {"message": f" alert form {request.user.first_name} contact number {request.user.client_user.phone}"})

    email = EmailMessage(mail_subject, message, to=[email])
    email.content_subtype = "html"
    email.send(fail_silently=True)
    return redirect(alartpage)
    

def alartpage(request):
    

    
    return render(request,"alert.html")


def diapose_alart_admin(request,pk):
    alert = EmergencyAlert.objects.get(id = pk)
    alert.dispose = True
    alert.save()
    return redirect("AdminIndex")

def view_details(request,pk):
    alert = EmergencyAlert.objects.get(id = pk)
    client = Client.objects.get(user = alert.user)
    context = {
       "client":client 
    }
    return render(request,"admin/view_alert.html",context)

def diapose_alart_staff(request,pk):
    alert = EmergencyAlert.objects.get(id = pk)
    alert.dispose = True
    alert.save()
    return redirect("staff_index")

def view_details_staff(request,pk):
    alert = EmergencyAlert.objects.get(id = pk)
    client = Client.objects.get(user = alert.user)
    context = {
       "client":client 
    }
    return render(request,"staff/view_alert.html",context)
    



