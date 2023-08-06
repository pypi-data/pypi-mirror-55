# Mypy-boto3 organizations submodule

Provides type annotations for boto3 organizations service

## Installation

```bash
pip install mypy-boto3[organizations]
```

## Usage

```python
import boto3
from mypy_boto3.organizations import Client, ServiceResource

client: Client = boto3.client("organizations")
resource: ServiceResource = boto3.resource("organizations")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

