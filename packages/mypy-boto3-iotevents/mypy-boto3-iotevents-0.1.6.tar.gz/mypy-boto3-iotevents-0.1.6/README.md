# Mypy-boto3 iotevents submodule

Provides type annotations for boto3 iotevents service

## Installation

```bash
pip install mypy-boto3[iotevents]
```

## Usage

```python
import boto3
from mypy_boto3.iotevents import Client, ServiceResource

client: Client = boto3.client("iotevents")
resource: ServiceResource = boto3.resource("iotevents")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

