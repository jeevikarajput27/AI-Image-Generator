import tkinter as tk
import customtkinter as ctk
import torch
from diffusers import StableDiffusionPipeline
from PIL import ImageTk, Image
from torch import autocast
from contextlib import nullcontext
from authtoken import auth_token


app = tk.Tk()
app.geometry("532x532")
app.title("Stable Diffusion IG")
ctk.set_appearance_mode("dark")


prompt = ctk.CTkEntry(
    app,
    height=40,
    width=500,
    text_color="black",
    fg_color="white"
)
prompt.place(x=10, y=10)


lmain = ctk.CTkLabel(app, height=512, width=512)
lmain.place(x=10, y=110)


modelid = "CompVis/stable-diffusion-v1-4"
device = "cuda" if torch.cuda.is_available() else "cpu"


pipe = StableDiffusionPipeline.from_pretrained(
    modelid,
    revision="fp16" if torch.cuda.is_available() else "main",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    use_auth_token=auth_token
)
pipe.to(device)

def generate():
    try:
        with autocast(device) if torch.cuda.is_available() else nullcontext():
            
            result = pipe(prompt.get(), guidance_scale=8.5)
            image = result.images[0]
        
        
        img = ImageTk.PhotoImage(image)
        image.save('Generated_Image.png')
        lmain.configure(image=img)
        lmain.image = img  
    except Exception as e:
        print(f"Error generating image: {e}")


trigger = ctk.CTkButton(
    master=app,
    height=40,
    width=120,
    text_color="white",
    fg_color="blue",
    command=generate
)
trigger.configure(text="Generate")
trigger.place(x=206, y=60)


app.mainloop()
