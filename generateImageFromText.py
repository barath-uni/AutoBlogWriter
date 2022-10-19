from tracemalloc import start
from min_dalle import MinDalle
import torch
from PIL import Image
import time

start_time = time.time()
model = MinDalle(
    models_root='./pretrained',
    dtype=torch.float32,
    device='cpu',
    is_mega=True, 
    is_reusable=True
)

print("STARTING TO GENERATE THE IMAGE")

image = model.generate_image(
    text='Ninja turtles wearing turban',
    seed=-1,
    grid_size=1,
    is_seamless=False,
    temperature=1,
    top_k=256,
    supercondition_factor=32,
    is_verbose=False
)

print(type(image))

# image = Image.frombytes(image)
image.save('image_Thing.png')

end_time = time.time()

print(f"TIME TAKE FOR THIS TO PRINT IS = {end_time-start_time}")