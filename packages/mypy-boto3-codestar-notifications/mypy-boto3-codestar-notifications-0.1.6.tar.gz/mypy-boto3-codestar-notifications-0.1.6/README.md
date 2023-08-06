# Mypy-boto3 codestar-notifications submodule

Provides type annotations for boto3 codestar-notifications service

## Installation

```bash
pip install mypy-boto3[codestar-notifications]
```

## Usage

```python
import boto3
from mypy_boto3.codestar_notifications import Client, ServiceResource

client: Client = boto3.client("codestar-notifications")
resource: ServiceResource = boto3.resource("codestar-notifications")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

