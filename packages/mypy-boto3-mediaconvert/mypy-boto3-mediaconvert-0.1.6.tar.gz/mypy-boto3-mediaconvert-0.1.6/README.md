# Mypy-boto3 mediaconvert submodule

Provides type annotations for boto3 mediaconvert service

## Installation

```bash
pip install mypy-boto3[mediaconvert]
```

## Usage

```python
import boto3
from mypy_boto3.mediaconvert import Client, ServiceResource

client: Client = boto3.client("mediaconvert")
resource: ServiceResource = boto3.resource("mediaconvert")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

