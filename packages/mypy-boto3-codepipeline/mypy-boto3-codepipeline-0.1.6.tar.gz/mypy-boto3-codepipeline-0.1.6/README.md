# Mypy-boto3 codepipeline submodule

Provides type annotations for boto3 codepipeline service

## Installation

```bash
pip install mypy-boto3[codepipeline]
```

## Usage

```python
import boto3
from mypy_boto3.codepipeline import Client, ServiceResource

client: Client = boto3.client("codepipeline")
resource: ServiceResource = boto3.resource("codepipeline")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

