from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import models
import json


@csrf_exempt
def create_additive_card(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        additive_card = models.AdditiveBehavior.objects.create(**data)
        response = {
            'power': additive_card.power,
            'splash': additive_card.splash,
            'radius': additive_card.radius
        }
        return JsonResponse(response, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def create_multiplicative_card(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        multiplicative_card = models.MultiplicativeBehavior.objects.create(**data)
        response = {
            'power': multiplicative_card.power,
            'range': multiplicative_card.range,
            'rate': multiplicative_card.rate
        }
        return JsonResponse(response, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def verify_mint():
    # Ensure a tower is sufficiently dissimilar from any tower already present on the blockchain
    pass

def mint_tower():
    # Submit new tower to the blockchain
    pass

def delete_tower():
    # Remove tower from the blockchain
    pass
