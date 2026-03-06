from ultralytics import YOLO
import torch

print("CUDA Available:", torch.cuda.is_available())
print("GPU:", torch.cuda.get_device_name(0))

model = YOLO("yolov8n.pt")
model.to("cuda")

results = model.predict(source=0, show=True)