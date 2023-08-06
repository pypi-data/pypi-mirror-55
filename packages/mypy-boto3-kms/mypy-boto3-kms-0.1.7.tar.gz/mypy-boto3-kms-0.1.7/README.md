# mypy-boto3-kms submodule

Provides type annotations for `boto3.kms` service

## Installation

```bash
pip install mypy-boto3[kms]
```

## Usage

```python
import boto3
from mypy_boto3.kms import Client, ServiceResource

client: Client = boto3.client("kms")
resource: ServiceResource = boto3.resource("kms")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

