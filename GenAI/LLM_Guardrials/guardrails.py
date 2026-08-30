"""
Input Guardrails
This module checks whether the user's prompt
is safe before sending it to Gemini.
"""
import re
# ============================================================
# BLOCKED KEYWORDS
# ============================================================
BLOCKED_KEYWORDS = [
    "hack",
    "malware",
    "ransomware",
    "phishing",
    "bomb",
    "terrorist",
    "terrorism",
    "kill",
    "murder",
    "weapon",
]
# ============================================================
# PROMPT INJECTION PATTERNS
# ============================================================
PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "ignore prior instructions",
    "ignore all prior instructions",
    "forget previous instructions",
    "forget all previous instructions"
    "disregard previous instructions",
    "disregard all previous instructions",
    "override previous instructions",
    "override system instructions",
    "system prompt",
    "system message",
    "developer message",
    "developer instructions",
    "reveal your prompt",
    "reveal the system prompt",
    "show your system prompt",
    "tell me your system prompt",
    "what are your instructions",
    "reveal your instructions",
    "show your instructions",
]
# ============================================================
# JAILBREAK PATTERNS
# ============================================================
JAILBREAK_PATTERNS = [
    "jailbreak",
    "jailbreak mode",
    "do anything now",
    "dan mode",
    "enable dan",
    "developer mode",
    "god mode",
    "unrestricted mode",
    "uncensored mode",
    "bypass safety",
    "bypass safeguards",
    "bypass restrictions",
    "disable safety",
    "disable safeguards",
    "disable restrictions",
    "ignore safety",
    "ignore safeguards",
    "ignore restrictions",
    "remove safety",
    "remove restrictions",
    "without restrictions",
    "without safety restrictions",
    "act as an unrestricted ai",
    "pretend you are an unrestricted ai",
    "pretend there are no restrictions",
]
# ============================================================
# FIND PATTERN
# ============================================================
def find_pattern(
    text: str,
    patterns: list[str]
) -> str | None:
    for pattern in patterns:
        if pattern in text:
            return pattern
    return None
# ============================================================
# INPUT GUARDRAIL
# ============================================================
def check_input(user_input: str) -> dict:
    """
    Validate user input.
    Returns a dictionary containing:
    allowed
    category
    message
    """
    # --------------------------------------------------------
    # 1. Validate type
    # --------------------------------------------------------
    if not isinstance(user_input, str):
        return {
            "allowed": False,
            "category": "INVALID_INPUT",
            "message": "Prompt must be a string."
        }
    # --------------------------------------------------------
    # 2. Empty prompt
    # --------------------------------------------------------
    if not user_input or not user_input.strip():
        return {
            "allowed": False,
            "category": "EMPTY_INPUT",
            "message": "Prompt cannot be empty."
        }
    # --------------------------------------------------------
    # 3. Maximum length
    # --------------------------------------------------------
    if len(user_input) > 5000:
        return {
            "allowed": False,
            "category": "INPUT_LENGTH",
            "message": (
                "Prompt exceeds 5000 characters."
            )
        }
    # --------------------------------------------------------
    # 4. Normalize input
    # --------------------------------------------------------
    text = user_input.strip().lower()
    # --------------------------------------------------------
    # 5. Blocked keywords
    # --------------------------------------------------------
    for keyword in BLOCKED_KEYWORDS:
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, text):
            return {
                "allowed": False,
                "category": "BLOCKED_KEYWORD",
                "message": (
                    f"Blocked keyword detected: "
                    f"'{keyword}'"
                )
            }
    # --------------------------------------------------------
    # 6. Prompt injection
    # --------------------------------------------------------
    detected_injection = find_pattern(
        text,
        PROMPT_INJECTION_PATTERNS
    )
    if detected_injection:
        return {
            "allowed": False,
            "category": "PROMPT_INJECTION",
            "message": "Prompt injection detected."
        }
    # --------------------------------------------------------
    # 7. Jailbreak
    # --------------------------------------------------------
    detected_jailbreak = find_pattern(
        text,
        JAILBREAK_PATTERNS
    )
    if detected_jailbreak:
        return {
            "allowed": False,
            "category": "JAILBREAK",
            "message": "Jailbreak attempt detected."
        }
    # --------------------------------------------------------
    # 8. Safe
    # --------------------------------------------------------
    return {
        "allowed": True,
        "category": "SAFE",
        "message": "Input passed all guardrails."
    }