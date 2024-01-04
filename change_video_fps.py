import cv2
import os
import subprocess
from tqdm import tqdm

def get_frame_rate(video_path):
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    return fps

def convert_fps(input_file, output_file, target_fps):
    cmd = [
        'ffmpeg', '-i', input_file, '-filter:v', f'fps=fps={target_fps}',
        '-c:a', 'copy', output_file
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def process_folder(input_folder, output_folder, target_fps):
    os.makedirs(output_folder, exist_ok=True)  # 确保输出文件夹存在
    file_number = 1

    for root, dirs, files in os.walk(input_folder):
        for filename in  tqdm(files):
            if filename.endswith(".mp4"):
                input_file = os.path.join(root, filename)
                current_fps = get_frame_rate(input_file)
                
                if current_fps >= target_fps:
                    output_file = os.path.join(output_folder, f"{file_number}.mp4")
                    convert_fps(input_file, output_file, target_fps)
                    file_number += 1

# 使用示例
input_folder = "./HDTF_DATA"  # 输入文件夹路径
output_folder = "./HDTF_DATA_25fps"  # 输出文件夹路径
target_fps = 25  # 目标帧率，可根据需要更改
process_folder(input_folder, output_folder, target_fps)
