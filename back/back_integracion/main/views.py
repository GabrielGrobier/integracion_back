from django.shortcuts import render
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User

@csrf_exempt  # Permitir solicitudes desde el servidor frontend
def register_backend(request):
    if request.method == 'POST':
        try:
            # Decodificar el cuerpo de la solicitud
            data = json.loads(request.body)

            # Obtener los datos del usuario
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')

            # Validaciones básicas
            if not all([username, email, password, confirm_password]):
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            if password != confirm_password:
                return JsonResponse({'error': 'Passwords do not match.'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists.'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists.'}, status=400)

            # Crear el usuario
            User.objects.create_user(username=username, email=email, password=password)

            return JsonResponse({'message': 'User registered successfully.'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
