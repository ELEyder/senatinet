from django.shortcuts import render, redirect
from userapp.models import DefaultUser
from postapp.models import Post
from .decorators import firebase_login_required
from firebase_admin import auth
from django.http import HttpResponse
import os
import pyrebase
from dotenv import load_dotenv

load_dotenv()

firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID")
}

firebase = pyrebase.initialize_app(firebase_config)
authentication = firebase.auth()

def set_user_status(user_id, status):
    """Actualiza el estado del usuario si existe user_id."""
    if user_id:
        DefaultUser.updateStatus(user_id, status)

def get_logged_in_user(request):
    """Obtiene el usuario logueado basado en la sesión."""
    user_id = request.session.get('user_id')
    return DefaultUser.getUserById(user_id) if user_id else None

@firebase_login_required
def index(request):
    user_login = get_logged_in_user(request)
    if not user_login:
        return redirect('login')
    
    set_user_status(user_login['id'], 'Online')
    posts = Post.getPosts()
    users = DefaultUser.getUsersById(user_login['id'])

    for post in posts:
        post['likeStatus'] = 'active' if user_login['id'] in post.get('likesD', []) else 'inactive'
        post['comments'] = Post.getComments(post['id'])

    for user_g in users:
        user_id = user_login['id']
        user_g['fStatus'] = (
            'Cancel' if user_id in user_g.get('friendRequestR', [])
            else 'Accept' if user_id in user_g.get('friendRequestS', [])
            else 'View' if user_id in user_g.get('friends', [])
            else 'Send'
        )
        
    return render(request, "home/index.html", {'users':users, 'userLogin':user_login, 'posts':posts})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        try:
            user = authentication.sign_in_with_email_and_password(email, password)
            set_user_status(user['localId'], "Online")
            request.session['user_id'] = user['localId']
            return redirect('home')
        except Exception as e:
            return HttpResponse(f"Credenciales incorrectas: {str(e)}")

    return render(request, 'user/login.html')


def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        username = request.POST.get('username', '')
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')

        if password1 != password2:
            return HttpResponse("⚠️ Contraseñas diferentes. Por favor, inténtalo de nuevo.")

        if any(user['username'] == username for user in DefaultUser.getUsers()):
            return HttpResponse("⚠️ El usuario ya existe.")

        try:
            user = auth.create_user(email=email, password=password1)
            DefaultUser.addUser(
                id=user.uid,
                userName=username,
                firstName=firstname,
                lastName=lastname,
                email=email,
            )
            Post.addPost(user.uid, "se ha unido a Senatinet", '')
            return HttpResponse("Usuario creado exitosamente.")
        except Exception as e:
            return HttpResponse(f"Error al crear usuario: {str(e)}")

    return redirect('login')

def exit(request):
    set_user_status(request.session.get('user_id'), "Disconected")
    request.session.flush()
    return redirect('login')