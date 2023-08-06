# Mypy-boto3 application-autoscaling submodule

Provides type annotations for boto3 application-autoscaling service

## Installation

```bash
pip install mypy-boto3[application-autoscaling]
```

## Usage

```python
import boto3
from mypy_boto3.application_autoscaling import Client, ServiceResource

client: Client = boto3.client("application-autoscaling")
resource: ServiceResource = boto3.resource("application-autoscaling")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

