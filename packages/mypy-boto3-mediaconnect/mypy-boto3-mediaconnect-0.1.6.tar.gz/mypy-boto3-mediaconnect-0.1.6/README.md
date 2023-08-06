# Mypy-boto3 mediaconnect submodule

Provides type annotations for boto3 mediaconnect service

## Installation

```bash
pip install mypy-boto3[mediaconnect]
```

## Usage

```python
import boto3
from mypy_boto3.mediaconnect import Client, ServiceResource

client: Client = boto3.client("mediaconnect")
resource: ServiceResource = boto3.resource("mediaconnect")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

