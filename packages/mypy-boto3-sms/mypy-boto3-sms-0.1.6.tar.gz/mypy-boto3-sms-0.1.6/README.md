# Mypy-boto3 sms submodule

Provides type annotations for boto3 sms service

## Installation

```bash
pip install mypy-boto3[sms]
```

## Usage

```python
import boto3
from mypy_boto3.sms import Client, ServiceResource

client: Client = boto3.client("sms")
resource: ServiceResource = boto3.resource("sms")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

