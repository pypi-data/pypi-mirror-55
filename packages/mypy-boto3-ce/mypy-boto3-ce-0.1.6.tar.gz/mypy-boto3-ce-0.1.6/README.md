# Mypy-boto3 ce submodule

Provides type annotations for boto3 ce service

## Installation

```bash
pip install mypy-boto3[ce]
```

## Usage

```python
import boto3
from mypy_boto3.ce import Client, ServiceResource

client: Client = boto3.client("ce")
resource: ServiceResource = boto3.resource("ce")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

