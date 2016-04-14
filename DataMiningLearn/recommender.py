__author__ = 'ccuulinay'

from math import sqrt

users2 = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
          "Ben": {"Taylor Swift": 5, "PSY": 2},
          "Clara": {"PSY": 3.5, "Whitney Houston": 4},
          "Daisy": {"Taylor Swift": 5, "Whitney Houston": 3}}

class recommender:

    def __init__(self, data, k=1, metric='pearson', n=5):
        self.k = k
        self.n = n
        self.metric = metric
        if self.metric == 'pearson':
            self.fn = self.pearson

        self.frequencies = {}
        self.deviations = {}


        if type(data).__name__ == 'dict':
            self.data = data


    def userRatings(self, username, n):
        ratings = self.data[username]
        ratings = list(ratings.items())
        ratings = ratings[:n]



    def manhattan(self, rating1, rating2):
        distance = 0
        commonRatings = False
        for key in rating1:
            if key in rating2:
                distance += abs(rating1[key] - rating2[key])
                commonRatings = True
        if commonRatings:
            return distance
        else:
            return -1


    def computeNearestNeighbor(self, username):
        distances = []
        for instance in self.data:
            if instance != username:
                distance = self.fn(self.data[username], self.data[instance])
                distances.append((instance, distance))
        distances.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        return distances


    def recommend(self, user):
        recommendations = {}

        nearest = self.computeNearestNeighbor(user)
        userRatings = self.data[user]
        totalDistance = 0.0
        for i in range(self.k):
            totalDistance += nearest[i][1]

        for i in range(self.k):
            weight = nearest[i][1]/totalDistance
            name = nearest[i][0]
            neighborRatings = self.data[name]
            for artist in neighborRatings:
                if not artist in userRatings:
                    if artist not in recommendations:
                        recommendations[artist] = (neighborRatings[artist] * weight)
                    else:
                        recommendations[artist] = (recommendations[artist] + neighborRatings[artist]*weight)

        recommendations = list(recommendations.items())
        recommendations.sort(key=lambda artistTuple: artistTuple[1], reverse=True)
        return recommendations[:self.n]



    def minkowski(rating1, rating2, r):
        distance = 0
        commonRatings = False
        for key in rating1:
            if key in rating2:
                distance += pow(abs(rating1[key] - rating2[key]), r)
                commonRatings = True
        if commonRatings:
            return pow(distance, 1/r)
        else:
            return 0


    def pearson(self, rating1, rating2):
        sum_xy=0
        sum_x=0
        sum_y=0
        sum_x_pow=0
        sum_y_pow=0
        n=0
        for key in rating1:
            if key in rating2:
                n += 1
                sum_xy += rating1[key]*rating2[key]
                sum_x += rating1[key]
                sum_y += rating2[key]
                sum_x_pow += rating1[key]**2
                sum_y_pow += rating2[key]**2

        numerator = sum_xy - (sum_x * sum_y)/n
        denominator = sqrt(sum_x_pow - (sum_x ** 2)/n) * sqrt(sum_y_pow - (sum_y ** 2)/n)

        if n == 0 or denominator == 0:
            return 0

        return numerator/denominator


    def cosineSimilarity(rating1, rating2):
        sum_xy = 0
        sum_x_pow = 0
        sum_y_pow = 0
        for key in rating1:
            if key in rating2:
                sum_xy += rating1[key] * rating2[key]  #Dot product
                sum_x_pow += rating1[key]**2
                sum_y_pow += rating2[key]**2
        numerator = sum_xy
        denominator = sqrt(sum_x_pow) * sqrt(sum_y_pow)
        return numerator/denominator


    def computeDeviations(self):
        # for each persion in the data:
        # get their ratings
        for ratings in self.data.values():
            # for each item and rating in that set of ratings:
            for (item, rating) in ratings.items():
                self.frequencies.setdefault(item, {})
                self.deviations.setdefault(item, {})
                # for each item2 & rating2 in that set of ratings:
                for (item2, rating2) in ratings.items():
                    if item != item2:
                        # add the difference between the ratings to our computation
                        self.frequencies[item].setdefault(item2, 0)
                        self.deviations[item].setdefault(item2, 0)

                        # find the card(), number of elements are is data set with item2 rated.
                        self.frequencies[item][item2] += 1
                        self.deviations[item][item2] += rating - rating2

        for (item, ratings) in self.deviations.items():
            for item2 in ratings:
                ratings[item2] /= self.frequencies[item][item2]


    def slopeOneRecommendations(self, oneUserRatings):
        recommendations = {}
        frequencies = {}
        # for every item and rating in the user's recommendations
        for (userItem, userRating) in oneUserRatings.items():

            # for every item in our dataset that the user didn't rate
            for (diffItem, diffRatings) in self.deviations.items():
                if diffItem not in oneUserRatings and userItem in self.deviations[diffItem]:
                    freq = self.frequencies[diffItem][userItem]
                    recommendations.setdefault(diffItem, 0.0)
                    frequencies.setdefault(diffItem, 0)
                    # add to the running sum representing the numerator
                    # of the formula
                    recommendations[diffItem] += (diffRatings[userItem] + userRating) * freq
                    # keep a running sum of the frequency of diffItem
                    frequencies[diffItem] += freq
        #recommendations =  [(self.convertProductID2name(k),v / frequencies[k]) for (k, v) in recommendations.items()]
        recommendations = [(k, v / frequencies[k]) for (k,v) in recommendations.items()]
        # finally sort and return
        sorted(recommendations, key=lambda artistTuple: artistTuple[1], reverse = True)
        # I am only going to return the first 50 recommendations
        return recommendations



r = recommender(users2)
r.computeDeviations()
print r.deviations
print r.frequencies

print

g = users2['Ben']
print r.slopeOneRecommendations(g)

