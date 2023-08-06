# mypy-boto3-elb submodule

Provides type annotations for `boto3.elb` service

## Installation

```bash
pip install mypy-boto3[elb]
```

## Usage

```python
import boto3
from mypy_boto3.elb import Client, ServiceResource

client: Client = boto3.client("elb")
resource: ServiceResource = boto3.resource("elb")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

