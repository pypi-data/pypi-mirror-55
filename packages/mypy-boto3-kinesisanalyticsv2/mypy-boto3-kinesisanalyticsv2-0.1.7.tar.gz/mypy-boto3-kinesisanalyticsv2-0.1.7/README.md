# mypy-boto3-kinesisanalyticsv2 submodule

Provides type annotations for `boto3.kinesisanalyticsv2` service

## Installation

```bash
pip install mypy-boto3[kinesisanalyticsv2]
```

## Usage

```python
import boto3
from mypy_boto3.kinesisanalyticsv2 import Client, ServiceResource

client: Client = boto3.client("kinesisanalyticsv2")
resource: ServiceResource = boto3.resource("kinesisanalyticsv2")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

