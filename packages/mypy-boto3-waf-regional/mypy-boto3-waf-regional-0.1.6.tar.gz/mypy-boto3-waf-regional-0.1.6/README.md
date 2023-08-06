# Mypy-boto3 waf-regional submodule

Provides type annotations for boto3 waf-regional service

## Installation

```bash
pip install mypy-boto3[waf-regional]
```

## Usage

```python
import boto3
from mypy_boto3.waf_regional import Client, ServiceResource

client: Client = boto3.client("waf-regional")
resource: ServiceResource = boto3.resource("waf-regional")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

