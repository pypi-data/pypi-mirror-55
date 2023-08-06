# mypy-boto3-iot1click-devices submodule

Provides type annotations for `boto3.iot1click-devices` service

## Installation

```bash
pip install mypy-boto3[iot1click_devices]
```

## Usage

```python
import boto3
from mypy_boto3.iot1click_devices import Client, ServiceResource

client: Client = boto3.client("iot1click-devices")
resource: ServiceResource = boto3.resource("iot1click-devices")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

