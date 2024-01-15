import os
import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from logzero import logger
def download_model():

    # check if the mdoel exists
    if os.path.exists('detector.tflite'):
        return

    cmd = 'wget -q -O detector.tflite -q https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite'
    os.system(cmd)


from typing import Tuple, Union
import math
import cv2
import numpy as np

MARGIN = 10  # pixels
ROW_SIZE = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (255, 0, 0)  # red


def _normalized_to_pixel_coordinates(
    normalized_x: float, normalized_y: float, image_width: int,
    image_height: int) -> Union[None, Tuple[int, int]]:
  """Converts normalized value pair to pixel coordinates."""

  # Checks if the float value is between 0 and 1.
  def is_valid_normalized_value(value: float) -> bool:
    return (value > 0 or math.isclose(0, value)) and (value < 1 or
                                                      math.isclose(1, value))

  if not (is_valid_normalized_value(normalized_x) and
          is_valid_normalized_value(normalized_y)):
    # TODO: Draw coordinates even if it's outside of the image bounds.
    return None
  x_px = min(math.floor(normalized_x * image_width), image_width - 1)
  y_px = min(math.floor(normalized_y * image_height), image_height - 1)
  return x_px, y_px


def visualize(
    image,
    detection_result,
    pad = (100,100)
) -> np.ndarray:
  """Draws bounding boxes and keypoints on the input image and return it.
  Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.
  Returns:
    Image with bounding boxes.
  """
  annotated_image = image.copy()
  height, width, _ = image.shape

  for detection in detection_result.detections:
    # Draw bounding_box
    bbox = detection.bounding_box
    start_point = bbox.origin_x, bbox.origin_y
    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height

    # crop the image
    img = image.copy()
    # img = img[int(start_point[1]):int(end_point[1]), int(start_point[0]):int(end_point[0])]

    # extend the image using the pad information
    x_min = max(0, int(start_point[0]) - pad[0])
    x_max = min(width, int(end_point[0]) + pad[0])
    y_min = max(0, int(start_point[1]) - pad[1])
    y_max = min(height, int(end_point[1]) + pad[1])
    img = img[y_min:y_max, x_min:x_max]

    return img
  
    # Draw keypoints
  return None

    # return annotated_image, start_point, end_point


def detection_result(IMAGE_FILE, base_options, pad = (100,100)):


    # STEP 2: Create an FaceDetector object.
    options = vision.FaceDetectorOptions(base_options=base_options)
    detector = vision.FaceDetector.create_from_options(options)

    # STEP 3: Load the input image.
    image = mp.Image.create_from_file(IMAGE_FILE)

    # STEP 4: Detect faces in the input image.
    detection_result = detector.detect(image)


    # STEP 5: Process the detection result. In this case, visualize it.
    image_copy = np.copy(image.numpy_view())

    annotated_image = visualize(image_copy, detection_result, pad = pad)


    return annotated_image




def vid2frame(inp_vid_path, out_path):
    os.makedirs(out_path, exist_ok=True)
   
    cap = cv2.VideoCapture(inp_vid_path)
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            count += 1

            strcount = str(count).zfill(4)
            cv2.imwrite(os.path.join(out_path, str(strcount) + '.png'), frame)
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    logger.info("Total frames: " + str(count))
    return count








if __name__ == '__main__':
    # download_model()




    
    # img = '/home/cilab/teja/demo_experiments/SyncedUp/vids/images/0001.png'
    # base_options = python.BaseOptions(model_asset_path='detector.tflite')
    # pad = (200,200)
    # out = detection_result(img, base_options, pad = pad)
    # cv2.imwrite('out.png', out)


    # inp = '/home/cilab/teja/demo_experiments/SyncedUp/vids/MVI_2280.MOV'
    # out = '/home/cilab/teja/demo_experiments/SyncedUp/vids/target'

    # vid2frame(inp, out)

    # inp = '/home/cilab/teja/demo_experiments/SyncedUp/sample_data/headmotion/input/head_poses.mp4'
    # out = '/home/cilab/teja/demo_experiments/SyncedUp/vids/source'

    # vid2frame(inp, out)

    from glob import glob
    from tqdm import tqdm
    imgs = glob('/home/cilab/teja/demo_experiments/SyncedUp/vids/target/*.png')

    for img in tqdm(imgs):
        try:
            base_options = python.BaseOptions(model_asset_path='detector.tflite')
            pad = (200,200)
            out = detection_result(img, base_options, pad = pad)

            out_path = img.replace('target', 'target_cropped')
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            cv2.imwrite(out_path, out)
            break
        except:
            pass