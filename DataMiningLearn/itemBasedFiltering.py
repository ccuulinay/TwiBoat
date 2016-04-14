__author__ = 'ccuulinay'


from math import sqrt
from prettytable import PrettyTable


def computeAdjustCosineSimilarity(band1, band2, userRatings):
    average = {}
    for (key, ratings) in userRatings.items():
        average[key] = (float(sum(ratings.values()))) / len(ratings.values())

    num = 0 #numerator
    dem1 = 0 #first half of denominator
    dem2 = 0 # second half of denominator
    for (user ,ratings) in userRatings.items():
        if band1 in ratings and band2 in ratings:
            avg = average[user]
            num += (ratings[band1] - avg) * (ratings[band2] - avg)
            dem1 += (ratings[band1] - avg) ** 2
            dem2 += (ratings[band2] - avg) ** 2
    return num / (sqrt(dem1) * sqrt(dem2))


def computeUserAverage(userRatings):
    average = {}
    for (key, ratings) in userRatings.items():
        average[key] = (float(sum(ratings.values()))) / len(ratings.values())
    return average


def normalizeUserRatings(username, userRatings):
    max_rating = max(userRatings[username].values())
    min_rating = min(userRatings[username].values())

    result = {}
    for (key, ratings) in userRatings[username].items():
        result[key] = (float(2 * (ratings - min_rating) - (max_rating - min_rating))/(max_rating - min_rating))

    return result
