# mypy-boto3-kafka submodule

Provides type annotations for `boto3.kafka` service

## Installation

```bash
pip install mypy-boto3[kafka]
```

## Usage

```python
import boto3
from mypy_boto3.kafka import Client, ServiceResource

client: Client = boto3.client("kafka")
resource: ServiceResource = boto3.resource("kafka")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

