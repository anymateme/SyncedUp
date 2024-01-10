from logzero import logger
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skimage.transform import resize
import warnings
import os
import imageio
import imageio_ffmpeg
import torch
import gdown


class HeadMotion:
    def __init__(self, configs):
        self.configs = configs
    
    def run(self):
        logger.debug("Running HeadMotion")
        module_name = self.configs['headmotion']['repo_name']
        if module_name == 'thinspline':
            self.download_models(module_name)
            self.run_module(module_name)

        
    def download_models(self, module_name):

        if module_name == 'thinspline':

            # checxk if the checkpoints exist
            if os.path.exists('src/HeadMotion/thinspline/checkpoints/vox.pth.tar'):
                logger.info("vox.pth.tar exists")
                return

            
            os.makedirs('src/HeadMotion/thinspline/checkpoints', exist_ok=True)

            url = 'https://drive.google.com/file/d/1wDRjWBwXLfF4KBXHtnqegvuKEOOZJ6Ve/view?usp=sharing'
            id = url.split('/')[-2]
            output = 'src/HeadMotion/thinspline/checkpoints/vox.pth.tar'
            gdown.download(id = id, output = output, quiet=False)
            logger.info("downloaded vox.pth.tar")


    def run_module(self, module_name):

        print ("Running " + module_name)

        import sys

        sys.path.append('src/headmotion/thinspline')

        if module_name == 'thinspline':
            device = torch.device('cuda:0')
            dataset_name = 'vox' # ['vox', 'taichi', 'ted', 'mgif']

            source_image_path = self.configs['headmotion']['input_path'][0]
            driving_video_path = self.configs['headmotion']['input_path'][1]

            output_path = self.configs['headmotion']['output_path']

            output_video_path = os.path.join(output_path, 'output.mp4')
            config_path = 'src/headmotion/thinspline/config/vox-256.yaml'
            checkpoint_path = 'src/HeadMotion/thinspline/checkpoints/vox.pth.tar'
            predict_mode = 'relative' # ['standard', 'relative', 'avd']
            find_best_frame = False # when use the relative mode to animate a face, use 'find_best_frame=True' can get better quality result

            pixel = 256 # for vox, taichi and mgif, the resolution is 256*256
            if(dataset_name == 'ted'): # for ted, the resolution is 384*384
                pixel = 384

            source_image = imageio.imread(source_image_path)
            reader = imageio.get_reader(driving_video_path)

            source_image = resize(source_image, (pixel, pixel))[..., :3]

            fps = reader.get_meta_data()['fps']
            driving_video = []
            try:
                for im in reader:
                    driving_video.append(im)
            except RuntimeError:
                pass
            reader.close()

            driving_video = [resize(frame, (pixel, pixel))[..., :3] for frame in driving_video]


            from src.headmotion.thinspline.demo import load_checkpoints
            from src.headmotion.thinspline.demo import make_animation
            from skimage import img_as_ubyte
            from src.headmotion.thinspline.demo import find_best_frame as _find
            inpainting, kp_detector, dense_motion_network, avd_network = load_checkpoints(config_path = config_path, 
                                                                                          checkpoint_path = checkpoint_path, 
                                                                                          device = device)

            if predict_mode=='relative' and find_best_frame:
                
                i = _find(source_image, driving_video, device.type=='cpu')
                print ("Best frame: " + str(i))
                driving_forward = driving_video[i:]
                driving_backward = driving_video[:(i+1)][::-1]
                predictions_forward = make_animation(source_image, driving_forward, inpainting, kp_detector, dense_motion_network, avd_network, device = device, mode = predict_mode)
                predictions_backward = make_animation(source_image, driving_backward, inpainting, kp_detector, dense_motion_network, avd_network, device = device, mode = predict_mode)
                predictions = predictions_backward[::-1] + predictions_forward[1:]
            else:
                predictions = make_animation(source_image, driving_video, inpainting, kp_detector, dense_motion_network, avd_network, device = device, mode = predict_mode)


        

            os.makedirs(output_path, exist_ok=True)
            #save resulting video
            imageio.mimsave(output_video_path, [img_as_ubyte(frame) for frame in predictions], fps=fps)



            

if __name__ == '__main__':
    pass