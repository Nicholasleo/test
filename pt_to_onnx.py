from ultralytics import YOLO

# Load a model
#model = YOLO('yolov8n.pt')  # load an official model
model = YOLO('/data/code/new_dnf/20240312/runs/detect/train/weights/best.pt')  # 预训练的 YOLOv8n 模型
#model = YOLO('/data/code/DNF/yolov8n.pt')  # 预训练的 YOLOv8n 模型
# Export the model
model.export(format='onnx')
print("ok")
