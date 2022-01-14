#!/usr/bin/env python
# -*- coding: utf-8 -*-


category_keys = {
    "Cultural origins",
    "Derivative forms",
    "Fusion genres",
    "Local scenes",
    "Other topics",
    "Stylistic origins",
    "Subgenres",
    "Typical instruments",
}
genre_categories = {
    "Derivative forms",
    "Fusion genres",
    "Stylistic origins",
    "Subgenres",
}


def normalize_genre_name(genre_name: str) -> str:

    return genre_name.split("\n")[0]


def normalize_genre_key(genre_key: str) -> str:

    return normalize_genre_name(genre_key).lower()


def normalize_category_key(category_key: str) -> str:

    return category_key.lower().replace(" ", "_")


def normalize_category_values(category_values: str) -> list:

    updated_category_values = []
    for category_value in category_values:
        if category_value not in category_keys:
            category_value = normalize_category_key(category_value)
            updated_category_values.append(category_value)

    return updated_category_values


def normalize_category_data(category_data: dict) -> dict:

    normalized_category_data = {}
    for category_key, category_value in category_data.items():
        if category_key in genre_categories:
            genres = []
            for genre in category_value:
                if genre not in category_keys:
                    genres.append(normalize_genre_key(genre))
            category_value = genres
        normalized_category_data[category_key] = category_value

    return normalized_category_data
