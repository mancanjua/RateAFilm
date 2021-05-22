from django.shortcuts import render
from django.shortcuts import redirect
from py2neo import Graph
from films.models import Film


def recommend(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/login', request.path))

    user_id = request.user.id
    graph = Graph(password='film')
    films = graph.run('MATCH (u1:User {id:' + str(user_id) + """})-[r:RATES]->(f:Film)
                       WITH u1, avg(r.rating) AS u1_mean
                    
                       MATCH (u1)-[r1:RATES]->(f:Film)<-[r2:RATES]-(u2)
                       WITH u1, u1_mean, u2, COLLECT({r1: r1, r2: r2}) AS ratings WHERE size(ratings) > 10
                     
                       MATCH (u2)-[r:RATES]->(m:Film)
                       WITH u1, u1_mean, u2, avg(r.rating) AS u2_mean, ratings
                    
                       UNWIND ratings AS r
                    
                       WITH sum((r.r1.rating - u1_mean) * (r.r2.rating - u2_mean)) AS nom,
                            sqrt(sum((r.r1.rating - u1_mean)^2) * sum((r.r2.rating - u2_mean)^2)) AS denom,
                            u1, u2 WHERE denom <> 0
                    
                       WITH u1, u2, nom/denom AS pearson
                       ORDER BY pearson DESC LIMIT 10
                    
                       MATCH (u2)-[r:RATES]->(m:Film) WHERE NOT EXISTS((u1)-[:RATES]->(m))
                    
                       RETURN m.id, SUM(pearson * r.rating) AS score
                       ORDER BY score DESC LIMIT 25""")

    recommendations = []

    while films.forward():
        recommendations.append(films.current['m.id'])

    films = [(i, Film.objects.get(id=i)) for i in recommendations]

    return render(request, 'recommendations.html', {'films': films})

