'''
    This project demonstrates the use of a pre-trained image diffusion model
for generating an anime-style image based on textual prompts.
Here's a summary of the key functionalities:


-Image Diffusion with Diffusers:
Utilizes the DiffusionPipeline from the diffusers library to generate images based on textual prompts.

-Model Loading
Loads a pre-trained anime image diffusion model ("Ojimi/anime-kawai-diffusion").

-GPU Acceleration:
Moves the diffusion pipeline to the CUDA device for GPU acceleration using the .to("cuda") method.

-Textual Prompt:
Specifies a textual prompt describing the desired characteristics of the generated image.

-Image Generation:
Uses the diffusion pipeline to generate an anime-style image based on the provided prompt.
'''
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained("Ojimi/anime-kawai-diffusion")
pipe = pipe.to("cuda")

prompt = "1girl, animal ears, long hair, solo, cat ears, choker, bare shoulders, red eyes, fang, looking at viewer, animal ear fluff, upper body, black hair, blush, closed mouth, off shoulder, bangs, bow, collarbone"
image = pipe(prompt, negative_prompt="lowres, bad anatomy").images[0]
