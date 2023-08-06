# mypy-boto3-elbv2 submodule

Provides type annotations for `boto3.elbv2` service

## Installation

```bash
pip install mypy-boto3[elbv2]
```

## Usage

```python
import boto3
from mypy_boto3.elbv2 import Client, ServiceResource

client: Client = boto3.client("elbv2")
resource: ServiceResource = boto3.resource("elbv2")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

