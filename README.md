# itgc-2022-map



[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6383012.svg)](https://doi.org/10.5281/zenodo.6383012)



A Python-flask site to display science of [ITGC](https://thwaitesglacier.org/) cruise NBP 2202 in a leaflet map.

This repo contains the source code for the interactive map at [nbp2202map.com/](https://nbp2202map.com/)

The map is built on a one page Python flask app inspired by the [UEA glider group piloting site](https://github.com/ueaglider/ueaglider-web)

All data are from the ITGC 2202 NBP cruise aboard the Nathaniel B Palmer. All data should be considered 
approximate and subject to arbitrary change. Contact the PIs of ITGC for all data quieries. Data are stored
as geojson in [itgc/static/nbp_data](https://github.com/callumrollo/itgc-2022-map/tree/main/itgc/static/nbp_data).

# How to run this app

1. Download the [nbp2202 website source code](https://github.com/callumrollo/itgc-2022-map) from this GitHub repository
[click here](https://github.com/callumrollo/itgc-2022-map/archive/refs/heads/main.zip) to get the zip file
2. Create a Python environment using pip with the requirements.txt file or conda with the environment.yml file.
3. navigate to the directory containing this README and run the command `python itgc/app.py`
4. Open a browser window and go to http://127.0.0.1:5000/
5. That's it! You're running the app on your very own PC. You should see a website that looks and functions just like the one at [nbp2202map.com](https://nbp2202map.com) but it is running solely on your PC


**NB** The ice imagery was too big for GitHub, it is included in the zenodo repository

For more detail on how to adapt the site to your needs, or host it on an cloud server, check out the [blog post](https://callumrollo.github.io/flask_leaflet.html)

### Copyright

This project is open source and avaialbe under the [MIT license](https://github.com/callumrollo/itgc-2022-map/blob/main/LICENSE). Feel free to copy, remix and reuse with attribution.

This is a personal project by Callum Rollo. It has no official support or endorsment from ITGC.

This project was made possible by [Voice of the Ocean Foundation](https://voiceoftheocean.org) paying Callum Rollo's salary while he built it.

### TODO

- [x] add installation instructions
- [x] upload static data
- [ ] remove unnecessary JS
- [ ] create branch for use on NBP
