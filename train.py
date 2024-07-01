from ultralytics import YOLO

# 加载模型
model = YOLO('./yolov8n.pt')  # 加载预训练模型（推荐用于训练）

# 使用1个GPU训练模型
results = model.train(data='./bns.yaml', epochs=50, imgsz=640, device=[0])

