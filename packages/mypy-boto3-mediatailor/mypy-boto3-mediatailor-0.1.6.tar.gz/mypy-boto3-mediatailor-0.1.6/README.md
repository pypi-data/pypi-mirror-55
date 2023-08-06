# Mypy-boto3 mediatailor submodule

Provides type annotations for boto3 mediatailor service

## Installation

```bash
pip install mypy-boto3[mediatailor]
```

## Usage

```python
import boto3
from mypy_boto3.mediatailor import Client, ServiceResource

client: Client = boto3.client("mediatailor")
resource: ServiceResource = boto3.resource("mediatailor")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

