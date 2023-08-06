# mypy-boto3-acm-pca submodule

Provides type annotations for `boto3.acm-pca` service

## Installation

```bash
pip install mypy-boto3[acm_pca]
```

## Usage

```python
import boto3
from mypy_boto3.acm_pca import Client, ServiceResource

client: Client = boto3.client("acm-pca")
resource: ServiceResource = boto3.resource("acm-pca")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

