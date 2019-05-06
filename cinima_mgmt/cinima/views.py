from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from pymongo import MongoClient

client=MongoClient()from django.shortcuts import render
db=client['cinima']
collection=db['students']

#postman
@api_view(['POST'])
def api_add_base(request):
    # print("*****************************************************")
    # print(request)
    # c = json.dumps(request.data)
    # print("*****************************************************")
    # print(request.data['genre'])
    req = request.data
    # print(req1)

    # data=collection.insert(c)
    
    data=collection.insert({"99popularity" : req["99popularity"] ,
    "director" : req["director"],
	"genre" : req["genre"],
	"imdb_score" : req["imdb_score"],
	"name" : req["name"]}
    
    )

    return JsonResponse({"msg":"data posted successfully"},safe=False)


#Find Least watched movie by its imdb score.
@api_view(['GET'])
def api_least_movie(request):    
    #cursor=collection.aggregate([{"$group":{"_id":"$director","count":{"$sum":1}}},{"$sort":{"count":-1}},{"$limit":4}])
    # cursor=collection.aggregate([{"$group":{"_id":"$genre","count":{"$sum":1}}},{"$sort":{"count":-1}},{"$limit":4}])
    # cursor=collection.find().sort("_id",-1).limit(1)
    # cursor=collection.find({},{"name":1,"imdb_score":1}).sort("imdb_score",1).limit(1)
    cursor = collection.aggregate([{"$group":{"_id":"$name","min":{"$min":"$imdb_score"}}},{"$sort":{"min":1}},{"$limit":10}])
    data = []
    for doc in cursor:
        doc.pop("_id")
        data.append(doc)
    return JsonResponse(data,safe=False)



#Director with maximum number of movies 
@api_view(['GET'])
def api_max_movie(request):   
    cursor=collection.aggregate([{"$group":{"_id":"$director","count":{"$sum":1}}},{"$sort":{"count":-1}},{"$limit":4}])
    data = []
    for doc in cursor:
        doc.pop("_id")
        data.append(doc)
    return JsonResponse(data,safe=False)

#List out top ten movies according to imdb score.
@api_view(['GET'])
def api_top_ten(request):
     cursor = collection.find({},{"name":1,"imdb_score":1,"_id":0}).sort("imdb_score",-1).limit(10)
     data=list(cursor)
     return JsonResponse(data, safe = False)
