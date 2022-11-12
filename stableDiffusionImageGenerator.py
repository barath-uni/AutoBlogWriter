
from diffusers import StableDiffusionPipeline
import torch
import time
from pathlib import Path
import random
start_time = time.time()
my_token = "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"
# get your token at https://huggingface.co/settings/tokens
LOCAL_IMAGE_PATH = Path("/home/barath/codespace/coolerssstack/public")
RELATIVE_IMAGE_PATH = Path("assets/images/posts/hero")

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_hero_image(prompt:str):
    pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", use_auth_token=my_token)
    pipe.to("cpu")
    image = pipe(prompt, height=600, width=1048).images[0]
    # image = pipe(prompt=prompt,image=img, mask_image=mask,strength=0.8).images[0]
    image.save(f"{Path(LOCAL_IMAGE_PATH, RELATIVE_IMAGE_PATH)}/{id}_{prompt.replace(' ', '_')[:8]}.png")
    print(f"IT TOOK = {time.time()-start_time}")
    # Returning the place where the hero image will be in the nextjs template(:TODO change the directory structure for the current proj)
    return f"{RELATIVE_IMAGE_PATH}/{id}_{prompt.replace(' ', '_')[:8]}.png"