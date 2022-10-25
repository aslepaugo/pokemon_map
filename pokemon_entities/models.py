from pyexpat import model
from django.db import models  # noqa F401

class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name="Название покемона (рус.)")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="Название покемона (eng.)")
    title_jp = models.CharField(max_length=200, blank=True, verbose_name="Название покемона (jap.)")
    image = models.ImageField(null=True, blank=True, verbose_name="Изображение покемона")
    description = models.TextField(blank=True, verbose_name="Описание покемона")

    previous_evolution = models.ForeignKey(
        "self", 
        on_delete=models.SET_NULL, 
        related_name="next_evolutions", 
        null=True, 
        blank=True,
        verbose_name="Из кого эволюционировал")

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Покемон", related_name="entities")
    lat = models.FloatField(verbose_name="широта")
    lon = models.FloatField(verbose_name="долгота")
    appeared_at = models.DateTimeField(null=True, blank=True, verbose_name="Время и дата появления")
    disappeared_at = models.DateTimeField(null=True, blank=True, verbose_name="Время и дата исчезновения")
    level = models.IntegerField(null=True, blank=True, verbose_name="Уровень")
    health = models.IntegerField(null=True, blank=True, verbose_name="Здоровье")
    strength = models.IntegerField(null=True, blank=True, verbose_name="Сила")
    defence = models.IntegerField(null=True, blank=True, verbose_name="Защита")
    stamina = models.IntegerField(null=True, blank=True, verbose_name="Выносливость")
