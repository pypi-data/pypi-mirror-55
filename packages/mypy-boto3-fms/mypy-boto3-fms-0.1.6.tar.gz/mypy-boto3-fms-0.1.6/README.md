# Mypy-boto3 fms submodule

Provides type annotations for boto3 fms service

## Installation

```bash
pip install mypy-boto3[fms]
```

## Usage

```python
import boto3
from mypy_boto3.fms import Client, ServiceResource

client: Client = boto3.client("fms")
resource: ServiceResource = boto3.resource("fms")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

