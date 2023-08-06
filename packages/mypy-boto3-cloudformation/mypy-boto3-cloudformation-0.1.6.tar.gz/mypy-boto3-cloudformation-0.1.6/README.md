# Mypy-boto3 cloudformation submodule

Provides type annotations for boto3 cloudformation service

## Installation

```bash
pip install mypy-boto3[cloudformation]
```

## Usage

```python
import boto3
from mypy_boto3.cloudformation import Client, ServiceResource

client: Client = boto3.client("cloudformation")
resource: ServiceResource = boto3.resource("cloudformation")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

