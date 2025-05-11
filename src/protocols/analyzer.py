from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import numpy as np
from datetime import datetime
from .base import BaseProtocol

class ProtocolAnalyzer(ABC):
    """Abstract base class for protocol analysis."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.protocols: Dict[str, BaseProtocol] = {}

    @abstractmethod
    def analyze_packet(self, packet_data: bytes) -> Dict[str, Any]:
        """Analyze a single packet and return analysis results."""
        pass

    @abstractmethod
    def detect_anomalies(self, packet_sequence: List[bytes]) -> List[Dict[str, Any]]:
        """Detect anomalies in a sequence of packets."""
        pass

class MCPAnalyzer(ProtocolAnalyzer):
    """Machine Control Protocol Analyzer implementation."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.packet_history: List[Dict[str, Any]] = []
        self.anomaly_threshold = config.get('anomaly_threshold', 0.95)

    def analyze_packet(self, packet_data: bytes) -> Dict[str, Any]:
        # Basic packet analysis
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'size': len(packet_data),
            'protocol_type': self._identify_protocol(packet_data),
            'structure': self._analyze_structure(packet_data),
            'metrics': self._calculate_metrics(packet_data)
        }
        
        # Update history
        self.packet_history.append(analysis)
        if len(self.packet_history) > 1000:  # Keep history bounded
            self.packet_history.pop(0)
            
        return analysis

    def detect_anomalies(self, packet_sequence: List[bytes]) -> List[Dict[str, Any]]:
        anomalies = []
        
        for i, packet in enumerate(packet_sequence):
            # Analyze current packet
            current_analysis = self.analyze_packet(packet)
            
            # Compare with historical patterns
            if self._is_anomalous(current_analysis):
                anomalies.append({
                    'packet_index': i,
                    'timestamp': current_analysis['timestamp'],
                    'type': 'anomaly',
                    'details': self._get_anomaly_details(current_analysis)
                })
        
        return anomalies

    def _identify_protocol(self, packet_data: bytes) -> str:
        """Identify the protocol type from packet data."""
        # Protocol identification logic
        header = packet_data[:4]  # Example: using first 4 bytes as header
        
        # Pattern matching for known protocols
        protocol_patterns = {
            b'\x01\x00': 'MCP-1',
            b'\x02\x00': 'MCP-2',
            b'\x03\x00': 'MCP-3'
        }
        
        for pattern, protocol in protocol_patterns.items():
            if header.startswith(pattern):
                return protocol
        
        return 'UNKNOWN'

    def _analyze_structure(self, packet_data: bytes) -> Dict[str, Any]:
        """Analyze the structure of the packet."""
        return {
            'header_size': 4,
            'payload_size': len(packet_data) - 4,
            'checksum_valid': self._verify_checksum(packet_data)
        }

    def _calculate_metrics(self, packet_data: bytes) -> Dict[str, float]:
        """Calculate various metrics from packet data."""
        return {
            'entropy': self._calculate_entropy(packet_data),
            'byte_frequency': self._calculate_byte_frequency(packet_data),
            'pattern_score': self._calculate_pattern_score(packet_data)
        }

    def _is_anomalous(self, analysis: Dict[str, Any]) -> bool:
        """Determine if the analyzed packet is anomalous."""
        if not self.packet_history:
            return False
            
        # Compare metrics with historical averages
        historical_metrics = [h['metrics'] for h in self.packet_history[-100:]]
        current_metrics = analysis['metrics']
        
        # Calculate z-scores for each metric
        z_scores = {}
        for metric in current_metrics:
            historical_values = [h[metric] for h in historical_metrics]
            mean = np.mean(historical_values)
            std = np.std(historical_values) or 1.0  # Avoid division by zero
            z_scores[metric] = abs((current_metrics[metric] - mean) / std)
        
        # Consider it anomalous if any z-score exceeds threshold
        return any(z > self.anomaly_threshold for z in z_scores.values())

    def _get_anomaly_details(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed information about detected anomaly."""
        return {
            'protocol': analysis['protocol_type'],
            'metrics': analysis['metrics'],
            'structure_issues': self._identify_structure_issues(analysis)
        }

    def _verify_checksum(self, packet_data: bytes) -> bool:
        """Verify packet checksum."""
        # Simple checksum verification example
        if len(packet_data) < 4:
            return False
        return sum(packet_data[:-4]) % 256 == packet_data[-1]

    def _calculate_entropy(self, data: bytes) -> float:
        """Calculate Shannon entropy of the data."""
        if not data:
            return 0.0
        
        # Calculate frequency of each byte value
        freq = np.bincount(np.frombuffer(data, dtype=np.uint8)) / len(data)
        # Remove zero frequencies to avoid log(0)
        freq = freq[freq > 0]
        # Calculate entropy
        return -np.sum(freq * np.log2(freq))

    def _calculate_byte_frequency(self, data: bytes) -> float:
        """Calculate normalized byte frequency distribution."""
        if not data:
            return 0.0
        
        freq = np.bincount(np.frombuffer(data, dtype=np.uint8))
        return float(np.max(freq)) / len(data)

    def _calculate_pattern_score(self, data: bytes) -> float:
        """Calculate pattern regularity score."""
        if len(data) < 2:
            return 0.0
        
        # Calculate differences between consecutive bytes
        diffs = np.diff(np.frombuffer(data, dtype=np.uint8))
        # Calculate standard deviation of differences
        return float(np.std(diffs))

    def _identify_structure_issues(self, analysis: Dict[str, Any]) -> List[str]:
        """Identify any issues in packet structure."""
        issues = []
        
        if not analysis['structure']['checksum_valid']:
            issues.append('Invalid checksum')
            
        if analysis['structure']['payload_size'] == 0:
            issues.append('Empty payload')
            
        if analysis['protocol_type'] == 'UNKNOWN':
            issues.append('Unrecognized protocol')
            
        return issues