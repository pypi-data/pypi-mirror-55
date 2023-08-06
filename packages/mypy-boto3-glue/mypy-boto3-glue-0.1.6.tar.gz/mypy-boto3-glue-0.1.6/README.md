# Mypy-boto3 glue submodule

Provides type annotations for boto3 glue service

## Installation

```bash
pip install mypy-boto3[glue]
```

## Usage

```python
import boto3
from mypy_boto3.glue import Client, ServiceResource

client: Client = boto3.client("glue")
resource: ServiceResource = boto3.resource("glue")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

