# Mypy-boto3 rekognition submodule

Provides type annotations for boto3 rekognition service

## Installation

```bash
pip install mypy-boto3[rekognition]
```

## Usage

```python
import boto3
from mypy_boto3.rekognition import Client, ServiceResource

client: Client = boto3.client("rekognition")
resource: ServiceResource = boto3.resource("rekognition")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

