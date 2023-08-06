# Mypy-boto3 codedeploy submodule

Provides type annotations for boto3 codedeploy service

## Installation

```bash
pip install mypy-boto3[codedeploy]
```

## Usage

```python
import boto3
from mypy_boto3.codedeploy import Client, ServiceResource

client: Client = boto3.client("codedeploy")
resource: ServiceResource = boto3.resource("codedeploy")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

