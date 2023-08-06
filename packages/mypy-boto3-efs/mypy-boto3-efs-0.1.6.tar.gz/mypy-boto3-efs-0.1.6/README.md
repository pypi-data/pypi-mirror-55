# Mypy-boto3 efs submodule

Provides type annotations for boto3 efs service

## Installation

```bash
pip install mypy-boto3[efs]
```

## Usage

```python
import boto3
from mypy_boto3.efs import Client, ServiceResource

client: Client = boto3.client("efs")
resource: ServiceResource = boto3.resource("efs")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

