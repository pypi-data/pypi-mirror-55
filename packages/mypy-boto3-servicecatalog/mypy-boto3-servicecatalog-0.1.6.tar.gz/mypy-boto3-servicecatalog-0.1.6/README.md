# Mypy-boto3 servicecatalog submodule

Provides type annotations for boto3 servicecatalog service

## Installation

```bash
pip install mypy-boto3[servicecatalog]
```

## Usage

```python
import boto3
from mypy_boto3.servicecatalog import Client, ServiceResource

client: Client = boto3.client("servicecatalog")
resource: ServiceResource = boto3.resource("servicecatalog")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

