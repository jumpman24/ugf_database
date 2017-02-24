"""
    Данный модуль предназначен для расчета рейтинга по методу В.Корсака.
    Методика отличается от системы EGD двумя моментами:
        1. В отличие от ЕГД вместо параметра е используется коэффциент развития при расчете нового рейтинга.
        2. Рейтинг каждого тура считается исходя из рейтинга полученного после расчета предыдущего тура.
    Более подробное описание здесь: http://forum.ufgo.org/viewtopic.php?f=3&t=1260
"""


from math import exp


def con(rate):
    res = 0
    if 100 <= rate < 200:
        res = 122 - rate * 0.06
    elif 200 <= rate < 1300:
        res = 120 - rate * 0.05
    elif 1300 <= rate < 2000:
        res = 107 - rate * 0.04
    elif 2000 <= rate < 2400:
        res = 87 - rate * 0.03
    elif 2400 <= rate < 2600:
        res = 63 - rate * 0.02
    elif 2600 <= rate < 2700:
        res = 37 - rate * 0.01
    elif rate >= 2700:
        res = 10
    return res


def a_param(rate):
    res = 0
    if 100 <= rate < 2700:
        res = 205 - rate / 20
    elif rate >= 2700:
        res = 70
    return res


def winning_expectancy(rate1, rate2):
    higher_rate, lower_rate = max(rate1, rate2), min(rate1, rate2)
    if higher_rate - lower_rate > 900:
        lower_rate -= 50
    lower_win_exp = 1 / (exp((higher_rate - lower_rate) / a_param(lower_rate)) + 1)
    higher_win_exp = 1 - lower_win_exp
    if rate1 <= rate2:
        return lower_win_exp
    else:
        return higher_win_exp


# РАССЧЕТ АНОМАЛЬНОГО РЕЗУЛЬТАТА
def abnormal_growth(self_rate, number_of_rounds):
    return number_of_rounds * con(self_rate) * (0.45 + (3100 - self_rate) / 50000)


def abnormal_rating(self_rate, number_of_rounds):
    return self_rate + abnormal_growth(self_rate, number_of_rounds)


# РАССЧЕТ НОВОГО РЕЙТИНГА
def growth(self_rate, opponent_rate, result):
    if result not in [0, 0.5, 1]:
        return 0
    else:
        return con(self_rate) * (result - winning_expectancy(self_rate, opponent_rate) + (3100 - self_rate) / 50000)


def new_rating(self_rate, opponent_rate, result=1):
    next_rating = self_rate + growth(self_rate, opponent_rate, result)
    if next_rating < 100:
        return 100
    else:
        return next_rating


# ПОДСЧЕТ КОЛИЧЕСТВА ТУРОВ
def count_rated_rounds(tournament_data):
    rated_rounds = dict()
    for player in tournament_data:
        rounds_count = 0
        for pairing in tournament_data[player]:
            if pairing[1] in [0, 0.5, 1]:
                rounds_count += 1
        rated_rounds[player] = rounds_count
    return rated_rounds


# РАССЧЕТ РЕЗУЛЬТАТОВ ТУРНИРА
def calculate_tournament_results(total_rounds, start_ratings, tournament_data):
    rated_rounds = count_rated_rounds(tournament_data)
    finish_ratings = dict(start_ratings)

    for current_round in range(total_rounds):
        for player in finish_ratings:
            opponent = tournament_data[player][current_round][0]
            self_rate = finish_ratings[player]
            opponent_rate = finish_ratings[opponent]
            result = tournament_data[player][current_round][1]

            if result not in [0, 0.5, 1]:
                continue

            next_rate = new_rating(self_rate, opponent_rate, result)
            finish_ratings[player] = next_rate

    abnormal_counter = 0
    for player in start_ratings:
        if finish_ratings[player] > abnormal_rating(start_ratings[player], rated_rounds[player]):
            abnormal_counter += 1
            start_ratings[player] = finish_ratings[player]
    if abnormal_counter:
        return calculate_tournament_results(total_rounds, start_ratings, tournament_data)
    else:
        return finish_ratings
