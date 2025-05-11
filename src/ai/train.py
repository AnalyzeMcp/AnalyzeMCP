import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from transformers import AutoModel, AutoTokenizer
from typing import List, Dict, Any
from .models import ProtocolAnalyzer

class TrainingConfig:
    def __init__(
        self,
        batch_size: int = 32,
        learning_rate: float = 1e-4,
        epochs: int = 10,
        device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
    ):
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.device = device

class ModelTrainer:
    def __init__(self, model: ProtocolAnalyzer, config: TrainingConfig):
        self.model = model.to(config.device)
        self.config = config
        self.optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
        self.criterion = nn.CrossEntropyLoss()

    def train_epoch(self, dataloader: DataLoader) -> float:
        self.model.train()
        total_loss = 0.0
        
        for batch in dataloader:
            self.optimizer.zero_grad()
            inputs, labels = self._prepare_batch(batch)
            outputs = self.model(inputs)
            loss = self.criterion(outputs, labels)
            loss.backward()
            self.optimizer.step()
            total_loss += loss.item()

        return total_loss / len(dataloader)

    def evaluate(self, dataloader: DataLoader) -> Dict[str, float]:
        self.model.eval()
        total_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            for batch in dataloader:
                inputs, labels = self._prepare_batch(batch)
                outputs = self.model(inputs)
                loss = self.criterion(outputs, labels)
                total_loss += loss.item()

                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        return {
            'loss': total_loss / len(dataloader),
            'accuracy': correct / total
        }

    def _prepare_batch(self, batch: Dict[str, torch.Tensor]) -> tuple:
        inputs = {k: v.to(self.config.device) for k, v in batch.items() if k != 'labels'}
        labels = batch['labels'].to(self.config.device)
        return inputs, labels

    def save_model(self, path: str):
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
        }, path)

    def load_model(self, path: str):
        checkpoint = torch.load(path)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])