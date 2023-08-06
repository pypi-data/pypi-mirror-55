# Mypy-boto3 es submodule

Provides type annotations for boto3 es service

## Installation

```bash
pip install mypy-boto3[es]
```

## Usage

```python
import boto3
from mypy_boto3.es import Client, ServiceResource

client: Client = boto3.client("es")
resource: ServiceResource = boto3.resource("es")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

