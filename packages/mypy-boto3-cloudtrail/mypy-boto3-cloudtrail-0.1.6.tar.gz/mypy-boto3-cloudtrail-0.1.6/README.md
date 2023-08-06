# Mypy-boto3 cloudtrail submodule

Provides type annotations for boto3 cloudtrail service

## Installation

```bash
pip install mypy-boto3[cloudtrail]
```

## Usage

```python
import boto3
from mypy_boto3.cloudtrail import Client, ServiceResource

client: Client = boto3.client("cloudtrail")
resource: ServiceResource = boto3.resource("cloudtrail")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

