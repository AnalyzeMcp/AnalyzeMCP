import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.preprocessing import StandardScaler
from .pipeline import DataPipeline

class DataProcessor:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.scaler = StandardScaler()
        self.pipeline = DataPipeline()

    def preprocess_protocol_data(self, raw_data: List[Dict[str, Any]]) -> pd.DataFrame:
        """Preprocess raw protocol data into structured format."""
        # Convert raw data to DataFrame
        df = pd.DataFrame(raw_data)
        
        # Basic cleaning
        df = self._clean_data(df)
        
        # Extract features
        features = self._extract_features(df)
        
        # Normalize numerical features
        numerical_cols = features.select_dtypes(include=[np.number]).columns
        features[numerical_cols] = self.scaler.fit_transform(features[numerical_cols])
        
        return features

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean raw data by handling missing values and outliers."""
        # Handle missing values
        df = df.fillna({
            'numeric_fields': 0,
            'categorical_fields': 'unknown',
            'timestamp_fields': pd.Timestamp.now()
        })
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle outliers using IQR method for numerical columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df = df[~((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR)))]
        
        return df

    def _extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract relevant features from cleaned data."""
        features = pd.DataFrame()
        
        # Time-based features
        if 'timestamp' in df.columns:
            features['hour'] = pd.to_datetime(df['timestamp']).dt.hour
            features['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
        
        # Protocol-specific features
        if 'protocol_type' in df.columns:
            # One-hot encode protocol types
            protocol_dummies = pd.get_dummies(df['protocol_type'], prefix='protocol')
            features = pd.concat([features, protocol_dummies], axis=1)
        
        # Statistical features
        if 'packet_size' in df.columns:
            features['avg_packet_size'] = df['packet_size'].rolling(window=10).mean()
            features['packet_size_std'] = df['packet_size'].rolling(window=10).std()
        
        # Add custom features through pipeline
        pipeline_features = self.pipeline.process(df)
        features = pd.concat([features, pipeline_features], axis=1)
        
        return features

    def prepare_training_data(self, features: pd.DataFrame, labels: List[int]) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare features and labels for model training."""
        X = features.values
        y = np.array(labels)
        
        return X, y

    def save_processor_state(self, path: str):
        """Save processor state including scaler parameters."""
        import joblib
        joblib.dump({
            'scaler': self.scaler,
            'config': self.config
        }, path)

    def load_processor_state(self, path: str):
        """Load processor state from file."""
        import joblib
        state = joblib.load(path)
        self.scaler = state['scaler']
        self.config = state['config']