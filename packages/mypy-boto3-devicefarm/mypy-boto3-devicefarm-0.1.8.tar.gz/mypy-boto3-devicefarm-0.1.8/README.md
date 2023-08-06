# mypy-boto3-devicefarm submodule

Provides type annotations for `boto3.devicefarm` service

## Installation

```bash
pip install mypy-boto3[devicefarm]
```

## Usage

```python
import boto3
from mypy_boto3.devicefarm import Client, ServiceResource

client: Client = boto3.client("devicefarm")
resource: ServiceResource = boto3.resource("devicefarm")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

