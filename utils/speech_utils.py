import os


def convert_mp3_to_wav(input_path, output_path):
    cmd = f'ffmpeg -i {input_path} -acodec pcm_s16le -ac 1 -ar 16000 {output_path}'
    os.system(cmd)


if __name__ == '__main__':
    input_path = '/home/cilab/teja/SyncedUp/data/lipsync/input/ttsMP3.com_VoiceText_2023-12-13_15_47_58.mp3'
    output_path = '/home/cilab/teja/SyncedUp/data/lipsync/input/input.wav'
    convert_mp3_to_wav(input_path, output_path)