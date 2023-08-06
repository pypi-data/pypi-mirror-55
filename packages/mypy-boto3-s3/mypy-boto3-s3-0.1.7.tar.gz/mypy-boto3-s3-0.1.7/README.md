# mypy-boto3-s3 submodule

Provides type annotations for `boto3.s3` service

## Installation

```bash
pip install mypy-boto3[s3]
```

## Usage

```python
import boto3
from mypy_boto3.s3 import Client, ServiceResource

client: Client = boto3.client("s3")
resource: ServiceResource = boto3.resource("s3")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

