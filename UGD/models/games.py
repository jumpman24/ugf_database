from django.db import models
from . import Player, Tournament, Rank
from decimal import Decimal


class TournamentPlayer(models.Model):

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        verbose_name="гравець"
    )
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        verbose_name="турнір"
    )
    rank = models.ForeignKey(
        Rank,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="ранг"
    )
    place = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="місце"
    )
    rating_start = models.DecimalField(
        null=True,
        blank=True,
        max_digits=8,
        decimal_places=4,
        verbose_name="R1"
    )
    rating_finish = models.DecimalField(
        null=True,
        blank=True,
        max_digits=8,
        decimal_places=4,
        verbose_name="R2"
    )

    class Meta:
        verbose_name = "учасник турніру"
        verbose_name_plural = "учасники турніру"

    def __str__(self):
        if self.player.first_name and self.player.last_name:
            full_name = self.player.first_name+' '+self.player.last_name
        elif self.player.egd_first_name and self.player.egd_last_name:
            full_name = self.player.egd_first_name+' '+self.player.egd_last_name
        else:
            full_name = self.player.id
        if self.tournament.name:
            tournament_name = self.tournament.name
        elif self.tournament.egd_name:
            tournament_name = self.tournament.egd_name
        else:
            tournament_name = self.tournament.id
        return tournament_name+' @ '+str(full_name)

    def get_rating_delta(self):
        if self.rating_start and self.rating_finish:
            return Decimal(self.rating_finish - self.rating_start).normalize()
        else:
            return ""

    def get_rating_start(self):
        if self.rating_start:
            return Decimal(self.rating_start).normalize()
        else:
            return ""

    def get_rating_finish(self):
        if self.rating_finish:
            return Decimal(self.rating_finish).normalize()
        else:
            return ""

    def get_games_count(self):
        return self.pairing_player.filter(
            tournament_player_opponent__isnull=False  # Отсеиваем партии без соперника
        ).count()

    def get_wins_count(self):
        return self.pairing_player.filter(
            game_result=True
        ).count()

    def get_result(self):
        return "%d/%d" % (self.get_wins_count(), self.get_games_count())


class Pairing(models.Model):
    tournament_player = models.ForeignKey(
        TournamentPlayer,
        on_delete=models.CASCADE,
        verbose_name="гравець",
        related_name="pairing_player"
    )
    tournament_player_opponent = models.ForeignKey(
        TournamentPlayer,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
        verbose_name="суперник",
        related_name="pairing_opponent"
    )
    tournament_round = models.PositiveIntegerField(
        verbose_name="раунд"
    )
    color = models.NullBooleanField(
        default=None,
        choices=(
            (None, 'Невідомо'),
            (False, 'Чорні'),
            (True, 'Білі')
        ),
        verbose_name="колір"
    )
    handicap = models.PositiveIntegerField(
        default=0,
        choices=(
            (0, 'Без фори'),
            (1, 'Комі 0.5 очок'),
            (2, '2 камня'),
            (3, '3 камня'),
            (4, '4 камня'),
            (5, '5 каменів'),
            (6, '6 каменів'),
            (7, '7 каменів'),
            (8, '8 каменів'),
            (9, '9 каменів'),
        ),
        verbose_name="гандікап"
    )
    game_result = models.NullBooleanField(
        verbose_name="перемога"
    )
    technical_result = models.BooleanField(
        default=False,
        verbose_name="технічний результат"
    )
    round_skip = models.BooleanField(
        default=False,
        verbose_name="Пропуск туру"
    )
    game_record = models.FileField(
        null=True,
        blank=True,
        upload_to='uploads/game_records/'
    )

    class Meta:
        verbose_name = "результат партії"
        verbose_name_plural = "результати партії"

    def __str__(self):
        if self.tournament_player_opponent:
            return str(self.tournament_player.tournament.name) + ' @ ' + \
                   str(self.tournament_player) + ' vs. ' + \
                   str(self.tournament_player_opponent.player)
        else:
            return str(self.tournament_player.tournament.name) + ' @ ' + \
                   str(self.tournament_player) + ' - пропуск туру'
