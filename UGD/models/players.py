from decimal import Decimal

from django.db import models

from . import City, Rank, LocalRank


class Player(models.Model):
    last_name = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="прізвище"
    )
    first_name = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="ім'я"
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="місто"
    )
    place = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="позиція в рейтингу"
    )
    rating = models.DecimalField(
        null=True,
        blank=True,
        max_digits=8,
        decimal_places=4,
        verbose_name="рейтинг"
    )
    rank = models.ForeignKey(
        Rank,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="ранг"
    )
    local_rank = models.ForeignKey(
        LocalRank,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="розряд"
    )
    sex = models.NullBooleanField(
        default=None,
        choices=(
            (False, '♀'),
            (True, '♂'),
        ),
        verbose_name="стать"
    )
    ufgo_member = models.BooleanField(
        default=False,
        verbose_name="Член УФГО"
    )
    active = models.BooleanField(
        default=False,
        verbose_name="Активний"
    )
    egd_pin = models.CharField(
        null=True,
        blank=True,
        max_length=8,
        verbose_name="Код гравця у EGD"
    )

    class Meta:
        verbose_name = "гравець"
        verbose_name_plural = "гравці"

    def __str__(self):
        if self.last_name and self.first_name:
            return self.last_name + ' ' + self.first_name
        else:
            return self.id

    def get_full_name(self):
        if self.last_name and self.first_name:
            return self.last_name + ' ' + self.first_name
        elif self.last_name:
            return self.last_name
        elif self.first_name:
            return self.first_name
        else:
            return ""

    def get_rating(self):
        return Decimal(self.rating).normalize()

    def get_number_of_tournaments(self):
        return self.tournamentplayer_set.count()

    def get_number_of_games(self):
        return self.tournamentplayer_set.filter(pairing_opponent__isnull=False).count()
