
 # django-mapbox-location-field
 [![Build Status](https://travis-ci.org/Simon-the-Shark/django-mapbox-location-field.svg?branch=master)](https://travis-ci.org/Simon-the-Shark/django-mapbox-location-field) [![Coverage Status](https://coveralls.io/repos/github/Simon-the-Shark/django-mapbox-location-field/badge.svg?branch=master)](https://coveralls.io/github/Simon-the-Shark/django-mapbox-location-field?branch=master)
 ![PyPI](https://img.shields.io/pypi/v/django-mapbox-location-field.svg)
 ****
 Simple in use **location model and form field** with **MapInput widget** for picking some location. Uses [mapbox gl js](https://docs.mapbox.com/mapbox-gl-js/), flexible map provider API. Fully compatible with bootstrap framework.
 ****


# Table of contents
* [Why this?](#why-this)
* [Live demo](#live-demo)
* [Compatibility](#compatibility)
 * [Instalation](#instalation)
* [Configuration](#configuration)
* [Usage](#usage)
* [Customization](#customization)
    * [map_attrs](#map_attrs)
    * [bootstrap](#bootstrap)
* [Admin interface usage](#admin-interface-usage)
* [AddressAutoHiddenField](#addressautohiddenfield)
* [Technologies](#technologies)

# Why this?
I was searching for some django location field which uses mapbox and I could use in my project. I didn't find anything which suits my needs in 100% and that is why I created this simple django app. My philosopy was simplicity but I wanted to create complete solution for picking location.

Feel free to open issues, make pull request and request some features or instructions. Let me know if you think it is not flexible enought.
# Compatibility
Automatically tested on Travis CI on versions:

* Django 1.11, 2.0, 2.1, 2.2
* Python 3.5, 3.6, 3.7

PS. Django 1.11 does not support Python 3.7 anymore.

#### Browser support
django-mapbox-location-field support all browsers, which are suported by mapbox gl js. Read more [here](https://docs.mapbox.com/help/troubleshooting/mapbox-browser-support/#mapbox-gl-js)

# Live demo
Curious how it works and looks like ? See live demo on https://django-mapbox-location-field.herokuapp.com
Demo app uses [django-bootstrap4](https://github.com/zostera/django-bootstrap4) for a little better looking form fields.

# Instalation
Using pip:
    `pip install django-mapbox-location-field`

# Configuration
* Add `"mapbox_location_field"` to `INSTALLED_APPS` in your settings file

```python
INSTALLED_APPS += ("mapbox_location_field",)
```

* Define [MAPBOX_KEY](https://docs.mapbox.com/help/how-mapbox-works/access-tokens/) in your settings file. This is vulnerable information which has to be passed to frontend, so it can be easily access by user. To ensure your safety, I would recommend using [url restrictions](https://docs.mapbox.com/help/how-mapbox-works/access-tokens/#url-restrictions) and [public scopes](https://docs.mapbox.com/help/how-mapbox-works/access-tokens/#scopes). More information on linked websites.
```python
MAPBOX_KEY = "pk.eyJ1IjoibWlnaHR5c2hhcmt5IiwiYSI6ImNqd2duaW4wMzBhcWI0M3F1MTRvbHB0dWcifQ.1sDAD43q0ktK1Sr374xGfw"
```
**PS. This above is only example access token. You have to paste here yours.**

# Usage
* Just create some model with LocationField.
```python
from django.db import models
from mapbox_location_field.models import LocationField

class SomeLocationModel(models.Model):
    location = LocationField()

```
* Create ModelForm
```python
from django import forms
from .models import Location

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = "__all__"
```
Of course you can also use CreateView, UpdateView or build Form yourself with mapbox_location_field.forms.LocationField


* Then just use it in html view. It can't be simpler!
Paste this in your html head:
```django
{% load mapbox_location_field_tags %}
{% location_field_includes %}
{% include_jquery %}
```
* And this in your body:
```django
   <form method="post">
        {% csrf_token %}
        {{form}}
        <input type="submit" value="submit">
    </form>
{{ form.media }}
```
* Your form is ready! Start your website and see how it looks. If you want to change something look to the [customization](#customization) section.

# Customization
In order to change few things you have to use `map_attrs` dictionary.
Default `map_attrs` looks like this:
```python
default_map_attrs = {
            "style": "mapbox://styles/mapbox/outdoors-v11",
            "zoom": 13,
            "center": [17.031645, 51.106715],
            "cursor_style": 'pointer',
            "marker_color": "red",
            "rotate": False,
            "geocoder": True,
            "fullscreen_button": True,
            "navigation_buttons": True,
            "track_location_button": True,
            "readonly": True,
            "placeholder": "Pick a location on map below",
        }
```
To change some values, just pass it when you creates model.
```python
from django.db import models
from mapbox_location_field.models import LocationField

class Location(models.Model):
    location = LocationField(map_attrs={"center": [0,0], "marker_color": "blue"})
```
## map_attrs
* style - `<string>`, mapbox style url. Read more [here](https://docs.mapbox.com/help/glossary/style-url/).
* zoom - `<int>`, map's zoom. Read more [here](https://docs.mapbox.com/help/glossary/zoom-level/).
* center - `<list>` or `<tuple>` of `<float>`s, defaults map's center point in [`latitude`, `longitude`]
* cursor_style - `<string>`, css cursor style. Read more [here](https://www.w3schools.com/cssref/pr_class_cursor.asp).
* marker_color - `<string>` css color property. Read more [here](https://www.w3schools.com/cssref/css_colors_legal.asp)  and [here](https://www.w3schools.com/cssref/css_colors.asp).
* rotate - `<bool>`, whether you can rotate map with right mouse click or not.
* geocoder -`<bool>`, whether geocoder searcher is showed or not.
* fullscreen_button - `<bool>`, whether fullscreen button is showed or not.
* navigation_buttons - `<bool>`, whether navigation buttons are showed or not.
* track_location_button - `<bool>`, whether show my location button is showed or not.
* readonly - `<bool>`, whether user can type location in text input
* placeholder - `<string>`, text input's placeholder

## bootstrap
MapInput widget is fully compatibile with bootstrap library. I can even recommend to use it with [django-bootstrap4](https://github.com/zostera/django-bootstrap4) or [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms).

# Admin interface usage
First create some model with location field like in [usage section](#usage).
Then register it in admin interface like this:
```python
from django.contrib import admin
from .models import Location
from mapbox_location_field.admin import MapAdmin

admin.site.register(Location, MapAdmin)
```
In example above, Location is name of your model.
Everything from [customization section](#customization) also works in admin interface.

# AddressAutoHiddenField
AddressAutoHiddenField is field for storing address. It uses AddressAutoHiddenInput which is hidden and when you place your marker on map, automatically fill itself with proper address.
In order to use it just add it to your model. Something like this:
```python
class Location(models.Model):
    location = LocationField()
    address = AddressAutoHiddenField()
```

# Technologies
* Django
* mapbox gl js
* jquery
* html and css
