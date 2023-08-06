# mypy-boto3-iotevents-data submodule

Provides type annotations for `boto3.iotevents-data` service

## Installation

```bash
pip install mypy-boto3[iotevents_data]
```

## Usage

```python
import boto3
from mypy_boto3.iotevents_data import Client, ServiceResource

client: Client = boto3.client("iotevents-data")
resource: ServiceResource = boto3.resource("iotevents-data")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

