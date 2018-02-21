# Wayfinder3D

An application for comparing estimated travel times and directions in 3D. Built with Python, CesiumJS and Google Maps API.

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

When you are done with the virtual environment, you can deactivate it with:

`source deactivate`

Should you want to later delete the virtual environment, you can do so with:

`conda env remove --name Wayfinder3D`


Copyright (c) 2018 Will Geary
