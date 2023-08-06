# Mypy-boto3 lambda submodule

Provides type annotations for boto3 lambda service

## Installation

```bash
pip install mypy-boto3[lambda]
```

## Usage

```python
import boto3
from mypy_boto3.lambda_ import Client, ServiceResource

client: Client = boto3.client("lambda")
resource: ServiceResource = boto3.resource("lambda")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

