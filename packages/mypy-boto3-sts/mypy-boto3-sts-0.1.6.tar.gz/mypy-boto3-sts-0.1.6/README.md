# Mypy-boto3 sts submodule

Provides type annotations for boto3 sts service

## Installation

```bash
pip install mypy-boto3[sts]
```

## Usage

```python
import boto3
from mypy_boto3.sts import Client, ServiceResource

client: Client = boto3.client("sts")
resource: ServiceResource = boto3.resource("sts")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

