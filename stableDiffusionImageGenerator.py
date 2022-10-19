
from diffusers import StableDiffusionPipeline
import torch
import time
start_time = time.time()
my_token = "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"
# get your token at https://huggingface.co/settings/tokens
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", use_auth_token=my_token)
pipe.to("cpu")

def create_hero_image(prompt:str):
    image = pipe(prompt, height=600, width=1080).images[0]
    image.save(f"output/hero/{prompt.replace(' ', '_')}+.png")
    print(f"IT TOOK = {time.time()-start_time}")
    return f"output/hero/{prompt.replace(' ', '_')}+.png"