# Mypy-boto3 ds submodule

Provides type annotations for boto3 ds service

## Installation

```bash
pip install mypy-boto3[ds]
```

## Usage

```python
import boto3
from mypy_boto3.ds import Client, ServiceResource

client: Client = boto3.client("ds")
resource: ServiceResource = boto3.resource("ds")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

