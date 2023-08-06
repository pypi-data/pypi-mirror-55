# mypy-boto3-cloudhsmv2 submodule

Provides type annotations for `boto3.cloudhsmv2` service

## Installation

```bash
pip install mypy-boto3[cloudhsmv2]
```

## Usage

```python
import boto3
from mypy_boto3.cloudhsmv2 import Client, ServiceResource

client: Client = boto3.client("cloudhsmv2")
resource: ServiceResource = boto3.resource("cloudhsmv2")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

