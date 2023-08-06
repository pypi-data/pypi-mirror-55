# Mypy-boto3 docdb submodule

Provides type annotations for boto3 docdb service

## Installation

```bash
pip install mypy-boto3[docdb]
```

## Usage

```python
import boto3
from mypy_boto3.docdb import Client, ServiceResource

client: Client = boto3.client("docdb")
resource: ServiceResource = boto3.resource("docdb")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

