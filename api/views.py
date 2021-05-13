from django.shortcuts import render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd

import subprocess

def getRecommendations(cuisineType, diningType, priceRange, xCoord, yCoord):
    funcCall = f'''"recommend_restaurants("{cuisineType}", "{diningType}", {priceRange}, {xCoord}, {yCoord}, Recommendations)."'''
    results = subprocess.getoutput(f'echo {funcCall} | swipl -q -f RestaurantRecommender.pl')
    # print(results)
    # restaurants = results.split("[",1)[1].split("]",1)[0].replace('"','').split(", ")
    if results.find("Recommendations") == -1: return False
    restaurants = results[(results.find('[')+1):results.find(']')].replace('"','').split(', ')
    return restaurants


restaurants = pd.read_csv('api/static/api/clean_data.csv')

# Create your views here.

@method_decorator(csrf_exempt)
def recommendation_request(request):
	post = json.loads(request.body)
	print(f"post: {post}")
	# post = {'cuisine': 'Continental', 'restType': 'QuickBites', 'dollarSign': '$$$', 'location': '1.2324, -1.0554'}
	post['dollarSign'] = len(post['dollarSign'])
	post['x'] = float(post['location'].split(',')[0])
	post['y'] = float(post['location'].split(',')[1].strip())
	print(post)
	
	recommendations = getRecommendations(post['cuisine'],post['restType'],post['dollarSign'],post['x'],post['y'])
	print(recommendations)

	try:
		return JsonResponse(
			{
				'success':True,
				'restaurants':restaurants[restaurants['name'].isin(recommendations)].values.tolist()
			}
		)
	except Exception as e:
		return JsonResponse(
			{
				'success':False,
				'message':str(e)
			}
		)