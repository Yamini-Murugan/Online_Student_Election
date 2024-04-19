from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile,Position,Candidate
from django.shortcuts import get_object_or_404
from django.db.models import F



def home(request):
     positions = Position.objects.all()
     return render (request, 'home.html',{'positions': positions})
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        phonenumber = request.POST['phoneno']
        regtype = request.POST['regtype']
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')
        
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname 
        myuser.save()
        
        
        profile = UserProfile.objects.create(user=myuser, regtype=regtype)

        messages.success(request, "You have Successfully Signed up")
        return redirect("login")
    
    return render(request, "signup.html")
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, "login.html")
def logoutpage(request):       
    logout(request)
    return redirect('home')

def add_position(request):
    if request.method == 'POST':
        position_name = request.POST.get('position_name')
        position = Position.objects.create(name=position_name)
        candidates = request.POST.get('candidate_names').split(',')
        for i, name in enumerate(candidates):
            Candidate.objects.create(position=position, name=name.strip(), votes=0)
    return render (request, 'adminadd.html')

def update_position(request, pk):
    position = get_object_or_404(Position, pk=pk)
    
    if request.method == 'POST':
        position_name = request.POST.get('position_name')
        if position_name:
            position.name = position_name
            position.save()
        
        candidate_names = request.POST.get('candidate_names')
        if candidate_names:
            candidate_names_list = candidate_names.split(',')
            
            position.candidates.all().delete()
            for name in candidate_names_list:
                Candidate.objects.create(position=position, name=name.strip(), votes=0)
        return redirect('home')
    
    return render(request, 'updateposition.html', {'position': position})

def delete_position(request, pk):
    position = get_object_or_404(Position, pk=pk)
    
    if request.method == 'POST':
        position.delete()
        return redirect('home')
    

    return render(request, 'confirm_delete_position.html', {'position': position})
def submit_vote(request):
    if request.method == 'POST':
        position_id = request.POST.get('position_id')
        selected_candidates = request.POST.getlist('candidates')
        
        Candidate.objects.filter(id__in=selected_candidates).update(votes=F('votes') + 1)
    return redirect('home') 
def vote(request, position_id):
    candidates = Candidate.objects.filter(position_id=position_id)
    return render(request, 'vote.html', {'candidates': candidates})