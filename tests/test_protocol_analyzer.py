import unittest
import numpy as np
from datetime import datetime
from src.protocols.analyzer import MCPAnalyzer
from src.data.processor import DataProcessor

class TestMCPAnalyzer(unittest.TestCase):
    def setUp(self):
        self.config = {
            'anomaly_threshold': 0.95
        }
        self.analyzer = MCPAnalyzer(config=self.config)
        self.processor = DataProcessor()

    def test_protocol_identification(self):
        # Test MCP-1 protocol identification
        mcp1_packet = b'\x01\x00\x00\x00payload'
        analysis = self.analyzer.analyze_packet(mcp1_packet)
        self.assertEqual(analysis['protocol_type'], 'MCP-1')

        # Test unknown protocol
        unknown_packet = b'\xFF\xFF\x00\x00payload'
        analysis = self.analyzer.analyze_packet(unknown_packet)
        self.assertEqual(analysis['protocol_type'], 'UNKNOWN')

    def test_packet_structure_analysis(self):
        packet = b'\x01\x00\x00\x00payload\x00'
        analysis = self.analyzer.analyze_packet(packet)
        structure = analysis['structure']

        self.assertEqual(structure['header_size'], 4)
        self.assertEqual(structure['payload_size'], len(packet) - 4)

    def test_anomaly_detection(self):
        # Generate normal packets
        normal_packets = [
            b'\x01\x00\x00\x00normal\x00' for _ in range(10)
        ]

        # Generate anomalous packet
        anomalous_packet = b'\x01\x00\x00\x00' + bytes([255] * 100)

        # Add normal packets to history
        for packet in normal_packets:
            self.analyzer.analyze_packet(packet)

        # Test anomaly detection
        anomalies = self.analyzer.detect_anomalies([anomalous_packet])
        self.assertTrue(len(anomalies) > 0)

    def test_metric_calculation(self):
        packet = b'\x01\x00\x00\x00test_data\x00'
        analysis = self.analyzer.analyze_packet(packet)
        metrics = analysis['metrics']

        self.assertIn('entropy', metrics)
        self.assertIn('byte_frequency', metrics)
        self.assertIn('pattern_score', metrics)

        self.assertTrue(0 <= metrics['entropy'] <= 8)  # Max entropy for bytes
        self.assertTrue(0 <= metrics['byte_frequency'] <= 1)

    def test_data_processor_integration(self):
        # Test integration between analyzer and data processor
        raw_data = [
            {
                'protocol_type': 'MCP-1',
                'timestamp': datetime.now(),
                'packet_size': 100,
                'payload': {'data': 'test'}
            }
            for _ in range(5)
        ]

        # Process data
        processed_data = self.processor.preprocess_protocol_data(raw_data)
        self.assertIsNotNone(processed_data)
        self.assertFalse(processed_data.empty)

    def test_checksum_verification(self):
        # Test valid checksum
        valid_packet = bytes([1, 2, 3, 4]) + bytes([10])
        self.assertTrue(self.analyzer._verify_checksum(valid_packet))

        # Test invalid checksum
        invalid_packet = bytes([1, 2, 3, 4]) + bytes([0])
        self.assertFalse(self.analyzer._verify_checksum(invalid_packet))

    def test_entropy_calculation(self):
        # Test uniform distribution (maximum entropy)
        uniform_data = bytes(range(256))
        entropy = self.analyzer._calculate_entropy(uniform_data)
        self.assertAlmostEqual(entropy, 8.0, places=1)

        # Test single value (minimum entropy)
        single_value = bytes([0] * 256)
        entropy = self.analyzer._calculate_entropy(single_value)
        self.assertAlmostEqual(entropy, 0.0, places=1)

if __name__ == '__main__':
    unittest.main()