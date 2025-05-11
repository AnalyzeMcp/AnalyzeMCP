# AnalyzeMCP API Documentation

This document provides detailed information about the AnalyzeMCP API endpoints, request/response formats, and usage examples.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication for local development. For production deployment, implement appropriate authentication mechanisms.

## Endpoints

### Analyze Protocol Data

```http
POST /analyze
```

Analyze protocol data and receive insights and recommendations.

#### Request Body

```json
{
  "data": [
    {
      "protocol_type": "string",
      "timestamp": "2023-01-01T00:00:00Z",
      "packet_size": 0,
      "payload": {
        "additional_field": "value"
      }
    }
  ]
}
```

#### Response

```json
{
  "analysis": [
    {
      "metric_name": "string",
      "value": 0,
      "change": 0,
      "data": [
        {
          "x": "string",
          "y": 0
        }
      ]
    }
  ],
  "insights": [
    "string"
  ],
  "recommendations": [
    "string"
  ]
}
```

### Health Check

```http
GET /health
```

Check the health status of the API service.

#### Response

```json
{
  "status": "healthy",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

### Get Metrics

```http
GET /metrics
```

Retrieve current analysis metrics and statistics.

#### Response

```json
{
  "total_packets_analyzed": 0,
  "anomalies_detected": 0,
  "protocol_distribution": {
    "MCP-1": 0,
    "MCP-2": 0,
    "MCP-3": 0
  },
  "average_packet_size": 0
}
```

## Error Handling

The API uses standard HTTP status codes for error responses:

- `200`: Success
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

Error Response Format:

```json
{
  "detail": "Error message description"
}
```

## Rate Limiting

Currently, no rate limiting is implemented for local development. For production deployment, consider implementing appropriate rate limiting mechanisms.

## Examples

### cURL

```bash
# Analyze Protocol Data
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "protocol_type": "MCP-1",
        "timestamp": "2023-01-01T00:00:00Z",
        "packet_size": 100,
        "payload": {
          "command": "START",
          "parameters": {"speed": 50}
        }
      }
    ]
  }'

# Health Check
curl http://localhost:8000/health

# Get Metrics
curl http://localhost:8000/metrics
```

### Python

```python
import requests
import json
from datetime import datetime

# Analyze Protocol Data
response = requests.post(
    'http://localhost:8000/analyze',
    json={
        'data': [
            {
                'protocol_type': 'MCP-1',
                'timestamp': datetime.now().isoformat(),
                'packet_size': 100,
                'payload': {
                    'command': 'START',
                    'parameters': {'speed': 50}
                }
            }
        ]
    }
)

result = response.json()
print(json.dumps(result, indent=2))
```

## Websocket Support

WebSocket support for real-time protocol analysis will be added in future versions.

## Version History

- v1.0.0 - Initial release
  - Basic protocol analysis
  - Insights and recommendations
  - Metrics tracking

## Support

For issues and feature requests, please use the GitHub issue tracker.