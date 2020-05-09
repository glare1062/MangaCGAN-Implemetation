import argparse
import time
import torch
import torchvision.utils as vutils
import numpy as np
import matplotlib.pyplot as plt
import json
from model import Generator


def generateImage(load_path='checkpoint/model_final.pth', num_output='1', eye_color='green', hair_color='green', load_json='data/animegan_params.json', entity_name='GeneratedPic'):
    print("called generated image")
    pic_name= entity_name + str((round(time.time() * 1000)))
    # Loads the Genrator modl to Pytorch
    state_dict = torch.load(load_path)

    with open(load_json, 'r') as info_file:
        info = json.load(info_file)
        color2ind = info['color2ind']

    # Makes model run on generator
    device = torch.device("cuda:0" if (torch.cuda.is_available()) else "cpu")
    params = state_dict['params']

    # Creates  gen Network
    genN = Generator(params).to(device)
    # Load the trained generator weights.
    genN.load_state_dict(state_dict['generator'])
    print(genN)
    # Gets latent vector Z from unit normal distribution.
    noise = torch.randn(int(num_output), params['nz'], 1, 1, device=device)
    # To create onehot embeddings for the condition labels.
    onehot = torch.zeros(params['vocab_size'], params['vocab_size'])
    onehot = onehot.scatter_(1,
                             torch.LongTensor([i for i in range(params['vocab_size'])]).view(params['vocab_size'], 1),
                             1).view(params['vocab_size'], params['vocab_size'], 1, 1)

    # Create input conditions vectors.
    input_condition = torch.cat((torch.ones(int(num_output), 1) * color2ind[eye_color],
                                 torch.ones(int(num_output), 1) * color2ind[hair_color]),
                                dim=1).type(torch.LongTensor)

    # Generate the onehot embeddings for the conditions.
    eye_hot = onehot[input_condition[:, 0]].to(device)
    hair_hot = onehot[input_condition[:, 1]].to(device)

    # Turn off gradient calculation to speed up the process.
    with torch.no_grad():
        # Get generated image from the noise vector using the trained generator.
        generated_img = genN(noise, eye_hot, hair_hot).detach().cpu()

    # Display the generated image.
    plt.axis("off")
    img_save = plt.imshow(np.transpose(vutils.make_grid(generated_img, normalize=True), (1, 2, 0)))
    # Saves file as pic name
    img_save.figure.savefig('./Static/' + pic_name)
    return pic_name

if __name__ == '__main__':
    print("called main")
    generateImage()