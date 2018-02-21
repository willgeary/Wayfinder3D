# Wayfinder3D

An application for comparing estimated travel times and directions on a 3D map.

Built with Python, CesiumJS and Google Maps API.

## Setup

`git clone https://github.com/willgeary/Wayfinder3D`

`cd Wayfinder3D`

(Optional) If you use anaconda, you can create and activate a virtual environment from the `environment.yml` file with:

`conda env create -f environment.yml`

`source activate Wayfinder3D`

## Instructions

You can generate directions from an origin to a destination via four modes: driving, transit, bicycling and walking like this:

```
python run.py \
--origin="Washington Square Park, New York City" \
--destination="Central Park, New York City" \
--modes="driving,transit,bicycling,walking"
```

View your app by navigating to [http://localhost:8000/](http://localhost:8000/) in your browser.

Voilà!

![img](https://i.imgur.com/LwygAdH.jpg)

If you only want to view select modes, such as driving and transit, you can do so like this:

```
python run.py \
--origin="Venice" \
--destination="Milan" \
--modes="driving,transit"
```
![img](https://i.imgur.com/S8e4hIx.jpg)

### Basemaps

You can select from Cesium's built in collection of basemaps by clicking on the imagery icon in the upper right corner:

![img](https://i.imgur.com/45QDYBe.jpg)

### Camera

You can force the camera to follow a particular mode by selecting the mode label and clicking the camera icon in the upper right.

![img](https://i.imgur.com/oxQd01T.jpg)


### Closing the app

You can terminate the local server with control + C or by closing the command line.

If you used a virtual environment, you can deactivate it with:

`source deactivate`

Should you want to later delete the virtual environment, you can do so with:

`conda env remove --name Wayfinder3D`


### License

Copyright (c) 2018 Will Geary

You are free to use this code however you want. If you do use it and like it please let me know!
