# Mypy-boto3 workdocs submodule

Provides type annotations for boto3 workdocs service

## Installation

```bash
pip install mypy-boto3[workdocs]
```

## Usage

```python
import boto3
from mypy_boto3.workdocs import Client, ServiceResource

client: Client = boto3.client("workdocs")
resource: ServiceResource = boto3.resource("workdocs")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

