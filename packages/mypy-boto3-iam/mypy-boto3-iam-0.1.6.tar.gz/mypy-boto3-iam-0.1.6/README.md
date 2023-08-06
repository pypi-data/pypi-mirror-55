# Mypy-boto3 iam submodule

Provides type annotations for boto3 iam service

## Installation

```bash
pip install mypy-boto3[iam]
```

## Usage

```python
import boto3
from mypy_boto3.iam import Client, ServiceResource

client: Client = boto3.client("iam")
resource: ServiceResource = boto3.resource("iam")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

