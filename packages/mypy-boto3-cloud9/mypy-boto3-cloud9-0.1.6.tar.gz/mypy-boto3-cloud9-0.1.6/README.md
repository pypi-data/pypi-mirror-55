# Mypy-boto3 cloud9 submodule

Provides type annotations for boto3 cloud9 service

## Installation

```bash
pip install mypy-boto3[cloud9]
```

## Usage

```python
import boto3
from mypy_boto3.cloud9 import Client, ServiceResource

client: Client = boto3.client("cloud9")
resource: ServiceResource = boto3.resource("cloud9")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

