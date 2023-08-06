# Mypy-boto3 s3control submodule

Provides type annotations for boto3 s3control service

## Installation

```bash
pip install mypy-boto3[s3control]
```

## Usage

```python
import boto3
from mypy_boto3.s3control import Client, ServiceResource

client: Client = boto3.client("s3control")
resource: ServiceResource = boto3.resource("s3control")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

