# Wayfinder3D

A little application made with Python 3 and [CesiumJS](https://cesiumjs.org/) for creating 3D animations of multi-modal route recommendations from Google Maps.

## Instructions

`git clone https://github.com/willgeary/Wayfinder3D`

`cd Wayfinder3D`

(Optional) If you use anaconda, you can create and activate a virtual environment from the `environment.yml` file with:

`conda env create -f environment.yml`

`source activate Wayfinder3D`

You can generate directions from an origin to a destination via four modes: driving, transit, bicycling and walking.

```
python run.py \
--origin="Washington Square Park, New York City" \
--destination="Central Park, New York City" \
--modes="driving,transit,bicycling,walking"
```

View your app by navigating to [http://localhost:8000/](http://localhost:8000/) in your browser.

Voilà!

![img](https://i.imgur.com/LwygAdH.jpg)

Should you want to delete the virtual environment, you can do so with:

`conda env remove --name Wayfinder3D`
