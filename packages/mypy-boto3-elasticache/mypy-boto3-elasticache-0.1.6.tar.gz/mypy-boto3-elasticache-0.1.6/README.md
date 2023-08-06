# Mypy-boto3 elasticache submodule

Provides type annotations for boto3 elasticache service

## Installation

```bash
pip install mypy-boto3[elasticache]
```

## Usage

```python
import boto3
from mypy_boto3.elasticache import Client, ServiceResource

client: Client = boto3.client("elasticache")
resource: ServiceResource = boto3.resource("elasticache")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

