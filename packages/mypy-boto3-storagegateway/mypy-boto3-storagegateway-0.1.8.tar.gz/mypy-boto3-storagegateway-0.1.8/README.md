# mypy-boto3-storagegateway submodule

Provides type annotations for `boto3.storagegateway` service

## Installation

```bash
pip install mypy-boto3[storagegateway]
```

## Usage

```python
import boto3
from mypy_boto3.storagegateway import Client, ServiceResource

client: Client = boto3.client("storagegateway")
resource: ServiceResource = boto3.resource("storagegateway")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

