# Mypy-boto3 clouddirectory submodule

Provides type annotations for boto3 clouddirectory service

## Installation

```bash
pip install mypy-boto3[clouddirectory]
```

## Usage

```python
import boto3
from mypy_boto3.clouddirectory import Client, ServiceResource

client: Client = boto3.client("clouddirectory")
resource: ServiceResource = boto3.resource("clouddirectory")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

