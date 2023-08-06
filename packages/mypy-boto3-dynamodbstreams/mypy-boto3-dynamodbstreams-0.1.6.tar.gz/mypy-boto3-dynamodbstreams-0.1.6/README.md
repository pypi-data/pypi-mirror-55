# Mypy-boto3 dynamodbstreams submodule

Provides type annotations for boto3 dynamodbstreams service

## Installation

```bash
pip install mypy-boto3[dynamodbstreams]
```

## Usage

```python
import boto3
from mypy_boto3.dynamodbstreams import Client, ServiceResource

client: Client = boto3.client("dynamodbstreams")
resource: ServiceResource = boto3.resource("dynamodbstreams")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

