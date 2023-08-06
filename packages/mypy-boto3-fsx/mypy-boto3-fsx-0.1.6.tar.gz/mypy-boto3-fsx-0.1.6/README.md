# Mypy-boto3 fsx submodule

Provides type annotations for boto3 fsx service

## Installation

```bash
pip install mypy-boto3[fsx]
```

## Usage

```python
import boto3
from mypy_boto3.fsx import Client, ServiceResource

client: Client = boto3.client("fsx")
resource: ServiceResource = boto3.resource("fsx")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

