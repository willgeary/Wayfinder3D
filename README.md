# Wayfinder3D

A Python and Cesium application for creating 3D animations of multi-modal route recommendations from Google Maps.

## Instructions

Download this repository and `cd` into it.

(Optional) If you use anaconda, you create a virtual environment from the `environment.yml` file.

`conda env create -f environment.yml`

You can visualize driving, transit, bicycling and walking directions from an origin to a destination like this:

`python run.py --origin="Washington Square Park, New York City" \
               --destination="Central Park, New York City" \
               --modes="driving,transit,bicycling,walking"`
