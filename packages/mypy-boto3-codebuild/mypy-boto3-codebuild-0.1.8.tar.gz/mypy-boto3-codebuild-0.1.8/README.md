# mypy-boto3-codebuild submodule

Provides type annotations for `boto3.codebuild` service

## Installation

```bash
pip install mypy-boto3[codebuild]
```

## Usage

```python
import boto3
from mypy_boto3.codebuild import Client, ServiceResource

client: Client = boto3.client("codebuild")
resource: ServiceResource = boto3.resource("codebuild")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

