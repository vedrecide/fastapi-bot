from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()

# Grab the guild channel and admin role from the environment
CHANNEL = int(os.environ["CHANNEL"])
ADMIN_ROLE_ID = int(os.environ["ADMIN_ROLE_ID"])

# In the real world these should be stored in a database
pending_requests: list[int] = []
approved_members: list[int] = []
