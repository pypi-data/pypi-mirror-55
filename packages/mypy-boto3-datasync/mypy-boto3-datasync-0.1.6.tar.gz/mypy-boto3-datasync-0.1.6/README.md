# Mypy-boto3 datasync submodule

Provides type annotations for boto3 datasync service

## Installation

```bash
pip install mypy-boto3[datasync]
```

## Usage

```python
import boto3
from mypy_boto3.datasync import Client, ServiceResource

client: Client = boto3.client("datasync")
resource: ServiceResource = boto3.resource("datasync")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

