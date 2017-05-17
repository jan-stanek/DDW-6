import csv
from scipy.spatial.distance import cosine
import numpy as np

def refRecommend(user, topCount, topUsers, wCB, wCF):
    movies = {}
    users = {}
    rated = {}
    ratings = {}
    movieToPos = {}

    with open('movies.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        i = -1
        for row in reader:
            if i == -1:
                i = 1
                continue

            id = int(row[0])
            genres = row[2].split('|')

            movies[id] = {
                'Adventure': 0,
                'Animation': 0,
                'Children': 0,
                'Comedy': 0,
                'Fantasy': 0
            }

            movies[id]['Adventure'] = 1 if 'Adventure' in genres else 0
            movies[id]['Animation'] = 1 if 'Animation' in genres else 0
            movies[id]['Children'] = 1 if 'Children' in genres else 0
            movies[id]['Comedy'] = 1 if 'Comedy' in genres else 0
            movies[id]['Fantasy'] = 1 if 'Fantasy' in genres else 0

            movieToPos[id] = i

            i += 1


    with open('ratings-test.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        i = 0
        for row in reader:
            if i == 0:
                i = 1
                continue

            userId = int(row[0])
            movieId = int(row[1])
            rating = float(row[2])

            if userId not in users:
                users[userId] = {
                    'Adventure': 0,
                    'Animation': 0,
                    'Children': 0,
                    'Comedy': 0,
                    'Fantasy': 0
                }

            if rating < 2.5:
                continue

            for genre in movies[movieId].keys():
                if movies[movieId][genre] > 0:
                    users[userId][genre] += 1

            if userId not in rated:
                rated[userId] = []

            rated[userId].append(movieId)

            if userId not in ratings:
                ratings[userId] = np.zeros((1, len(movies)))

            ratings[userId][0, movieToPos[movieId]] = rating

    # most similar movies
    relatedMovie = []
    relatedDistance = []

    userVector = np.matrix(list(users[user].values()))

    for movie in movies:
        movieVector = np.matrix(list(movies[movie].values()))
        distance = cosine(userVector, movieVector)
        relatedMovie.append(movie)
        relatedDistance.append(distance)

    sortedSimilarities = np.argsort(relatedDistance)

    topMovies1 = []
    topMovies1Distances = []

    for i in range(0, len(relatedMovie)):
        movieId = relatedMovie[sortedSimilarities[i]]
        if movieId not in rated[user]:
            topMovies1.append(movieId)
            topMovies1Distances.append(relatedDistance[sortedSimilarities[i]])
        if len(topMovies1) == topCount:
            break

    # most similar users movies
    relatedUser = []
    relatedUserDistance = []

    user1Vector = np.matrix(ratings[user])

    for u in users:
        user2Vector = np.matrix(ratings[u])
        distance = cosine(user1Vector, user2Vector)
        relatedUser.append(u)
        relatedUserDistance.append(distance)

    sortedUSimilarities = np.delete(np.argsort(relatedUserDistance), 0, 0)

    topMovies2Distances = []

    for m in sortedSimilarities[:topCount]:
        nn = 0
        sum = 0

        for r in range(0, topUsers):
            rat = ratings[relatedUser[sortedUSimilarities[r]]][0, m]
            if rat > 0:
                sum += rat
                nn += 1

        if nn == 0:
            ratio = 0
        else:
            ratio = sum / (nn * 5)

        topMovies2Distances.append(ratio)

    topMoviesSimilarities = []

    for i in range(0, topCount):
        topMoviesSimilarities.append(wCB * (1 - topMovies1Distances[i]) + wCF * topMovies2Distances[i])

    topMoviesSort = np.argsort(topMoviesSimilarities)[::-1]

    topMovies = []
    for i in topMoviesSort:
        topMovies.append(topMovies1[i])

    return topMovies


def testRecommend(user, topCount, topUsers, wCB, wCF):
    movies = {}
    users = {}
    rated = {}
    ratings = {}
    usersTest = {}
    ratedTest = {}
    ratingsTest = {}
    movieToPos = {}

    with open('movies.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        i = -1
        for row in reader:
            if i == -1:
                i = 1
                continue

            id = int(row[0])
            genres = row[2].split('|')

            movies[id] = {
                'Adventure': 0,
                'Animation': 0,
                'Children': 0,
                'Comedy': 0,
                'Fantasy': 0
            }

            movies[id]['Adventure'] = 1 if 'Adventure' in genres else 0
            movies[id]['Animation'] = 1 if 'Animation' in genres else 0
            movies[id]['Children'] = 1 if 'Children' in genres else 0
            movies[id]['Comedy'] = 1 if 'Comedy' in genres else 0
            movies[id]['Fantasy'] = 1 if 'Fantasy' in genres else 0

            movieToPos[id] = i

            i += 1

    with open('ratings-train.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        i = 0
        for row in reader:
            if i == 0:
                i = 1
                continue

            userId = int(row[0])
            movieId = int(row[1])
            rating = float(row[2])

            if userId not in users:
                users[userId] = {
                    'Adventure': 0,
                    'Animation': 0,
                    'Children': 0,
                    'Comedy': 0,
                    'Fantasy': 0
                }

            if rating < 2.5:
                continue

            for genre in movies[movieId].keys():
                if movies[movieId][genre] > 0:
                    users[userId][genre] += 1

            if userId not in rated:
                rated[userId] = []

            rated[userId].append(movieId)

            if userId not in ratings:
                ratings[userId] = np.zeros((1, len(movies)))

            ratings[userId][0, movieToPos[movieId]] = rating


    with open('ratings-test.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        i = 0
        for row in reader:
            if i == 0:
                i = 1
                continue

            userId = int(row[0])
            movieId = int(row[1])
            rating = float(row[2])

            if userId not in usersTest:
                usersTest[userId] = {
                    'Adventure': 0,
                    'Animation': 0,
                    'Children': 0,
                    'Comedy': 0,
                    'Fantasy': 0
                }

            if rating < 2.5:
                continue

            for genre in movies[movieId].keys():
                if movies[movieId][genre] > 0:
                    usersTest[userId][genre] += 1

            if userId not in ratedTest:
                ratedTest[userId] = []

            ratedTest[userId].append(movieId)

            if userId not in ratingsTest:
                ratingsTest[userId] = np.zeros((1, len(movies)))

            ratingsTest[userId][0, movieToPos[movieId]] = rating

    # most similar movies
    relatedMovie = []
    relatedDistance = []

    userVector = np.matrix(list(usersTest[user].values()))

    for movie in movies:
        movieVector = np.matrix(list(movies[movie].values()))
        distance = cosine(userVector, movieVector)
        relatedMovie.append(movie)
        relatedDistance.append(distance)

    sortedSimilarities = np.argsort(relatedDistance)

    topMovies1 = []
    topMovies1Distances = []

    for i in range(0, len(relatedMovie)):
        movieId = relatedMovie[sortedSimilarities[i]]
        if movieId not in rated[user]:
            topMovies1.append(movieId)
            topMovies1Distances.append(relatedDistance[sortedSimilarities[i]])
        if len(topMovies1) == topCount:
            break

    # most similar users movies
    relatedUser = []
    relatedUserDistance = []

    user1Vector = np.matrix(ratingsTest[user])

    for u in users:
        user2Vector = np.matrix(ratings[u])
        distance = cosine(user1Vector, user2Vector)
        relatedUser.append(u)
        relatedUserDistance.append(distance)

    sortedUSimilarities = np.delete(np.argsort(relatedUserDistance), 0, 0)

    topMovies2Distances = []

    for m in sortedSimilarities[:topCount]:
        nn = 0
        sum = 0

        for r in range(0, topUsers):
            rat = ratings[relatedUser[sortedUSimilarities[r]]][0, m]
            if rat > 0:
                sum += rat
                nn += 1

        if nn == 0:
            ratio = 0
        else:
            ratio = sum / (nn * 5)

        topMovies2Distances.append(ratio)

    topMoviesSimilarities = []

    for i in range(0, topCount):
        topMoviesSimilarities.append(wCB * (1 - topMovies1Distances[i]) + wCF * topMovies2Distances[i])

    topMoviesSort = np.argsort(topMoviesSimilarities)[::-1]

    topMovies = []
    for i in topMoviesSort:
        topMovies.append(topMovies1[i])

    return topMovies


ref = refRecommend(26, 100, 3, 0, 1)[:10]
test = testRecommend(26, 100, 3, 0, 1)[:10]
intersect = list(set(ref) & set(test))

prec = len(intersect) / len(test)
rec = len(intersect) / len(ref)

print('precision')
print(prec)
print('recall')
print(rec)
print('f-measure')
print((2*prec*rec) / (prec + rec))

print(ref)
print(test)
