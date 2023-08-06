# Mypy-boto3 iot-jobs-data submodule

Provides type annotations for boto3 iot-jobs-data service

## Installation

```bash
pip install mypy-boto3[iot-jobs-data]
```

## Usage

```python
import boto3
from mypy_boto3.iot_jobs_data import Client, ServiceResource

client: Client = boto3.client("iot-jobs-data")
resource: ServiceResource = boto3.resource("iot-jobs-data")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

