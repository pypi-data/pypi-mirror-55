# mypy-boto3-appmesh submodule

Provides type annotations for `boto3.appmesh` service

## Installation

```bash
pip install mypy-boto3[appmesh]
```

## Usage

```python
import boto3
from mypy_boto3.appmesh import Client, ServiceResource

client: Client = boto3.client("appmesh")
resource: ServiceResource = boto3.resource("appmesh")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

