# Mypy-boto3 serverlessrepo submodule

Provides type annotations for boto3 serverlessrepo service

## Installation

```bash
pip install mypy-boto3[serverlessrepo]
```

## Usage

```python
import boto3
from mypy_boto3.serverlessrepo import Client, ServiceResource

client: Client = boto3.client("serverlessrepo")
resource: ServiceResource = boto3.resource("serverlessrepo")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

