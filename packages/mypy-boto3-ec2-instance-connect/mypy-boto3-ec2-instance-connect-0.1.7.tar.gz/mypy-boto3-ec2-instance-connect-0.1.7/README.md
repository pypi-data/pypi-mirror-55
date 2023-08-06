# mypy-boto3-ec2-instance-connect submodule

Provides type annotations for `boto3.ec2-instance-connect` service

## Installation

```bash
pip install mypy-boto3[ec2_instance_connect]
```

## Usage

```python
import boto3
from mypy_boto3.ec2_instance_connect import Client, ServiceResource

client: Client = boto3.client("ec2-instance-connect")
resource: ServiceResource = boto3.resource("ec2-instance-connect")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

