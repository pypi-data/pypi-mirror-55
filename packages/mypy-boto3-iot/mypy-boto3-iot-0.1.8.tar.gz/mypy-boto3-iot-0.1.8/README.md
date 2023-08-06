# mypy-boto3-iot submodule

Provides type annotations for `boto3.iot` service

## Installation

```bash
pip install mypy-boto3[iot]
```

## Usage

```python
import boto3
from mypy_boto3.iot import Client, ServiceResource

client: Client = boto3.client("iot")
resource: ServiceResource = boto3.resource("iot")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

