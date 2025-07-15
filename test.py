import argparse
import os
import shutil
import subprocess
import cv2
import warnings

warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser()
parser.add_argument('--img1', type=str, required=True)
parser.add_argument('--img2', type=str, required=True)
parser.add_argument('--out', type=str, required=True)
parser.add_argument('--prompt', default='an anime scene', type=str)
args = parser.parse_args()

os.makedirs('temp_in')
# shutil.copy(args.img1, os.path.join('temp_in/frame1.png'))
# shutil.copy(args.img2, os.path.join('temp_in/frame2.png'))
img1 = cv2.imread(args.img1)
img2 = cv2.imread(args.img2)
h, w, c = img1.shape

if (h, w) != (320, 512):
    img1 = cv2.resize(img1, (512, 320))
    img2 = cv2.resize(img2, (512, 320))
cv2.imwrite('temp_in/frame1.png', img1)
cv2.imwrite('temp_in/frame2.png', img2)
with open(os.path.join('temp_in', 'prompts.txt'), 'w') as f:
    f.write(args.prompt)

command = 'sh scripts/run.sh'
subprocess.run(command, shell=True)

input_video = 'temp_out/tooncrafter_512_interp_seed123/samples_separate/frame1_sample0.mp4'
video = cv2.VideoCapture(input_video)
fps = video.get(cv2.CAP_PROP_FPS)
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
print(total_frames)

for i in range(total_frames):
    success, frame = video.read()

    if i == 8 and success:
        if (h, w) != (320, 512):
            frame = cv2.resize(frame, (w, h))
        cv2.imwrite(args.out, frame)
        break
video.release()
shutil.rmtree('temp_in', ignore_errors=True)
shutil.rmtree('temp_out', ignore_errors=True)