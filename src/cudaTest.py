import torch
import os
print(torch.__version__)
print(torch.version.cuda)
print(torch.cuda.is_available())

from urllib.request import getproxies
print(getproxies())

map = torch.load("E:\Github\midi-emotion\output\continuous_concat\mappings.pt")
print("..")

torch.save([1,2], "../output/a.pt")

s = "adfasf"
print(os.path.join("../data", s[0], s + ".pt"))