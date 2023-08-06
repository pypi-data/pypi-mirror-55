# Mypy-boto3 mediastore submodule

Provides type annotations for boto3 mediastore service

## Installation

```bash
pip install mypy-boto3[mediastore]
```

## Usage

```python
import boto3
from mypy_boto3.mediastore import Client, ServiceResource

client: Client = boto3.client("mediastore")
resource: ServiceResource = boto3.resource("mediastore")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

