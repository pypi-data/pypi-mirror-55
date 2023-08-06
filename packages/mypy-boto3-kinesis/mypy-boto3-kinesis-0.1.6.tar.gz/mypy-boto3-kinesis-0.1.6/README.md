# Mypy-boto3 kinesis submodule

Provides type annotations for boto3 kinesis service

## Installation

```bash
pip install mypy-boto3[kinesis]
```

## Usage

```python
import boto3
from mypy_boto3.kinesis import Client, ServiceResource

client: Client = boto3.client("kinesis")
resource: ServiceResource = boto3.resource("kinesis")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

