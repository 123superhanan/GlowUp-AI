import torch
import torch.nn.functional as F
from PIL import Image
# Import internal modular components
from models.cnn import CNN
from utils.classes import SKIN_TONE_CLASSES
from utils.preprocess import preprocess_image