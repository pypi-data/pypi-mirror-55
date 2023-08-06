# mypy-boto3-kinesisanalytics submodule

Provides type annotations for `boto3.kinesisanalytics` service

## Installation

```bash
pip install mypy-boto3[kinesisanalytics]
```

## Usage

```python
import boto3
from mypy_boto3.kinesisanalytics import Client, ServiceResource

client: Client = boto3.client("kinesisanalytics")
resource: ServiceResource = boto3.resource("kinesisanalytics")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

