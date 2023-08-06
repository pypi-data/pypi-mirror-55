# Mypy-boto3 shield submodule

Provides type annotations for boto3 shield service

## Installation

```bash
pip install mypy-boto3[shield]
```

## Usage

```python
import boto3
from mypy_boto3.shield import Client, ServiceResource

client: Client = boto3.client("shield")
resource: ServiceResource = boto3.resource("shield")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

