# mypy-boto3-ec2 submodule

Provides type annotations for `boto3.ec2` service

## Installation

```bash
pip install mypy-boto3[ec2]
```

## Usage

```python
import boto3
from mypy_boto3.ec2 import Client, ServiceResource

client: Client = boto3.client("ec2")
resource: ServiceResource = boto3.resource("ec2")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

