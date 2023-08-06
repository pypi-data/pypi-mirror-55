# Mypy-boto3 health submodule

Provides type annotations for boto3 health service

## Installation

```bash
pip install mypy-boto3[health]
```

## Usage

```python
import boto3
from mypy_boto3.health import Client, ServiceResource

client: Client = boto3.client("health")
resource: ServiceResource = boto3.resource("health")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

