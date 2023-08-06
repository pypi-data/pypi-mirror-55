# mypy-boto3-mediapackage-vod submodule

Provides type annotations for `boto3.mediapackage-vod` service

## Installation

```bash
pip install mypy-boto3[mediapackage_vod]
```

## Usage

```python
import boto3
from mypy_boto3.mediapackage_vod import Client, ServiceResource

client: Client = boto3.client("mediapackage-vod")
resource: ServiceResource = boto3.resource("mediapackage-vod")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

