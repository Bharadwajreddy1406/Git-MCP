from enum import Enum

class MCPVersion(Enum):
    V1_0 = "1.0"
    V1_1 = "1.1"
    V1_10 = "1.10"
    V1_11 = "1.11"
    V1_12 = "1.12"
    V1_13 = "1.13"
    V1_14 = "1.14"
    V1_15 = "1.15"
    V1_16 = "1.16"
    V1_17 = "1.17"
    V1_18 = "1.18"
    V1_19 = "1.19"
    V1_20 = "1.20"

class RepoArea(Enum):
    WORKING = "working"
    STAGED = "staged"
    COMMITTED = "committed"
    REMOTE = "remote"