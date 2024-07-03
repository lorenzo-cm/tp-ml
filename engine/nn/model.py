# import torch
# import torch.nn as nn
# import torch.nn.functional as F

# class ResidualBlock(nn.Module):
#     def __init__(self, in_channels, out_channels, kernel_size=3, stride=1, padding=1):
#         super(ResidualBlock, self).__init__()
#         self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding)
#         self.bn1 = nn.BatchNorm2d(out_channels)
#         self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size, stride, padding)
#         self.bn2 = nn.BatchNorm2d(out_channels)
#         self.relu = nn.ReLU(inplace=True)

#     def forward(self, x):
#         residual = x
#         out = self.conv1(x)
#         out = self.bn1(out)
#         out = self.relu(out)
#         out = self.conv2(out)
#         out = self.bn2(out)
#         out += residual
#         out = self.relu(out)
#         return out

# class ChessCNN(nn.Module):
#     def __init__(self, input_shape, num_blocks=5):
#         super(ChessCNN, self).__init__()
#         self.conv = nn.Conv2d(input_shape[0], 256, kernel_size=3, padding=1)
#         self.bn = nn.BatchNorm2d(256)
#         self.relu = nn.ReLU(inplace=True)

#         # Create residual blocks
#         self.res_blocks = nn.ModuleList([ResidualBlock(256, 256) for _ in range(num_blocks)])

#         # Value head
#         self.value_conv = nn.Conv2d(256, 1, kernel_size=1)
#         self.value_bn = nn.BatchNorm2d(1)
#         self.value_fc1 = nn.Linear(8*8, 256)
#         self.value_fc2 = nn.Linear(256, 1)

#         # Policy head
#         self.policy_conv = nn.Conv2d(256, 2, kernel_size=1)
#         self.policy_bn = nn.BatchNorm2d(2)
#         self.policy_fc = nn.Linear(2*8*8, 128)  # Output 128 values (64 for from_square and 64 for to_square)

#     def forward(self, x):
#         x = self.conv(x)
#         x = self.bn(x)
#         x = self.relu(x)

#         for block in self.res_blocks:
#             x = block(x)

#         # Value head
#         vh = self.value_conv(x)
#         vh = self.value_bn(vh)
#         vh = self.relu(vh)
#         vh = vh.view(vh.size(0), -1)
#         vh = self.value_fc1(vh)
#         vh = self.relu(vh)
#         vh = self.value_fc2(vh)
#         vh = vh * 10

#         # Policy head
#         ph = self.policy_conv(x)
#         ph = self.policy_bn(ph)
#         ph = self.relu(ph)
#         ph = ph.view(ph.size(0), -1)
#         ph = self.policy_fc(ph)
        
#         # Split the policy head output into two 8x8 matrices
#         from_square = ph[:, :64].view(-1, 8, 8)
#         to_square = ph[:, 64:].view(-1, 8, 8)
        
#         from_square = F.softmax(from_square.view(ph.size(0), -1), dim=1).view(-1, 8, 8)
#         to_square = F.softmax(to_square.view(ph.size(0), -1), dim=1).view(-1, 8, 8)

#         return vh, (from_square, to_square)

# # Example input shape (channels, board size, board size)
# input_shape = (12, 8, 8)
# model = ChessCNN(input_shape)

# # Print model summary
# print(model)

# batch_size = 1
# input_shape = (12, 8, 8)
# sample_input = torch.randn(batch_size, *input_shape)

# # Instantiate the model
# model = ChessCNN(input_shape)

# # Pass the sample input through the model
# value_head_output, (from_square_output, to_square_output) = model(sample_input)

# # Print the output shapes
# print(f"Value head output shape: {value_head_output.shape}")
# print(f"From square output shape: {from_square_output.shape}")
# print(f"To square output shape: {to_square_output.shape}")

# print(value_head_output[0])
# print(from_square_output[0])
# print(to_square_output[0].shape)
