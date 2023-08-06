import os
import numpy as np
import cv2


def load_model(weights_file,names_file,anchors_path):
  # load the COCO class labels our YOLO model was trained on
  labelsPath = names_file
  print(labelsPath)
  print(os.getcwd())
  LABELS = open(labelsPath).read().strip().split("\n")


  # derive the paths to the YOLO weights and model configuration
  weightsPath = weights_file
  configPath = anchors_path

  # load our YOLO object detector trained on COCO dataset (80 classes)
  # and determine only the *output* layer names that we need from YOLO
  print("[INFO] loading YOLO from disk...")
  net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
  ln = net.getLayerNames()
  ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


  return net, ln, LABELS
