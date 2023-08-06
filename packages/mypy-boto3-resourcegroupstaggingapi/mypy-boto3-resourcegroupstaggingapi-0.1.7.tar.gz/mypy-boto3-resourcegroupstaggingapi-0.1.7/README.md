# mypy-boto3-resourcegroupstaggingapi submodule

Provides type annotations for `boto3.resourcegroupstaggingapi` service

## Installation

```bash
pip install mypy-boto3[resourcegroupstaggingapi]
```

## Usage

```python
import boto3
from mypy_boto3.resourcegroupstaggingapi import Client, ServiceResource

client: Client = boto3.client("resourcegroupstaggingapi")
resource: ServiceResource = boto3.resource("resourcegroupstaggingapi")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

