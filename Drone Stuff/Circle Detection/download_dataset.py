from roboflow import Roboflow

rf = Roboflow(api_key="LKMNlvypynSJUmpg6Wf9")

project = rf.workspace().project("circle-9po6m-sw919")

# Use a valid format like "yolov11" or "yolov11-txt" if you want the TXT version
dataset = project.version(1).download("yolov11")
