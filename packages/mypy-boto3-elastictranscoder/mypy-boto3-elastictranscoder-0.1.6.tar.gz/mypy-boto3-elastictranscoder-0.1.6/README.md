# Mypy-boto3 elastictranscoder submodule

Provides type annotations for boto3 elastictranscoder service

## Installation

```bash
pip install mypy-boto3[elastictranscoder]
```

## Usage

```python
import boto3
from mypy_boto3.elastictranscoder import Client, ServiceResource

client: Client = boto3.client("elastictranscoder")
resource: ServiceResource = boto3.resource("elastictranscoder")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

