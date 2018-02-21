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
--origin="Rome" \
--destination="Paris" \
--modes="driving,transit"
```

When you are done with the virtual environment, you can deactivate it with:

`source deactivate`

Should you want to later delete the virtual environment, you can do so with:

`conda env remove --name Wayfinder3D`



## License

MIT License

Copyright (c) 2018 Will Geary

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
