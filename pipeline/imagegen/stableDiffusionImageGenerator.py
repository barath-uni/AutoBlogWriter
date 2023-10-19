
from diffusers import StableDiffusionPipeline
import torch
import time
from pathlib import Path
import string
import random
import cv2
import numpy as np

start_time = time.time()
my_token = "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"
# get your token at https://huggingface.co/settings/tokens
LOCAL_IMAGE_PATH = Path("/home/barath/codespace/coolerssstack/public")
RELATIVE_IMAGE_PATH = Path("assets/images/posts/hero")

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_hero_image(prompt:str, height=256, width=256):
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    pipe.to("cpu")
    image = pipe(prompt, height=height, width=width).images[0]
    id = id_generator()
    # image = pipe(prompt=prompt,image=img, mask_image=mask,strength=0.8).images[0]
    image.save(f"{Path(LOCAL_IMAGE_PATH, RELATIVE_IMAGE_PATH)}/{id}_{prompt.replace(' ', '_')[:8]}.png")
    print(f"IT TOOK = {time.time()-start_time}")
    # Returning the place where the hero image will be in the nextjs template(:TODO change the directory structure for the current proj)
    return f"{RELATIVE_IMAGE_PATH}/{id}_{prompt.replace(' ', '_')[:8]}.png"

def try_gpt_image_gen():
    image = cv2.imread('/home/barath/codespace/coolerssstack/public/assets/images/posts/Bajaj_PX_97_TORQUE_(.jpg')
    
    background = np.full((1024, 1024, 3), 255, dtype=np.uint8)

    # Convert the image to grayscale and threshold it to create a binary mask
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 255, 255, cv2.THRESH_BINARY_INV)

    # Create a mask with the same size as the image
    mask = np.full(image.shape[:2], 255, dtype=np.uint8)

    # Remove the white background from the image and mask
    image = cv2.bitwise_and(image, image, mask=thresh)
    mask = cv2.bitwise_and(mask, mask, mask=thresh)

    # Resize the image to fit the background
    image_height, image_width, _ = image.shape
    background_height, background_width, _ = background.shape
    # scale = min(background_width / image_width, background_height / image_height)
    # new_width = int(image_width * scale)
    # new_height = int(image_height * scale)
    # image = cv2.resize(image, (new_width, new_height))

    # Add the image to the center of the background and the mask to the image
    x_offset = (background_width - image_width) // 2
    y_offset = (background_height - image_height) // 2
    background[y_offset:y_offset+image_height, x_offset:x_offset+image_width] = image
    # mask[y_offset:y_offset+image_height, x_offset:x_offset+image_width] = 0
    gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 255, 255, cv2.THRESH_BINARY_INV)
    mask = np.full(background.shape[:2], 255, dtype=np.uint8)

    # Remove the white background from the image and mask
    background = cv2.bitwise_and(background, background, mask=thresh)
    mask = cv2.bitwise_and(mask, mask, mask=thresh)
    print(background.shape)
    # Save the new image and mask
    cv2.imwrite('new_image.png', background)
    cv2.imwrite('mask.png', mask)