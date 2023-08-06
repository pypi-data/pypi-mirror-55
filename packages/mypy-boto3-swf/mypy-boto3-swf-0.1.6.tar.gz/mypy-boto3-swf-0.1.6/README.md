# Mypy-boto3 swf submodule

Provides type annotations for boto3 swf service

## Installation

```bash
pip install mypy-boto3[swf]
```

## Usage

```python
import boto3
from mypy_boto3.swf import Client, ServiceResource

client: Client = boto3.client("swf")
resource: ServiceResource = boto3.resource("swf")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

