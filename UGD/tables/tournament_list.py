import django_tables2 as tables
from django_tables2.utils import A
from ..models import Tournament


class TournamentTable(tables.Table):
    date_begin = tables.DateColumn(
        verbose_name="Дата",
        format="d.m.Y",
        attrs={"td": {"class": "col-xs-auto"}}
    )
    name = tables.LinkColumn(
        verbose_name="Назва турніру",
        viewname='UGD:tournament_info',
        args=[A('pk')],
        attrs={"td": {"class": "col-lg-auto"}}
    )
    count_tournament_players = tables.Column(
        verbose_name="Гравців",
        attrs={"td": {"class": "col-xs-auto"}}
    )
    count_player_games = tables.Column(
        verbose_name="Партій",
        attrs={"td": {"class": "col-md-auto"}}
    )
    city = tables.Column(
        verbose_name="Місто",
        attrs={"td": {"class": "col-md-auto"}}
    )
    egd_code = tables.LinkColumn(
        verbose_name="EGD",
        viewname="UGD:egd_tournament_link",
        args=[A('egd_code')],
        attrs={"td": {"class": "col-md-auto"}}
    )

    class Meta:
        model = Tournament
        fields = (
            'date_begin',
            'name',
            'count_tournament_players',
            'count_player_games',
            'city',
            'egd_code'
        )
        attrs = {
            'id': 'tournament_list_table',
            'class': 'ugd_table'
        }
