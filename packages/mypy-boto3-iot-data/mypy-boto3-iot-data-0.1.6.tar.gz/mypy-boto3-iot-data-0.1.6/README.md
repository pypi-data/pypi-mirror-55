# Mypy-boto3 iot-data submodule

Provides type annotations for boto3 iot-data service

## Installation

```bash
pip install mypy-boto3[iot-data]
```

## Usage

```python
import boto3
from mypy_boto3.iot_data import Client, ServiceResource

client: Client = boto3.client("iot-data")
resource: ServiceResource = boto3.resource("iot-data")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

