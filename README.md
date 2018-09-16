# Download pairs of images from Mapbox

You will need an [Mapbox](https://mapbox.com) API key.

## To download images

```sh
python get_tiles.py \
  --key YOUR_API_KEY \ 
  --width 256 --height 256 --zoom 17 --num_images 10 \
  --output_dir results/nyc_256a --augment 1 \
  --lat_min -74.004503 --lng_min 40.563883 \
  --lat_max -73.732700 --lng_max 40.895277 \
  --style_map USERNAME/MAP_ID
```

## Post-processing

```sh
python post_processing.py --in_path results/nyc_512 --combine 0 --w 1024 --h 512 --frac 0.75 --label_map 1
```

`--combine` : to concatenate into single image (pix2pix) or separate directories
`--w` and `--h` : output width and height, center-cropped from originals
`--frac` : zooming factor to crop smaller subset of image (1.0 = use whole image)
`--label_map` : output label map which is 1-channels denoting index of class, otherwise use original label colors