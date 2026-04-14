#!/usr/bin/env python3
import sys
import json
import requests

THEHIVE_URL = "http://<THEHIVE_IP>:9000"
THEHIVE_API_KEY = "<YOUR_WAZUH_SERVICE_API_KEY>"
THEHIVE_ORG = "SOC-Lab"

alert_file = open(sys.argv[1])
alert = json.load(alert_file)
alert_file.close()

title = alert.get("rule", {}).get("description", "Wazuh Alert")
level = alert.get("rule", {}).get("level", 1)
description = json.dumps(alert, indent=2)

payload = {
    "title": f"Wazuh Alert: {title}",
    "description": f"```\n{description}\n```",
    "severity": 2,
    "source": "Wazuh",
    "sourceRef": str(alert.get("id", "0")),
    "type": "external",
    "tags": ["wazuh", f"level-{level}"]
}

try:
    r = requests.post(
        f"{THEHIVE_URL}/api/v1/alert",
        json=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {THEHIVE_API_KEY}",
            "X-Organisation": THEHIVE_ORG
        }
    )
    print(r.status_code, r.text)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
