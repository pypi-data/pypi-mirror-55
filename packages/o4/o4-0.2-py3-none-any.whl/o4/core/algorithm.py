from o4.detection.detection import Detection
from o4.core import settings
from o4.core.dataset import Dataset
from o4.tracking.tracking import Tracking

from o4.video_processors.input import Camera
from o4.video_processors.input.panorama.panorama import Panorama
from o4.video_processors.output import VideoWriter

from o4.video_processors.input import IPCam
from o4.video_processors.input import Video
from o4.video_processors.output import window_viewer
from o4.video_processors.input import Image as ImageVideoProcessor

import numpy as np
import cv2
from PIL import Image, ImageDraw


class O4():

  def __init__(self, weights_file, names_file, anchors_path, gpu=0, not_detect=[], min_box_size=0, max_box_size=9999,
               detector_pass_frames=0):
    self.detection = Detection(weights_file, names_file, anchors_path, gpu=gpu, not_detect=not_detect,
                               min_box_size=min_box_size, max_box_size=max_box_size)
    self.tracking = Tracking()

    self.features = []
    self.broadcaster = False

    self.backSub = cv2.createBackgroundSubtractorMOG2()
    settings.DETECTOR_ON_N_FRAME = detector_pass_frames + 1

    self.save_video = False

    # dataset feature
    self.dataset_creation = False

    self.first_frame_processed = False
    self.detection_frame = 0

  def compute(self, frame, W, H, time_unit):
    f = frame.copy()
    detections = self.detection.detect(frame, W, H, time_unit)
    detections = self.tracking.measurement(frame, detections, time_unit)

    if self.dataset_creation:
      self.dataset.add(f, detections)

    return detections

  def fake_compute(self, time_unit):
    detections = self.tracking.predict_measurements(time_unit)
    return detections

  def get_colors(self):
    return self.detection.get_colors()

  def get_labels(self):
    return self.detection.get_labels()

  def get_unique_objects(self, classNames=[]):
    if classNames:
      count = 0
      for c in classNames:
        count += self.tracking.idByClassName[c]
      return count

    return self.tracking.idCounter

  def add_feature(self, feature):
    self.features.append(feature)

  def get_object_id(self, name):
    for i, l in enumerate(self.get_labels()):
      if l == name:
        return i
    raise Exception('no label with name: ' + name)

  def get_objects(self):
    return self.tracking.points

  def draw(self, frame, detections, time_unit):

    # convert to drawable PIL
    image = Image.fromarray(frame)
    image = image.convert("RGBA")
    tmp = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(tmp)

    for feature in self.features:
      feature.perform(self, frame, detections, time_unit)
      draw = feature.draw(self, draw, detections, time_unit)

    image = Image.alpha_composite(image, tmp)
    image = image.convert("RGB")

    frame = np.array(image)

    return frame

  def video(self, input_dir, output_dir, maxFrames=0, passFrames=1, initial_pass=0, save_video=True):
    self.video_processor = Video(input_dir, maxFrames=maxFrames, passFrames=passFrames, initial_pass=initial_pass)
    self.save_video = True

    if self.save_video:
      self.videoWriter = VideoWriter(output_dir)

  def ipcam(self, url):
    self.video_processor = IPCam(url)

  def camera(self, cameraNumber=0):
    self.video_processor = Camera(cameraNumber)

  def image(self, directory):
    self.video_processor = ImageVideoProcessor(directory)

  def panorama(self, directory1, directory2):
    self.video_processor = Panorama(ImageVideoProcessor(directory1), ImageVideoProcessor(directory2))

  def pre_process_frame(self, frame):
    fgMask = self.backSub.apply(frame)
    res = cv2.bitwise_and(frame, frame, mask=fgMask)
    return res

  def next(self):
    grabbed, frame, time_unit = self.video_processor.get_frame()

    if not grabbed:
      return False

    if not self.first_frame_processed:
      self.process_first_frame(frame)

    if self.detection_frame == 0:
      detections = self.compute(frame, self.WIDTH, self.HEIGHT, time_unit)
    else:
      detections = self.fake_compute(time_unit)

    self.detection_frame = (self.detection_frame + 1) % settings.DETECTOR_ON_N_FRAME

    frame = self.draw(frame, detections, time_unit)

    if self.broadcaster:
      pass
      # self.broadcaster.broadcast()

    window_viewer.show_frame(frame)
    if self.save_video:
      self.videoWriter.write(frame)

    return True

  def process_first_frame(self, frame):
    self.first_frame = frame
    (self.HEIGHT, self.WIDTH) = frame.shape[:2]
    for f in self.features:
      f.set_o4(self)

    self.tracking.setup(self)

    self.first_frame_processed = True

  def broadcast(self, urls, time, auth=None):
    broadcast_features = []

    for f in self.features:
      if f.broadcast:
        broadcast_features.append(f)

    # self.broadcaster = Broadcast(urls, time, broadcast_features, auth=auth)

  def show(self, feature, name="Feature", save_as=None):
    img = feature.draw(self, self.first_frame, [], 0)
    window_viewer.show_frame(img, name=name)
    if not save_as is None:
      cv2.imwrite(save_as, img)

  def close(self):
    window_viewer.close()
    self.end()

  def end(self):
    self.video_processor.close()

    if self.save_video:
      self.videoWriter.save()

    if self.dataset_creation:
      self.dataset.save()

  def dataset(self, dir, **kwargs):
    self.dataset_creation = True
    self.dataset = Dataset(dir, **kwargs)
