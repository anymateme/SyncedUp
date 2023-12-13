from logzero import logger
import os

class lipsync:
    def __init__(self, configs):
        self.configs = configs
    
    def run(self):
        logger.debug("Running lipsync")

        module_name = self.configs['lipsync']['repo_name']
        
        if module_name == "wav2lip":
            
            os.makedirs('temp/', exist_ok=True)

            self.download_models(module_name)
            self.run_module(module_name)


    def download_models(self, module_name):

        if module_name == 'wav2lip':
            
            os.makedirs('src/lipsync/Wav2Lip/face_detection/detection/sfd', exist_ok=True)
            os.makedirs('src/lipsync/Wav2Lip/checkpoints', exist_ok=True)
            
            # check if the wav2lip model exists in the models directory
            if os.path.exists('src/lipsync/Wav2Lip/face_detection/detection/sfd/s3fd.pth'):
                logger.debug("Wav2lip model already exists")
                return
            
            logger.debug("Downloading wav2lip model")
            cmd = 'wget "https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth" -O "src/lipsync/Wav2Lip/face_detection/detection/sfd/s3fd.pth"'
            os.makedirs('src/lipsync/Wav2Lip/face_detection/detection/sfd', exist_ok=True)
            os.system(cmd)

            cmd = "wget 'https://iiitaphyd-my.sharepoint.com/personal/radrabha_m_research_iiit_ac_in/_layouts/15/download.aspx?share=EdjI7bZlgApMqsVoEUUXpLsBxqXbn5z8VTmoxp55YNDcIA' -O 'src/lipsync/Wav2Lip/checkpoints/wav2lip_gan.pth'"
            os.makedirs('src/lipsync/Wav2Lip/checkpoints', exist_ok=True)
            os.system(cmd)
    
    def run_module(self, module_name):

        if module_name == 'wav2lip':
            
            model_path = 'src/lipsync/Wav2Lip/checkpoints/wav2lip_gan.pth'
            video_path, audio_path = self.configs['lipsync']['input_path']
            output_video = self.configs['lipsync']['output_path']

            # make the output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_video), exist_ok=True)

            cmd = f'python3 src/lipsync/Wav2Lip/inference.py --checkpoint_path {model_path} --face {video_path} --audio {audio_path} --outfile {output_video}'
            os.system(cmd)
        