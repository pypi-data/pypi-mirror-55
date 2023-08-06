# Mypy-boto3 sagemaker-runtime submodule

Provides type annotations for boto3 sagemaker-runtime service

## Installation

```bash
pip install mypy-boto3[sagemaker-runtime]
```

## Usage

```python
import boto3
from mypy_boto3.sagemaker_runtime import Client, ServiceResource

client: Client = boto3.client("sagemaker-runtime")
resource: ServiceResource = boto3.resource("sagemaker-runtime")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

