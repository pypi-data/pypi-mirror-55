# mypy-boto3-xray submodule

Provides type annotations for `boto3.xray` service

## Installation

```bash
pip install mypy-boto3[xray]
```

## Usage

```python
import boto3
from mypy_boto3.xray import Client, ServiceResource

client: Client = boto3.client("xray")
resource: ServiceResource = boto3.resource("xray")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

