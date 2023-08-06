# Mypy-boto3 pinpoint-sms-voice submodule

Provides type annotations for boto3 pinpoint-sms-voice service

## Installation

```bash
pip install mypy-boto3[pinpoint-sms-voice]
```

## Usage

```python
import boto3
from mypy_boto3.pinpoint_sms_voice import Client, ServiceResource

client: Client = boto3.client("pinpoint-sms-voice")
resource: ServiceResource = boto3.resource("pinpoint-sms-voice")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

