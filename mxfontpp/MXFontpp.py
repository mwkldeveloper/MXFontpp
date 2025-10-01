from typing import List
from .models import Generator
from PIL import Image
import torch
from sconf import Config
import torchvision.transforms.v2 as v2
from torchvision import transforms
import numpy as np
from .utils.visualize import refine, tensor_to_image


class MXFontpp:
    def __init__(self, cfg: Config, weight_path: str, img_size=128):
        g_kwargs = cfg.get('g_args', {})

        if torch.cuda.is_available():
            self.device = 'cuda'
        elif torch.backends.mps.is_available():
            self.device = 'mps'
        else:
            self.device = 'cpu'
        print("Using", self.device.upper())

        self.__preprocess__ = v2.Compose([
            v2.Resize((img_size, img_size)),
            v2.ToImage(),
            v2.Grayscale(num_output_channels=1),
            v2.ToDtype(torch.float32, scale=True),              
            v2.Normalize([0.5], [0.5]), # Map to (-1, 1)
        ])

        # self.__preprocess__  = transforms.Compose([
        #     transforms.Resize((128, 128)), 
        #     transforms.Grayscale(num_output_channels=1), 
        #     transforms.ToTensor(), 
        #     transforms.Normalize([0.5], [0.5])
        #     ])

        self.gen = Generator(1, cfg.C, 1, **g_kwargs).to(self.device).eval()

        if weight_path is not None:
            self.load_weight(weight_path)

    def load_weight(self, weight_path, weights_only=False):
        weight = torch.load(weight_path, weights_only=weights_only)
        if "generator_ema" in weight:
            weight = weight["generator_ema"]
        self.gen.load_state_dict(weight)

    def preprocess(self, x):
        return torch.Tensor(np.array(self.__preprocess__(x)))

    def get_style_facts(self, ref_batches):
        style_facts = {}
        for batch in ref_batches:
            style_fact = self.gen.factorize(self.gen.encode(batch), 0)
            for k in style_fact:
                style_facts.setdefault(k, []).append(style_fact[k])
        style_facts = {k: torch.cat(v).mean(0, keepdim=True) for k, v in style_facts.items()}
        return style_facts

    def gen_sample(self, 
                    source_imgs: torch.Tensor, 
                    ref_imgs: torch.Tensor, 
                    return_pil_image: bool = False) -> list[Image.Image] | list[torch.Tensor]:
        ref_batches = torch.split(ref_imgs, 3)
        style_facts = self.get_style_facts(ref_batches)

        source_imgs = source_imgs.to(self.device)
        ref_imgs = ref_imgs.to(self.device)
        # replicate style facts for each source image
        style_facts = {
            k: v.repeat(source_imgs.shape[0], *([1] * (v.dim() - 1))) for k, v in style_facts.items()
        }
        print("Generating sample...")
        
        encode_img = self.gen.encode(source_imgs)
        char_facts = self.gen.factorize(encode_img, 1)
        gen_feats = self.gen.defactorize([style_facts, char_facts])
        generated_imgs = self.gen.decode(gen_feats).detach().cpu()
        generated_imgs = refine(generated_imgs)
        generated_imgs = [tensor_to_image(img) if return_pil_image else img for img in generated_imgs]
        return generated_imgs

if __name__ == "__main__":
    # 當直接運行此文件時，需要將當前目錄添加到 Python 路徑
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    img_size = 128
    cfg = Config("../cfgs/eval.yaml", default="../cfgs/defaults.yaml")
    mxfontpp = MXFontpp(cfg, weight_path="../results/340000.pth")
    # Tensor of source Images
    x_src = torch.randn(10,1,img_size,img_size).to('cuda') 
    # Tensor of reference Images
    x_ref = torch.randn(10,1,img_size,img_size).to('cuda')
    out = mxfontpp.gen_sample(x_src, x_ref, return_pil_image=True)
    print(out)  