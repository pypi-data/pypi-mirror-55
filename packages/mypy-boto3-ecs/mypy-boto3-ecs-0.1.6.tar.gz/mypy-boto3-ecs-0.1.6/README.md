# Mypy-boto3 ecs submodule

Provides type annotations for boto3 ecs service

## Installation

```bash
pip install mypy-boto3[ecs]
```

## Usage

```python
import boto3
from mypy_boto3.ecs import Client, ServiceResource

client: Client = boto3.client("ecs")
resource: ServiceResource = boto3.resource("ecs")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

