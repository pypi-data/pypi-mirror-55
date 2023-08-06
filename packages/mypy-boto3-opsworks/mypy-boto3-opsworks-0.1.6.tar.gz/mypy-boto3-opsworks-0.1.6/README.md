# Mypy-boto3 opsworks submodule

Provides type annotations for boto3 opsworks service

## Installation

```bash
pip install mypy-boto3[opsworks]
```

## Usage

```python
import boto3
from mypy_boto3.opsworks import Client, ServiceResource

client: Client = boto3.client("opsworks")
resource: ServiceResource = boto3.resource("opsworks")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

