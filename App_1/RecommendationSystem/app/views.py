from django.shortcuts import render
from django.http import HttpResponse
import pymysql
import numpy as np
# Create your views here

# def index(req):
#     return HttpResponse('<h1>Hello World</h1>')

def mysqlshit():
    conn = pymysql.connect(host='localhost',user='root',port=3307,db='movies_db',charset='latin1')
    cursor = conn.cursor()

    query = "select * from movies where m_cat like '%Action%'"
    cursor.execute(query)
    actionMovies = cursor.fetchall()

    query = "select * from movies where m_cat like '%Adventure%'"
    cursor.execute(query)
    adventureMovies = cursor.fetchall()

    query = "select * from movies where m_cat like '%Comedy%'"
    cursor.execute(query)
    comedyMovies = cursor.fetchall()

    query = "select * from movies where m_cat like '%Biography%'"
    cursor.execute(query)
    biopicMovies = cursor.fetchall()

    query = "select * from movies where m_cat like '%Horror%'"
    cursor.execute(query)
    horrorMovies = cursor.fetchall()

    query = 'select * from movies where watched=1'
    cursor.execute(query)
    watchedMovies = cursor.fetchall()

    query = 'select * from movies where watched=0'
    cursor.execute(query)
    unwatchedMovies = cursor.fetchall()

    watched_genres = []
    for item in watchedMovies:
        watched_genres.append(item[6].split(', '))
        
    watched_genre = []    
    for i in range(len(watched_genres)):
        for j in range(len(watched_genres[i])):
            watched_genre.append(watched_genres[i][j])

    watched_genre = list(set(watched_genre))

    movies_dict = {}
    for item in unwatchedMovies:
        movies_dict[item[0]]=item[6].split(', ')
    
    simi_dict = {}
    for item in movies_dict:
        numer = len(set(watched_genre).intersection(set(movies_dict[item])))
        denom = len(set(watched_genre).union(set(movies_dict[item])))
        simi_dict[item] = numer/denom



    recommended_ids = []

    # for item in simi_dict:
    #     if simi_dict[item] == 0:
    #         del simi_dict[item]
    
    ids = list(simi_dict.keys())
    scores = []
    for item in simi_dict:
        scores.append(simi_dict[item])
        
    indexes = list(np.argsort(scores))
    indexes.reverse()


    for i in indexes:
        recommended_ids.append(ids[i])
        
    if len(recommended_ids) >= 3:
        query = 'select * from movies where m_id in (%s,%s,%s)'
        cursor.execute(query,(recommended_ids[0],recommended_ids[1],recommended_ids[2]))
        recommendedMovies= cursor.fetchall()

    elif len(recommended_ids) == 2:
        query = 'select * from movies where m_id in (%s,%s)'
        cursor.execute(query,(recommended_ids[0],recommended_ids[1]))
        recommendedMovies= cursor.fetchall()

    elif len(recommended_ids) == 1:
        query = 'select * from movies where m_id in (%s)'
        cursor.execute(query,(recommended_ids[0]))
        recommendedMovies= cursor.fetchall()
        
    else:
        recommendedMovies=[]
        pass

    if watchedMovies == []:
        recommendedMovies=[]
        pass


    database = {
        'action': actionMovies,
        'comedy': comedyMovies,
        'adventure': adventureMovies,
        'horror': horrorMovies,
        'biopic': biopicMovies,
        'rec' : recommendedMovies
    }
    return database

def index(req):
    return render(req,'index.html',context={"data":mysqlshit()})

def watched(req,pk):
    conn = pymysql.connect(host='localhost',user='root',port=3307,db='movies_db',charset='latin1')
    cursor = conn.cursor()
    query = 'update movies set watched=1 where m_id=%s'
    cursor.execute(query,(pk))
    conn.commit()
    query = 'select * from movies where watched=1'
    cursor.execute(query)
    watchedMovies = cursor.fetchall()
    return render(req,'watched.html',context={'watched':watchedMovies})
