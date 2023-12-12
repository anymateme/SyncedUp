from logzero import logger
import os


class faceswap:
    def __init__(self, configs):
        self.configs = configs

    def run(self):
        logger.debug("Running faceswap")

        module_name = self.configs['faceswap']['repo_name']
        
        if module_name == "roop":
            self.download_models(module_name)
            self.run_module(module_name)


    def download_models(self, module_name):
        logger.debug("Downloading models for {}".format(module_name))

        if module_name == "roop":

            # check if the onnx model exists in the models directory
            if os.path.exists('models/faceswap/roop/inswapper_128.onnx'):
                logger.debug("Faceswap model already exists")
                return
            
            logger.debug("Downloading faceswap model")
            cmd = 'wget https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx -O inswapper_128.onnx'
            os.system(cmd)

            os.makedirs('models/faceswap/roop', exist_ok=True)
            os.system('mv inswapper_128.onnx models/faceswap/roop/inswapper_128.onnx')



    def run_module(self, module_name):
        
        if module_name == "roop":
            logger.debug("Running faceswap module: {}".format(module_name))

            input_video, photo = self.configs['faceswap']['input_path']
            output_video = self.configs['faceswap']['output_path']

            # make the output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_video), exist_ok=True)

            cmd = f'src/faceswap/roop/run.py --target {input_video} --output-video-quality 80 --source {photo} -o {output_video} --execution-provider cuda --frame-processor face_swapper face_enhancer'

            os.system(cmd)

            logger.debug("Faceswap module finished")


