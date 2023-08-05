from o4.detection.detectors import DnnYoloDetector
from o4.detection.detectors.yolo3_keras.detector import YoloKerasDetector
from tensorflow.python.client import device_lib


class Detection():

  def __init__(self, weights_file, names_file,anchors_path, confidence=0.5, threshold=0.3, min_box_size=20, max_box_size=1000,
               gpu=False, not_detect=[]):
    if gpu == True:
      gpu = len(list(filter(lambda x: x.device_type == 'GPU', device_lib.list_local_devices())))

    if gpu >= 1:
      self.detector = YoloKerasDetector(weights_file, names_file, confidence=confidence, threshold=threshold, gpu=gpu)
    else:
      self.detector = DnnYoloDetector(weights_file, names_file,anchors_path, confidence=confidence, threshold=threshold)

    self.detector.set_min_box_size(min_box_size)
    self.detector.set_max_box_size(max_box_size)
    self.detector.set_not_detect(not_detect)

  def set_detector(self, detector):
    self.detector = detector

  def get_colors(self):
    return self.detector.get_colors()

  def get_labels(self):
    return self.detector.get_labels()

  def detect(self, frame, W, H, time_unit):
    return self.detector.detect(frame, W, H, time_unit)
