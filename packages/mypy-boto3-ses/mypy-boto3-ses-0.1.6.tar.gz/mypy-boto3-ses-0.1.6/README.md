# Mypy-boto3 ses submodule

Provides type annotations for boto3 ses service

## Installation

```bash
pip install mypy-boto3[ses]
```

## Usage

```python
import boto3
from mypy_boto3.ses import Client, ServiceResource

client: Client = boto3.client("ses")
resource: ServiceResource = boto3.resource("ses")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

