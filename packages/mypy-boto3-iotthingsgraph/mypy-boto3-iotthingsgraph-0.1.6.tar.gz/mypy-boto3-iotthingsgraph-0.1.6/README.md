# Mypy-boto3 iotthingsgraph submodule

Provides type annotations for boto3 iotthingsgraph service

## Installation

```bash
pip install mypy-boto3[iotthingsgraph]
```

## Usage

```python
import boto3
from mypy_boto3.iotthingsgraph import Client, ServiceResource

client: Client = boto3.client("iotthingsgraph")
resource: ServiceResource = boto3.resource("iotthingsgraph")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

