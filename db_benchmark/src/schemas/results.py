
class ReadResults:

    user_movies = []
    last_user_movies = []
    popular = []
    last_watched = []

    def get_average(self):
        average = dict(
            user_movies=sum(self.user_movies) / len(self.user_movies),
            last_user_movies=sum(self.last_user_movies) / len(self.last_user_movies),
            popular=sum(self.popular) / len(self.popular),
            last_watched=sum(self.last_watched) / len(self.last_watched),
        )
        return average


def average(values) -> dict:
    result = {}
    for key in values[0]:
        row = []
        for val in values:
            row.append(val[key])
        result[key] = sum(row) / len(row)
    return result
