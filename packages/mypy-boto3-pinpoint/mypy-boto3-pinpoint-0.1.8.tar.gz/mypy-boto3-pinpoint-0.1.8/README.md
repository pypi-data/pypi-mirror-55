# mypy-boto3-pinpoint submodule

Provides type annotations for `boto3.pinpoint` service

## Installation

```bash
pip install mypy-boto3[pinpoint]
```

## Usage

```python
import boto3
from mypy_boto3.pinpoint import Client, ServiceResource

client: Client = boto3.client("pinpoint")
resource: ServiceResource = boto3.resource("pinpoint")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

