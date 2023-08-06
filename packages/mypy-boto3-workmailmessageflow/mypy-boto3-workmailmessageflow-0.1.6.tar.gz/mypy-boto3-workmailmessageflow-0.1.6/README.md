# Mypy-boto3 workmailmessageflow submodule

Provides type annotations for boto3 workmailmessageflow service

## Installation

```bash
pip install mypy-boto3[workmailmessageflow]
```

## Usage

```python
import boto3
from mypy_boto3.workmailmessageflow import Client, ServiceResource

client: Client = boto3.client("workmailmessageflow")
resource: ServiceResource = boto3.resource("workmailmessageflow")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

