# Wayfinder3D

A Python and Cesium application for creating 3D animations of multi-modal route recommendations from Google Maps.

## Instructions

Download this repository and `cd` into it.

(Optional) If you use anaconda, you can create and activate a virtual environment from the `environment.yml` file with:

`conda env create -f environment.yml`
`source activate wayfinder3D`

You can generate directions from an origin to a destination via four modes: driving, transit, bicycling and walking.

```
python run.py \
--origin="Washington Square Park, New York City" \
--destination="Central Park, New York City" \
--modes="driving,transit,bicycling,walking"
```

View your app by navigating to `http://localhost:8000/` in your browser.

Voilà!

![img](https://i.imgur.com/LwygAdH.jpg)
