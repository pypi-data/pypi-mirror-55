# Mypy-boto3 connect submodule

Provides type annotations for boto3 connect service

## Installation

```bash
pip install mypy-boto3[connect]
```

## Usage

```python
import boto3
from mypy_boto3.connect import Client, ServiceResource

client: Client = boto3.client("connect")
resource: ServiceResource = boto3.resource("connect")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

