"""
Output Guardrails

Checks Gemini's response before
returning it to the user.
"""
# ============================================================
# BLOCKED OUTPUT PATTERNS
# ============================================================
BLOCKED_OUTPUT_PATTERNS = [
    "api key",
    "api_key",
    "secret key",
    "password",
    "private key",
]
# ============================================================
# OUTPUT GUARDRAIL
# ============================================================
def check_output(output: str) -> dict:
    """
    Validate Gemini output.
    Returns:
    allowed
    category
    message
    """
    # --------------------------------------------------------
    # 1. Empty output
    # --------------------------------------------------------
    if not output or not output.strip():
        return {
            "allowed": False,
            "category": "EMPTY_OUTPUT",
            "message": (
                "Model returned an empty response."
            )
        }
    # --------------------------------------------------------
    # 2. Normalize
    # --------------------------------------------------------
    text = output.lower()
    # --------------------------------------------------------
    # 3. Sensitive information
    # --------------------------------------------------------
    for pattern in BLOCKED_OUTPUT_PATTERNS:
        if pattern in text:
            return {
                "allowed": False,
                "category": "SENSITIVE_OUTPUT",
                "message": (
                    "Potentially sensitive information "
                    "detected in model output."
                )
            }
    # --------------------------------------------------------
    # 4. Safe output
    # --------------------------------------------------------
    return {
        "allowed": True,
        "category": "SAFE",
        "message": "Output passed the guardrail."
    }