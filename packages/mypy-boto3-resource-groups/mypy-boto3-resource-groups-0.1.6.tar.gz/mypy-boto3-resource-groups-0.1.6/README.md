# Mypy-boto3 resource-groups submodule

Provides type annotations for boto3 resource-groups service

## Installation

```bash
pip install mypy-boto3[resource-groups]
```

## Usage

```python
import boto3
from mypy_boto3.resource_groups import Client, ServiceResource

client: Client = boto3.client("resource-groups")
resource: ServiceResource = boto3.resource("resource-groups")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

