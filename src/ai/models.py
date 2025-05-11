from typing import Dict, List, Optional
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, global_mean_pool
from transformers import AutoModel, AutoTokenizer

class PricePredictor(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int):
        super(PricePredictor, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, batch_first=True)
        self.attention = nn.MultiheadAttention(hidden_dim, num_heads=8)
        self.fc = nn.Linear(hidden_dim, output_dim)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        lstm_out, _ = self.lstm(x)
        attn_out, _ = self.attention(lstm_out, lstm_out, lstm_out)
        return self.fc(attn_out[:, -1, :])

class BehaviorAnalyzer(nn.Module):
    def __init__(self, node_features: int, hidden_channels: int):
        super(BehaviorAnalyzer, self).__init__()
        self.conv1 = GCNConv(node_features, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.fc = nn.Linear(hidden_channels, 1)
    
    def forward(self, x: torch.Tensor, edge_index: torch.Tensor, batch: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.conv1(x, edge_index))
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.conv2(x, edge_index)
        x = global_mean_pool(x, batch)
        return torch.sigmoid(self.fc(x))

class RiskAssessor(nn.Module):
    def __init__(self, input_features: int, hidden_dim: int):
        super(RiskAssessor, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_features, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1)
        )
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return torch.sigmoid(self.layers(x))

class ModelManager:
    def __init__(self, config: Dict):
        self.price_predictor = PricePredictor(
            input_dim=config['price_input_dim'],
            hidden_dim=config['price_hidden_dim'],
            output_dim=config['price_output_dim']
        )
        self.behavior_analyzer = BehaviorAnalyzer(
            node_features=config['behavior_node_features'],
            hidden_channels=config['behavior_hidden_channels']
        )
        self.risk_assessor = RiskAssessor(
            input_features=config['risk_input_features'],
            hidden_dim=config['risk_hidden_dim']
        )
    
    def predict_price(self, data: torch.Tensor) -> torch.Tensor:
        return self.price_predictor(data)
    
    def analyze_behavior(self, x: torch.Tensor, edge_index: torch.Tensor, batch: torch.Tensor) -> torch.Tensor:
        return self.behavior_analyzer(x, edge_index, batch)
    
    def assess_risk(self, features: torch.Tensor) -> torch.Tensor:
        return self.risk_assessor(features)