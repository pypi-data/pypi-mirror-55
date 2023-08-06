# Mypy-boto3 backup submodule

Provides type annotations for boto3 backup service

## Installation

```bash
pip install mypy-boto3[backup]
```

## Usage

```python
import boto3
from mypy_boto3.backup import Client, ServiceResource

client: Client = boto3.client("backup")
resource: ServiceResource = boto3.resource("backup")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

