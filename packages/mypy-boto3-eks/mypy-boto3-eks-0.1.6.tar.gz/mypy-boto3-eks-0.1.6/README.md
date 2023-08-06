# Mypy-boto3 eks submodule

Provides type annotations for boto3 eks service

## Installation

```bash
pip install mypy-boto3[eks]
```

## Usage

```python
import boto3
from mypy_boto3.eks import Client, ServiceResource

client: Client = boto3.client("eks")
resource: ServiceResource = boto3.resource("eks")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

