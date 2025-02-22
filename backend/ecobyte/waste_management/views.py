from django.shortcuts import render

# Create your views here.
import tensorflow.lite as tflite
import numpy as np
from PIL import Image
import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import WasteItem



MODEL_PATH = os.path.join(settings.BASE_DIR, 'waste_management', 'model', 'waste_classifier.tflite')

def load_tflite_model():
    if not os.path.exists(MODEL_PATH):
        raise ValueError(f"Model file not found at {MODEL_PATH}")
    
    interpreter = tflite.Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    return interpreter

# Initialize the model
interpreter = load_tflite_model()
input_tensor_index = interpreter.get_input_details()[0]['index']
output_tensor_index = interpreter.get_output_details()[0]['index']

@api_view(['POST'])
def classify_waste(request):
    if 'image' not in request.FILES:
        return Response({'error': 'No image uploaded'}, status=400)

    image = request.FILES['image']
    image = Image.open(image).convert('RGB').resize((224, 224))
    input_data = np.array(image, dtype=np.float32) / 255.0
    input_data = np.expand_dims(input_data, axis=0)

    interpreter.set_tensor(input_tensor_index, input_data)
    interpreter.invoke()
    result = interpreter.get_tensor(output_tensor_index)

    predicted_class = np.argmax(result)
    class_labels = ['Plastic', 'Paper', 'Metal', 'Organic', 'E-Waste']
    waste_type = class_labels[predicted_class]
    confidence = float(np.max(result))
    
    waste_item = WasteItem.objects.create(
        user=request.user,
        image=image,
        waste_type=waste_type,
        confidence=confidence
    )
    
    return Response({'waste_type': waste_type, 'confidence': confidence})










from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.decorators import api_view

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token, created = Token.objects.get_or_create(user=response.data['user'])
        return Response({'token': token.key})

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if User.objects.filter(username=username).exists():
        return Response({'error': 'User already exists'}, status=400)
    user = User.objects.create_user(username=username, password=password)
    token = Token.objects.create(user=user)
    return Response({'token': token.key})
