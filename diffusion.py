#from diffusers import DiffusionPipeline, EulerDiscreteScheduler, DPMSolverMultistepScheduler
from diffusers import DiffusionPipeline, EulerDiscreteScheduler, DPMSolverMultistepScheduler, StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
import torch
import os

repo_id = "../stable-diffusion-v1-5"
#repo_id = "./dreamlike-photoreal-2.0"
#repo_id = "./abyss"

scheduler = UniPCMultistepScheduler.from_pretrained(repo_id, subfolder="scheduler")

stable_diffusion = DiffusionPipeline.from_pretrained(repo_id, scheduler=scheduler, safety_checker=None)

stable_diffusion.to("cuda")
generator = torch.Generator(device="cuda").manual_seed(1)

#image = stable_diffusion("blond hair, highly detailed, 8k, symmetrical face, beautiful, photorealistic", generator=generator).images[0]
with open('classes.txt', 'r') as file:
    lines = file.readlines()

    for i, line in enumerate(lines, start=0):
        if i < 1:
            continue
        number, name = line.split(maxsplit=1)
        os.makedirs(number, exist_ok=True)


        for i in range(1300):
            generator = torch.Generator(device="cuda").manual_seed(i)
            image = stable_diffusion(f'a photo of a {name}', negative_prompt="", generator=generator, num_inference_steps=20).images[0]
            image.save(f'{number}/seed_{i}.jpg')

