import torch
import torch.nn as nn
import torch.optim as optim

value_loss_fn = nn.MSELoss()  # Value head loss
policy_loss_fn = nn.CrossEntropyLoss()  # Policy head loss

input_shape = (12, 8, 8)
