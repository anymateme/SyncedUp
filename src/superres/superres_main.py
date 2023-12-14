from logzero import logger
import os
import cv2
import shutil

class superres:
    def __init__(self, config):
        self.config = config

    def run(self):
        if self.config['superres']['repo_name'] == 'gfpgan':
            self.download_models()
            self.run_module()


    def download_models(self):
        if self.config['superres']['repo_name'] == 'gfpgan':
            os.makedirs('experiments/pretrained_models', exist_ok=True)
            if os.path.exists('experiments/pretrained_models/GFPGANv1.3.pth'):
                logger.debug("GFPGAN model already exists")
                return
            logger.debug("Downloading GFPGAN model")
            cmd = 'wget https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth -P experiments/pretrained_models'
            os.system(cmd)


    def run_module(self):

        vid_path = self.config['superres']['input_path']

        # make a dir called images in the input path
        vid_dir = os.path.dirname(vid_path)
        shutil.rmtree(os.path.join(vid_dir, 'images'), ignore_errors=True)
        os.makedirs(os.path.join(vid_dir, 'images'), exist_ok=True)

        # extract frames from the video
        cmd = f'ffmpeg -i {vid_path} -r 1 {os.path.join(vid_dir, "images")}/%05d.png'
        os.system(cmd)


        output_path = self.config['superres']['output_path']
        inp_img_dir = os.path.join(vid_dir, 'images')

        shutil.rmtree(output_path, ignore_errors=True)
        os.makedirs(output_path, exist_ok=True)

        cmd = f'python src/superres/GFPGAN/inference_gfpgan.py -i {inp_img_dir} -o {output_path} -v 1.3 -s 2'
        os.system(cmd)

        # fps of the original video 
        fps = cv2.VideoCapture(vid_path).get(cv2.CAP_PROP_FPS)

        # make a video from the frames
        cmd = f'ffmpeg -r {fps} -i {os.path.join(output_path,"restored_imgs" ,"%05d.png")} -vcodec libx264 -crf 25 -pix_fmt yuv420p {os.path.join(output_path, "output.mp4")}'
        os.system(cmd)

        # add the audio to the video
        cmd = f'ffmpeg -i {vid_path} -i {os.path.join(output_path, "output.mp4")} -c copy -map 0:v:0 -map 1:a:0 {os.path.join(output_path, "output_with_audio.mp4")}'
        os.system(cmd)
