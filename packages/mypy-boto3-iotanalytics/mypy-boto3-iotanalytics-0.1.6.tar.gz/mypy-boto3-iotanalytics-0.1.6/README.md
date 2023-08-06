# Mypy-boto3 iotanalytics submodule

Provides type annotations for boto3 iotanalytics service

## Installation

```bash
pip install mypy-boto3[iotanalytics]
```

## Usage

```python
import boto3
from mypy_boto3.iotanalytics import Client, ServiceResource

client: Client = boto3.client("iotanalytics")
resource: ServiceResource = boto3.resource("iotanalytics")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

