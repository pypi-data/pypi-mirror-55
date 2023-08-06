# Mypy-boto3 config submodule

Provides type annotations for boto3 config service

## Installation

```bash
pip install mypy-boto3[config]
```

## Usage

```python
import boto3
from mypy_boto3.config import Client, ServiceResource

client: Client = boto3.client("config")
resource: ServiceResource = boto3.resource("config")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

