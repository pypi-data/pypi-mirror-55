from .base import CNN
from ...modules.residual import Residual


class ResNet(CNN):
  channels = None

  def __init__(self):
    super(ResNet, self).__init__()


