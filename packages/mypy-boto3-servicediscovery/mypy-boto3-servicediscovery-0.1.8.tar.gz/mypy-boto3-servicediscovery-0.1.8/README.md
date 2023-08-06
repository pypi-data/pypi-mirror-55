# mypy-boto3-servicediscovery submodule

Provides type annotations for `boto3.servicediscovery` service

## Installation

```bash
pip install mypy-boto3[servicediscovery]
```

## Usage

```python
import boto3
from mypy_boto3.servicediscovery import Client, ServiceResource

client: Client = boto3.client("servicediscovery")
resource: ServiceResource = boto3.resource("servicediscovery")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

