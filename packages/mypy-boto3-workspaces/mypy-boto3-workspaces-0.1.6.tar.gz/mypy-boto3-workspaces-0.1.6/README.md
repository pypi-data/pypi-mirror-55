# Mypy-boto3 workspaces submodule

Provides type annotations for boto3 workspaces service

## Installation

```bash
pip install mypy-boto3[workspaces]
```

## Usage

```python
import boto3
from mypy_boto3.workspaces import Client, ServiceResource

client: Client = boto3.client("workspaces")
resource: ServiceResource = boto3.resource("workspaces")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

