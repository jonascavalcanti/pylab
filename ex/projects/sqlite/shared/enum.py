from enum import Enum


class SyncProvider(Enum):
    SCIM = 0  # System for Cross-domain Identity Management
    GWS = 1  # Google Workspaces
    AWS = 2  # Amazon Web Services
    GH = 3  # GitHub
    NR = 4  # New Relic


class SyncAction(Enum):
    NONE = 0
    INSYNC = 1
    CREATED = 2
    UPDATED = 3
    PATCHED = 4
    INVITED = 5
    REMOVED = 6
    SKIPPED = 7
