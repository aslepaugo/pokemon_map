from time import timezone
import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime

from pokemon_entities.models import Pokemon, PokemonEntity
from .settings import DEFAULT_IMAGE_URL


MOSCOW_CENTER = [55.751244, 37.618423]


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    local_time = localtime()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=local_time, disappeared_at__gt=local_time)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, 
            pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_entity.pokemon.get_image_url(request)
        )
    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.get_image_url(request),
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    local_time = localtime()
    requested_pokemon = get_object_or_404(Pokemon, pk=pokemon_id)
    pokemon = {
        "title_ru": requested_pokemon.title_ru,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "img_url": requested_pokemon.get_image_url(request),
        "description": requested_pokemon.description,
    }
    if requested_pokemon.next_evolutions.count():
        next_evolutions = requested_pokemon.next_evolutions.get()
        if next_evolutions:
            pokemon['next_evolutions'] = {
                "pokemon_id": next_evolutions.id,
                "title_ru": next_evolutions.title_ru,
                "img_url": next_evolutions.get_image_url(request),

            }    
    previous_evolutions = requested_pokemon.previous_evolution
    if previous_evolutions:
        pokemon['previous_evolution'] = {
            "pokemon_id": previous_evolutions.id,
            "title_ru": previous_evolutions.title_ru,
            "img_url": previous_evolutions.get_image_url(request),
        }    
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon.entities.filter(appeared_at__lt=local_time, disappeared_at__gt=local_time):
        add_pokemon(
            folium_map, 
            pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon['img_url']
        )
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
