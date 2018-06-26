
### to download images

python get_tiles.py --key YOUR_API_KEY --width 512 --height 512 --zoom 17 --num_images 10 --output_dir results/nyc_512a --augment True


### to combine them into single images

python copy_tiles.py --in_path results/nyc_512

