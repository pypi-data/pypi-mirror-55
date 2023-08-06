# mypy-boto3-waf submodule

Provides type annotations for `boto3.waf` service

## Installation

```bash
pip install mypy-boto3[waf]
```

## Usage

```python
import boto3
from mypy_boto3.waf import Client, ServiceResource

client: Client = boto3.client("waf")
resource: ServiceResource = boto3.resource("waf")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

