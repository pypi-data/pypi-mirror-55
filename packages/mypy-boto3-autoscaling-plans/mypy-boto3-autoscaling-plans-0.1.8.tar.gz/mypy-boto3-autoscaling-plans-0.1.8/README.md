# mypy-boto3-autoscaling-plans submodule

Provides type annotations for `boto3.autoscaling-plans` service

## Installation

```bash
pip install mypy-boto3[autoscaling_plans]
```

## Usage

```python
import boto3
from mypy_boto3.autoscaling_plans import Client, ServiceResource

client: Client = boto3.client("autoscaling-plans")
resource: ServiceResource = boto3.resource("autoscaling-plans")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

