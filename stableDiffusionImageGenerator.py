
from diffusers import StableDiffusionPipeline
import torch
import time
start_time = time.time()
my_token = "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"
# get your token at https://huggingface.co/settings/tokens
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", use_auth_token=my_token)
pipe.to("cpu")

def create_hero_image(prompt:str):
    image = pipe(prompt, height=600, width=1048).images[0]
    image.save(f"output/hero/gpt_{prompt.replace(' ', '_')[:8]}+.png")
    print(f"IT TOOK = {time.time()-start_time}")
    # Returning the place where the hero image will be in the nextjs template(:TODO change the directory structure for the current proj)
    return f"assets/images/posts/hero/gpt_{prompt.replace(' ', '_')[:8]}+.png"