import gdown
import os

class DrivingHead:
    def __init__(self) -> None:
        pass

    def download(self,url, output):

        id = url.split('/')[-2]
        gdown.download(id = id, output = output, quiet=False)

    
    def male_driving_vids(self):
        # 'https://drive.google.com/file/d/1ztpAh0P9fmWamBT3zSk9UHB0v_eZ12Ai/view?usp=drive_link'
        urls = ['https://drive.google.com/file/d/1ztpAh0P9fmWamBT3zSk9UHB0v_eZ12Ai/view?usp=sharing',
                'https://drive.google.com/file/d/1ggdOlZfwdABFxrjyFTtx4xPfBqOU7Fn4/view?usp=sharing',
                ]
        return urls
    
    def female_driving_vids(self):
        urls = ['https://drive.google.com/file/d/1UrJcZcwf7STHE_FlhiD2m6WAh0LeSrqq/view?usp=sharing',
                'https://drive.google.com/file/d/19ZU5q_Bef70vTRnECniZ1yNYCRGkiaqp/view?usp=sharing']
        
        return urls


    def julia_hair_back(self):
        urls = ['https://drive.google.com/file/d/1rF9ue2p-RrPLlz_8VbEikqC2RBYSSoBC/view?usp=sharing']
        return urls
    

    def julia_driving_heads(self):
        urls = ['https://drive.google.com/file/d/1ObX6GE0tcQxG9T5GU0pdkl1DgLPRiocQ/view?usp=sharing',
                'https://drive.google.com/file/d/1nm4DyLTqjErYPMX-oihJP6WDXY4GqoHs/view?usp=sharing']
        
        return urls


if __name__ == '__main__':
    dh = DrivingHead()
    urls = dh.male_driving_vids()
    output_path = 'data/male_driving_head/'
    os.makedirs(output_path, exist_ok=True)
    for no,url in enumerate(urls):
        dh.download(url, os.path.join(output_path, str(no) + '.mp4'))


    urls = dh.female_driving_vids()
    output_path = 'data/female_driving_head/'
    os.makedirs(output_path, exist_ok=True)
    for no,url in enumerate(urls):
        dh.download(url, os.path.join(output_path, str(no) + '.mp4'))