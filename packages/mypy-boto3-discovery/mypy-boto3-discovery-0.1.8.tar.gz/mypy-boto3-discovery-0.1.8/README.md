# mypy-boto3-discovery submodule

Provides type annotations for `boto3.discovery` service

## Installation

```bash
pip install mypy-boto3[discovery]
```

## Usage

```python
import boto3
from mypy_boto3.discovery import Client, ServiceResource

client: Client = boto3.client("discovery")
resource: ServiceResource = boto3.resource("discovery")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

