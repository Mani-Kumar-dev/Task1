from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Request_user
from django.contrib.auth import authenticate,login,logout

#sending email
from django.conf import settings
from django.core.mail import send_mail
from django.core import mail
from django.core.mail.message import EmailMessage

# Create your views here.



def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        
        if password != cpassword:
            messages.error(request, "Passwords do not match")
            return redirect('/signup')
        
        try:
            user = User.objects.get(username=username)
            messages.error(request, "Username already taken")
            return redirect('/signup')
        except User.DoesNotExist:
            pass
        
        try:
            user = User.objects.get(email=email)
            messages.error(request, "Email already taken")
            return redirect('/signup')
        except User.DoesNotExist:
            pass
        
        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.save()
        
        messages.success(request, "User created successfully. Please log in.")
        return redirect('/login')
    
    return render(request, "signup.html")

def admin_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        
        if password != cpassword:
            messages.error(request, "Passwords do not match")
            return redirect('/signIn')
        
        try:
            user = User.objects.get(username=username)
            messages.error(request, "Username already taken")
            return redirect('/signIn')
        except User.DoesNotExist:
            pass
        
        try:
            user = User.objects.get(email=email)
            messages.error(request, "Email already taken")
            return redirect('/signIn')
        except User.DoesNotExist:
            pass
        
        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.is_staff = True
        myuser.is_superuser =True
        myuser.save()
        
        messages.success(request, "User created successfully. Please log in.")
        return redirect('/login')
    
    return render(request, "admin_reg.html")


def handlelogin(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password = request.POST.get('password')
        myuser=authenticate(username=username,password=password)
        if myuser is not None:
            login(request,myuser)
            if  myuser.is_superuser == True:
                AllPosts= Request_user.objects.all()
                context={"AllPosts": AllPosts}
                return render(request,"admin.html",context)
            else:
                return render(request,"user.html")
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('/login')
            
        
    return render(request,"login.html")

def addreq(request):
    if request.method == "POST":
        current_user=request.user
        request_type=request.POST.get("request_type")
        reason=request.POST.get("reason")
        query=Request_user(user_Id=current_user,requesttype=request_type,reason=reason,status="pending")
        query.save()
    return render(request,"user.html")

def accept_request(request, request_id):
    if request.user.is_authenticated:
        try:
            request_user = Request_user.objects.get(id=request_id)
        except Request_user.DoesNotExist:
            messages.error(request, "Leave request not found.")
            return redirect("/handleleaves/")
        request_user.status = 'Accepted'
        request_user.save()
        
        # Send emails
        from_email = settings.EMAIL_HOST_USER
        connection = mail.get_connection()
        connection.open()
        email_admin = mail.EmailMessage(
            ' Request Accepted',
            f'The  request has been Approved.',
            from_email,
            [request_user.user_Id.email],
            connection=connection
        )
        connection.send_messages([email_admin])
        connection.close()

        AllPosts= Request_user.objects.all()
        context={"AllPosts": AllPosts}
        return render(request,"admin.html",context)
    else:
       
        return render(request, "login.html")
    
def reject_request(request, request_id):
    if request.user.is_authenticated:
        try:
            request_user = Request_user.objects.get(id=request_id)
        except Request_user.DoesNotExist:
            messages.error(request, "Leave request not found.")
            return redirect("/handleleaves/")
        request_user.status = 'Rejected'
        request_user.save()
        
        # Send emails
        from_email = settings.EMAIL_HOST_USER
        connection = mail.get_connection()
        connection.open()
        email_admin = mail.EmailMessage(
            ' Request Accepted',
            f'The request from has been Rejected.',
            from_email,
            [request_user.user_Id.email],
            connection=connection
        )
        connection.send_messages([email_admin])
        connection.close()
        AllPosts= Request_user.objects.all()
        context={"AllPosts": AllPosts}
        return render(request,"admin.html",context)
    else:
       
        return render(request, "login.html")
    
    