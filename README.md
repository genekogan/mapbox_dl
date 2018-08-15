# Download pairs of images from Mapbox

You will need an [Mapbox](https://mapbox.com) API key.

## To download images

```sh
python get_tiles.py \
  --key YOUR_API_KEY \ 
  --width 256 --height 256 --zoom 17 --num_images 10 \
  --output_dir results/nyc_256a --augment True \
  --lat_min -74.004503 --lng_min 40.563883 \
  --lat_max -73.732700 --lng_max 40.895277 \
  --style_map USERNAME/MAP_ID
```

## To combine them into single images

```sh
python copy_tiles.py --in_path results/nyc_512
```
