# Mypy-boto3 mq submodule

Provides type annotations for boto3 mq service

## Installation

```bash
pip install mypy-boto3[mq]
```

## Usage

```python
import boto3
from mypy_boto3.mq import Client, ServiceResource

client: Client = boto3.client("mq")
resource: ServiceResource = boto3.resource("mq")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

