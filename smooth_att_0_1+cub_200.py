# -*- coding: utf-8 -*-
"""Smooth_Att_0.1+CUB_200.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1S_wvOyeLvdeUad6L81CIdIarHCwaa9Jf
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torchvision import models, transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import os
import pandas as pd
import numpy as np

# google drive mount
from google.colab import drive
drive.mount('/content/drive')

!unzip '/content/drive/MyDrive/Smooth Attention/input/CUB_200.zip'

import tarfile

# Untar CUB_200_2011.tgz
with tarfile.open('/content/CUB_200_2011.tgz', 'r:gz') as tar_ref:
    tar_ref.extractall('CUB_200_2011')

# Untar segmentations.tgz
with tarfile.open('/content/segmentations.tgz', 'r:gz') as tar_ref:
    tar_ref.extractall('segmentations')

# Constants
BATCH_SIZE = 8
NUM_EPOCHS = 20
LEARNING_RATE = 0.0001

class CUB200Dataset(Dataset):
    def __init__(self, root_dir, segmentations_dir, transform=None):
        self.root_dir = root_dir
        self.segmentations_dir = segmentations_dir
        self.transform = transform
        self.images = []
        self.segmentations = []

        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.jpg'):
                    image_path = os.path.join(root, file)
                    seg_path = os.path.join(segmentations_dir, root.split('/')[-1], file.replace('.jpg', '.png'))
                    if os.path.exists(seg_path):
                        self.images.append(image_path)
                        self.segmentations.append(seg_path)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_path = self.images[idx]
        seg_path = self.segmentations[idx]

        image = Image.open(img_path).convert("RGB")
        segmentation = Image.open(seg_path).convert("L")

        if self.transform:
            image = self.transform(image)
            segmentation = self.transform(segmentation)

        return image, segmentation

# Data preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# Create datasets
dataset = CUB200Dataset(
    root_dir='/content/CUB_200_2011/CUB_200_2011/images',
    segmentations_dir='/content/segmentations/segmentations',
    transform=transform
)

# Split dataset into train and test
train_size = int(0.8 * len(dataset))
test_size = len(dataset) - train_size
train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

class SmoothAttention(nn.Module):
    def __init__(self, in_channels, out_channels, threshold=0.1):
        super(SmoothAttention, self).__init__()
        self.query = nn.Conv2d(in_channels, out_channels, kernel_size=1)
        self.key = nn.Conv2d(in_channels, out_channels, kernel_size=1)
        self.value = nn.Conv2d(in_channels, out_channels, kernel_size=1)
        self.gamma = nn.Parameter(torch.zeros(1))
        self.threshold = threshold

    def forward(self, x):
        batch_size, C, H, W = x.size()

        proj_query = self.query(x).view(batch_size, -1, H * W).permute(0, 2, 1)
        proj_key = self.key(x).view(batch_size, -1, H * W)
        energy = torch.bmm(proj_query, proj_key)
        attention = F.softmax(energy, dim=-1)

        attention_reshaped = attention.view(batch_size, H, W, H * W)
        attention_padded = F.pad(attention_reshaped, (0, 0, 1, 1, 1, 1), mode='replicate')

        chebyshev_distances = []
        for i in range(3):
            for j in range(3):
                if i == 1 and j == 1:
                    continue
                neighbor = attention_padded[:, i:i + H, j:j + W, :]
                distance = torch.max(torch.abs(neighbor - attention_reshaped), dim=-1)[0]
                chebyshev_distances.append(distance)

        chebyshev_distances = torch.stack(chebyshev_distances, dim=-1)
        max_chebyshev_distance = torch.max(chebyshev_distances, dim=-1)[0]

        smoothing_mask = (max_chebyshev_distance > self.threshold).float()

        # # Debug: print tensor shapes
        # print(f"attention_reshaped shape: {attention_reshaped.shape}")
        # print(f"attention_padded shape: {attention_padded.shape}")
        # print(f"smoothing_mask shape: {smoothing_mask.shape}")

        # Calculate the smoothed attention correctly
        smoothed_attention = torch.stack([
            attention_padded[:, i:i + H, j:j + W, :]
            for i in range(3) for j in range(3)
            if not (i == 1 and j == 1)
        ], dim=0).mean(dim=0)

        # Ensure the broadcasted dimensions match
        smoothing_mask = smoothing_mask.unsqueeze(-1).expand_as(attention_reshaped)

        final_attention = (1 - smoothing_mask) * attention_reshaped + smoothing_mask * smoothed_attention

        final_attention = final_attention.view(batch_size, H * W, H * W)

        proj_value = self.value(x).view(batch_size, -1, H * W)
        out = torch.bmm(proj_value, final_attention.permute(0, 2, 1))
        out = out.view(batch_size, C, H, W)

        out = self.gamma * out + x
        return out

class SmoothAttentionUNet(nn.Module):
    def __init__(self, num_classes):
        super(SmoothAttentionUNet, self).__init__()
        self.encoder = models.resnet18(pretrained=True)
        self.encoder = nn.Sequential(*list(self.encoder.children())[:-2])
        self.smooth_attention = SmoothAttention(512, 512)
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(512, 256, kernel_size=2, stride=2),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(64, 32, kernel_size=2, stride=2),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(32, num_classes, kernel_size=2, stride=2)
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.smooth_attention(x)
        x = self.decoder(x)
        return x

# Create the model and move it to the device
num_classes = 1  # Binary segmentation (background vs bird)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SmoothAttentionUNet(num_classes=num_classes).to(device)

# Print model summary
print(model)

# Verify model is on the correct device
print(f"Model is on device: {next(model.parameters()).device}")

criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=5, verbose=True)

import torch
import torch.nn.functional as F
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def compute_iou(pred, target):
    intersection = torch.logical_and(pred, target).float().sum((1, 2))
    union = torch.logical_or(pred, target).float().sum((1, 2))
    iou = (intersection + 1e-6) / (union + 1e-6)
    return iou.mean().item()

def compute_dice(pred, target):
    intersection = torch.logical_and(pred, target).float().sum((1, 2))
    dice = (2. * intersection + 1e-6) / (pred.float().sum((1, 2)) + target.float().sum((1, 2)) + 1e-6)
    return dice.mean().item()

def compute_metrics(pred, target):
    pred_flat = pred.view(-1).cpu().numpy()
    target_flat = target.view(-1).cpu().numpy()

    acc = accuracy_score(target_flat, pred_flat)
    precision = precision_score(target_flat, pred_flat)
    recall = recall_score(target_flat, pred_flat)
    f1 = f1_score(target_flat, pred_flat)

    return acc, precision, recall, f1

from torchvision.transforms.functional import resize

def train(model, train_loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0

    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)

        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    epoch_loss = running_loss / len(train_loader)
    return epoch_loss

def compute_metrics(pred, target):
    pred_flat = pred.view(-1).cpu().numpy()
    target_flat = target.view(-1).cpu().numpy()

    acc = accuracy_score(target_flat, pred_flat)
    precision = precision_score(target_flat, pred_flat, zero_division=0)
    recall = recall_score(target_flat, pred_flat, zero_division=0)
    f1 = f1_score(target_flat, pred_flat, zero_division=0)

    return acc, precision, recall, f1

def evaluate(model, loader, device):
    model.eval()
    iou_list = []
    dice_list = []
    accuracy_list = []
    precision_list = []
    recall_list = []
    f1_list = []

    with torch.no_grad():
        for data in loader:
            inputs, targets = data
            inputs, targets = inputs.to(device), targets.to(device)

            outputs = model(inputs)
            preds = torch.sigmoid(outputs) > 0.5  # Convert to binary mask

            iou = compute_iou(preds, targets)
            dice = compute_dice(preds, targets)
            acc, precision, recall, f1 = compute_metrics(preds.int(), targets.int())  # Ensure binary masks

            iou_list.append(iou)
            dice_list.append(dice)
            accuracy_list.append(acc)
            precision_list.append(precision)
            recall_list.append(recall)
            f1_list.append(f1)

    avg_iou = sum(iou_list) / len(iou_list)
    avg_dice = sum(dice_list) / len(dice_list)
    avg_accuracy = sum(accuracy_list) / len(accuracy_list)
    avg_precision = sum(precision_list) / len(precision_list)
    avg_recall = sum(recall_list) / len(recall_list)
    avg_f1 = sum(f1_list) / len(f1_list)

    return avg_iou, avg_dice, avg_accuracy, avg_precision, avg_recall, avg_f1

# Training loop
best_metric = float('-inf')
for epoch in range(NUM_EPOCHS):
    train_loss = train(model, train_loader, criterion, optimizer, device)
    test_metrics = evaluate(model, test_loader, device)  # Remove 'criterion' from here

    # Unpack the metrics returned by the evaluate function
    avg_iou, avg_dice, avg_accuracy, avg_precision, avg_recall, avg_f1 = test_metrics

    # Since the evaluate function does not return the test loss, use avg_iou or other metrics for comparison
    if avg_iou > best_metric:
        best_metric = avg_iou
        torch.save(model.state_dict(), 'best_model.pth')

    print(f'Epoch {epoch+1}/{NUM_EPOCHS}, Train Loss: {train_loss:.4f}, Test IoU: {avg_iou:.4f}, Test Dice: {avg_dice:.4f}, Test Accuracy: {avg_accuracy:.4f}, Test Precision: {avg_precision:.4f}, Test Recall: {avg_recall:.4f}, Test F1: {avg_f1:.4f}')