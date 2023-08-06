# Mypy-boto3 mgh submodule

Provides type annotations for boto3 mgh service

## Installation

```bash
pip install mypy-boto3[mgh]
```

## Usage

```python
import boto3
from mypy_boto3.mgh import Client, ServiceResource

client: Client = boto3.client("mgh")
resource: ServiceResource = boto3.resource("mgh")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

