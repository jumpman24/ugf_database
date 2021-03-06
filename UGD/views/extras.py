from django.views.generic.base import TemplateView

from functions import rate_calc_func


class RatingCalculatorView(TemplateView):
    template_name = 'UGD/rating_calculator.html'
    http_method_names = ['get', 'post']

    def get_context_data(self, **kwargs):
        context = super(RatingCalculatorView, self).get_context_data(**kwargs)
        try:
            first_rating = float(self.request.GET['first_rating'])
            second_rating = float(self.request.GET['second_rating'])
            result = float(self.request.GET['result'])
            context['new_rating_1'] = round(rate_calc_func.new_rating(first_rating, second_rating, result), 2)
            context['new_rating_1a'] = round(rate_calc_func.new_rating(first_rating, second_rating, (1 - result)), 2)
            context['new_rating_2'] = round(rate_calc_func.new_rating(second_rating, first_rating, (1 - result)), 2)
            context['new_rating_2a'] = round(rate_calc_func.new_rating(second_rating, first_rating, result), 2)
            context['con_param_1'] = round(rate_calc_func.k_factor(first_rating), 2)
            context['con_param_2'] = round(rate_calc_func.k_factor(second_rating), 2)
            context['a_param_1'] = round(rate_calc_func.a_factor(first_rating), 2)
            context['a_param_2'] = round(rate_calc_func.a_factor(second_rating), 2)
            context['win_exp_1'] = round(rate_calc_func.winning_expectancy(first_rating, second_rating), 2)
            context['win_exp_2'] = round(rate_calc_func.winning_expectancy(second_rating, first_rating), 2)
        except KeyError:
            print(1)
        return context
