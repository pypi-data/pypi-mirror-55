# Mypy-boto3 inspector submodule

Provides type annotations for boto3 inspector service

## Installation

```bash
pip install mypy-boto3[inspector]
```

## Usage

```python
import boto3
from mypy_boto3.inspector import Client, ServiceResource

client: Client = boto3.client("inspector")
resource: ServiceResource = boto3.resource("inspector")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

