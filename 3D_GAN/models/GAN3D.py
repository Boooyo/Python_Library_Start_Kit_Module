import torch
import torch.nn as nn
from torchsummary import summary

class Discriminator(nn.Module):
    def __init__(self, in_channels=1, dim=64, out_conv_channels=512):
        super(Discriminator, self).__init__()
        self.out_conv_channels = out_conv_channels
        self.out_dim = dim // 16
        
        conv_channels = [out_conv_channels // 8, out_conv_channels // 4, out_conv_channels // 2]
        
        self.convolutions = nn.Sequential(
            *[self._conv_block(in_channels if i == 0 else conv_channels[i-1], out_channel)
              for i, out_channel in enumerate(conv_channels + [out_conv_channels])]
        )
        
        self.out = nn.Sequential(
            nn.Linear(out_conv_channels * self.out_dim ** 3, 1),
            nn.Sigmoid(),
        )

    def _conv_block(self, in_channels, out_channels):
        return nn.Sequential(
            nn.Conv3d(in_channels, out_channels, kernel_size=4, stride=2, padding=1, bias=False),
            nn.BatchNorm3d(out_channels),
            nn.LeakyReLU(0.2, inplace=True)
        )

    def forward(self, x):
        x = self.convolutions(x)
        x = x.view(-1, self.out_conv_channels * self.out_dim ** 3)
        return self.out(x)


class Generator(nn.Module):
    def __init__(self, in_channels=512, out_dim=64, out_channels=1, noise_dim=200, activation="sigmoid"):
        super(Generator, self).__init__()
        self.in_dim = out_dim // 16
        
        conv_out_channels = [in_channels // 2 ** i for i in range(3)]
        
        self.linear = nn.Linear(noise_dim, in_channels * self.in_dim ** 3)
        
        self.convolutions = nn.Sequential(
            *[self._deconv_block(in_channels if i == 0 else conv_out_channels[i-1], out_channel)
              for i, out_channel in enumerate(conv_out_channels + [out_channels])]
        )
        
        self.out = nn.Sigmoid() if activation == "sigmoid" else nn.Tanh()

    def _deconv_block(self, in_channels, out_channels):
        return nn.Sequential(
            nn.ConvTranspose3d(in_channels, out_channels, kernel_size=(4, 4, 4), stride=2, padding=1, bias=False),
            nn.BatchNorm3d(out_channels),
            nn.ReLU(inplace=True)
        )

    def project(self, x):
        return x.view(-1, self.in_channels, self.in_dim, self.in_dim, self.in_dim)

    def forward(self, x):
        x = self.linear(x)
        x = self.project(x)
        return self.out(self.convolutions(x))


def test_gan3d():
    noise_dim = 200
    in_channels = 512
    dim = 64  # cube volume
    model_generator = Generator(in_channels=in_channels, out_dim=dim, out_channels=1, noise_dim=noise_dim)
    noise = torch.rand(1, noise_dim)
    generated_volume = model_generator(noise)
    print("Generator output shape:", generated_volume.shape)
    
    model_discriminator = Discriminator(in_channels=1, dim=dim, out_conv_channels=in_channels)
    out = model_discriminator(generated_volume)
    print("Discriminator output:", out)
    
    summary(model_generator, (1, noise_dim))
    summary(model_discriminator, (1, 64, 64, 64))


test_gan3d()
