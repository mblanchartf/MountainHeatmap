# Mountain heatmap with OpenCV and GPXPY

This learning project pretends to show the mountain usage based on the GPX files that users upload to internet using only OpenCV and GPDXPY libraries. 
It uses the Google Maps API to obtain a satellite high resolution image. 

## Instructions

Join in a folder all the tracks you want to print over the satellite image. You can obtain them from Strava, Wikiloc...

Then run the mountain_heatmap.py script that has the following arguments: 

```bash
python mountain_heatmap.py -h
usage: mountain_heatmap.py [-h] -m MOUNTAIN_NAME -tpath TRACKS_PATH
                           [--z [ZOOM]] [--pxe [PX_ERROR]]

Generate heatmap from GPX tracks

required arguments:
  -m MOUNTAIN_NAME, --mountain_name MOUNTAIN_NAME
                        Mountain name for output file
  -tpath TRACKS_PATH, --tracks_path TRACKS_PATH
                        Path to the GPX tracks

optional arguments:
  -h, --help            show this help message and exit
  --z [ZOOM], --zoom [ZOOM]
                        Satellite image zoom
  --pxe [PX_ERROR], --px_error [PX_ERROR]
                        Pixel error value to differentiate between tracks

```

### Examples

```bash
python mountain_heatmap.py -m Puigpedros -tpath tracks_puigpedros/ --zoom 15 --pxe 6
Image created. Open file: tracks_puigpedros/20180703231116_Puigpedros_heatmap.png
```

<img src=screenshots/Puigpedros.png width=100% />


## Other examples

Teide:

<img src=screenshots/Teide.png width=100% />


Monteixo:

<img src=screenshots/Monteixo.png width=100% />


Pica d'Estats:

<img src=screenshots/Pica_Estats.png width=100% />


Vignemale:

<img src=screenshots/Vignemale.png width=100% />


Aneto:

<img src=screenshots/Aneto.png width=100% />


## Authors

* **Marc Blanchart** - *Learning project* - [MarcBlanchart](https://github.com/mblanchartf)

