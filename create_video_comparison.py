#!/usr/bin/env python3

import sys
import os
import subprocess
import json
import argparse

def get_video_info(video_path):
    cmd = [
        'ffprobe', '-v', 'quiet', '-print_format', 'json',
        '-select_streams', 'v:0', '-count_packets',
        '-show_entries', 'stream=width,height,r_frame_rate,duration',
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    info = json.loads(result.stdout)
    stream = info['streams'][0]
    
    framerate = eval(stream['r_frame_rate'])
    return {
        'width': stream['width'],
        'height': stream['height'],
        'framerate': f"{framerate:.2f}",
        'duration': float(stream['duration'])
    }

def process_videos(input_video_1, input_video_2, output_video, args):
    label_1 = args.label1 or os.path.basename(input_video_1)
    label_2 = args.label2 or os.path.basename(input_video_2)

    video1_info = get_video_info(input_video_1)
    video2_info = get_video_info(input_video_2)

    if video1_info != video2_info:
        print("Error: Input videos must have the same resolution and framerate.")
        sys.exit(1)

    width = video1_info['width']
    height = video1_info['height']
    duration = video1_info['duration']

    # Calculate the frequency based on sweeps per minute
    frequency = args.sweep_speed / 60

    if args.vertical:
        blend_expr = f'if(gte(Y,H*(0.5+0.5*sin(2*PI*{frequency}*T))),A,B)'
        overlay_expr = f'0:(H-{args.divider_width})*(0.5+0.5*sin(2*PI*{frequency}*t))'
        divider_size = f'{width}x{args.divider_width}'
    else:
        blend_expr = f'if(gte(X,W*(0.5+0.5*sin(2*PI*{frequency}*T))),A,B)'
        overlay_expr = f'(W-{args.divider_width})*(0.5+0.5*sin(2*PI*{frequency}*t)):0'
        divider_size = f'{args.divider_width}x{height}'

    filter_complex = f"""
    [0:v][1:v]scale2ref[v0][v1];
    [v0]drawtext=fontfile={args.font}:fontsize={args.fontsize}:fontcolor=white@0.5:box=1:boxcolor=black@0.5:boxborderw=5:x=10:y=10:text='{label_2}',
        drawtext=fontfile={args.font}:fontsize={args.fontsize}:fontcolor=white@0.5:box=1:boxcolor=black@0.5:boxborderw=5:x=w-tw-10:y=10:text='{label_2}',
        drawtext=fontfile={args.font}:fontsize={args.fontsize}:fontcolor=white@0.5:box=1:boxcolor=black@0.5:boxborderw=5:x=10:y=h-th-10:text='{label_2}',
        drawtext=fontfile={args.font}:fontsize={args.fontsize}:fontcolor=white@0.5:box=1:boxcolor=black@0.5:boxborderw=5:x=w-tw-10:y=h-th-10:text='{label_2}'[v0labeled];
    [v1]drawtext=fontfile={args.font}:fontsize={args.fontsize}:fontcolor=white@0.5:box=1:boxcolor=black@0.5:boxborderw=5:x=10:y=10:text='{label_1}',
        drawtext=fontfile={args.font}:fontsize={args.fontsize}:fontcolor=white@0.5:box=1:boxcolor=black@0.5:boxborderw=5:x=w-tw-10:y=10:text='{label_1}',
        drawtext=fontfile={args.font}:fontsize={args.fontsize}:fontcolor=white@0.5:box=1:boxcolor=black@0.5:boxborderw=5:x=10:y=h-th-10:text='{label_1}',
        drawtext=fontfile={args.font}:fontsize={args.fontsize}:fontcolor=white@0.5:box=1:boxcolor=black@0.5:boxborderw=5:x=w-tw-10:y=h-th-10:text='{label_1}'[v1labeled];
    [v0labeled][v1labeled]blend=all_expr='{blend_expr}':shortest=1[blended];
    color=white:s={divider_size}[bar];
    [blended][bar]overlay='{overlay_expr}'
    """

    cmd = [
        'ffmpeg', '-i', input_video_2, '-i', input_video_1,
        '-filter_complex', filter_complex,
        '-c:v', 'libx264', '-preset', args.preset, '-crf', str(args.crf),
        '-t', str(duration), output_video
    ]

    subprocess.run(cmd, check=True)
    print(f"Video processing complete. Output saved as {output_video}")

def main():
    parser = argparse.ArgumentParser(description="Compare two videos with a moving divider.")
    parser.add_argument("input_video_1", help="Path to the first input video")
    parser.add_argument("input_video_2", help="Path to the second input video")
    parser.add_argument("output_video", help="Path for the output video")
    parser.add_argument("--label1", help="Label for the first video")
    parser.add_argument("--label2", help="Label for the second video")
    parser.add_argument("--sweep-speed", type=float, default=60, help="Number of complete sweeps per minute")
    parser.add_argument("--divider-width", type=int, default=8, help="Width of the divider")
    parser.add_argument("--font", default="/usr/share/fonts/gnu-free/FreeSansBold.ttf", help="Path to the font file")
    parser.add_argument("--fontsize", type=int, default=24, help="Font size for labels")
    parser.add_argument("--preset", default="veryslow", help="FFmpeg preset")
    parser.add_argument("--crf", type=int, default=23, help="Constant Rate Factor for video compression")
    parser.add_argument("--vertical", action="store_true", help="Use vertical divide instead of horizontal")

    args = parser.parse_args()

    for file in [args.input_video_1, args.input_video_2]:
        if not os.path.isfile(file) or not os.access(file, os.R_OK):
            print(f"Error: File '{file}' does not exist or is not readable.")
            sys.exit(1)

    process_videos(args.input_video_1, args.input_video_2, args.output_video, args)

if __name__ == "__main__":
    main()