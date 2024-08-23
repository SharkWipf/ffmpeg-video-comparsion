A simple ffmpeg wrapper script to generate a side-by-side comparison video.  
Useful for sharing comparison videos without needing to set up a website with a javascript comparison slider.

Note: your ffmpeg needs to be built with drawtext support for labels to work. Not all distro ffmpeg builds have this.  
Fedora's ffmpeg seems not to have drawtext, but ffmpeg from conda-forge does, for a cross-compatible target.

```
usage: create_video_comparison.py [-h] [--label1 LABEL1] [--label2 LABEL2] [--sweep-speed SWEEP_SPEED] [--divider-width DIVIDER_WIDTH] [--font FONT] [--fontsize FONTSIZE] [--preset PRESET] [--crf CRF] [--vertical] input_video_1 input_video_2 output_video

Compare two videos with a moving divider.

positional arguments:
  input_video_1         Path to the first input video
  input_video_2         Path to the second input video
  output_video          Path for the output video

options:
  -h, --help            show this help message and exit
  --label1 LABEL1       Label for the first video
  --label2 LABEL2       Label for the second video
  --sweep-speed SWEEP_SPEED
                        Number of complete sweeps per minute
  --divider-width DIVIDER_WIDTH
                        Width of the divider
  --font FONT           Path to the font file
  --fontsize FONTSIZE   Font size for labels
  --preset PRESET       FFmpeg preset
  --crf CRF             Constant Rate Factor for video compression
  --vertical            Use vertical divide instead of horizontal
```



https://github.com/user-attachments/assets/81d4d724-7ec5-41bb-b633-94ae1610963c



https://github.com/user-attachments/assets/92073290-5438-44f8-8718-8cc410d25fb4



This script was originally hosted [as a gist](https://gist.github.com/SharkWipf/0d2781bbf82f04e331e6e1cf3d5393a9), but as more people started using it, I've moved it to a proper repo to avoid people running into licensing issues.

