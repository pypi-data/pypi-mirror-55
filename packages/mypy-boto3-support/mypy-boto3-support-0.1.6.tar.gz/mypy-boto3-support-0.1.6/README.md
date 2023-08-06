# Mypy-boto3 support submodule

Provides type annotations for boto3 support service

## Installation

```bash
pip install mypy-boto3[support]
```

## Usage

```python
import boto3
from mypy_boto3.support import Client, ServiceResource

client: Client = boto3.client("support")
resource: ServiceResource = boto3.resource("support")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

