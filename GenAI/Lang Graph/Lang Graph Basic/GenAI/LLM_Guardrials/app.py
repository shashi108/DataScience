"""
FastAPI Application
LLM Guardrails Workshop
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from guardrails import check_input
from output_guardrails import check_output
from gemini_service import generate_response
# ============================================================
# FastAPI Application
# ============================================================
app = FastAPI(
    title="LLM Guardrails by Shashi Kumar",
    description=(
        "Gemini + FastAPI + "
        "Input and Output Guardrails"
    ),
    version="1.0.0",
)
# ============================================================
# Static Files
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)
# ============================================================
# Templates
# ============================================================
templates = Jinja2Templates(
    directory="templates"
)
# ============================================================
# Request Model
# ============================================================
class PromptRequest(BaseModel):
    prompt: str
# ============================================================
# Home Page
# ============================================================
@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )
# ============================================================
# Health Check
# ============================================================
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "application": "LLM Guardrails Workshop"
    }
# ============================================================
# Generate
# ============================================================
@app.post("/generate")
async def generate(request: PromptRequest):
    user_input = request.prompt
    # ========================================================
    # STEP 1
    # INPUT GUARDRAIL
    # ========================================================
    input_result = check_input(
        user_input
    )
    # ========================================================
    # BLOCK UNSAFE INPUT
    # ========================================================
    if not input_result["allowed"]:
        return {
            "status": "blocked",
            "stage": "input_guardrail",
            "category": input_result["category"],
            "message": input_result["message"],
            "response": None
        }
    # ========================================================
    # STEP 2
    # GEMINI
    # ========================================================
    model_response = generate_response(
        user_input
    )
    # ========================================================
    # STEP 3
    # OUTPUT GUARDRAIL
    # ========================================================
    output_result = check_output(
        model_response
    )
    # ========================================================
    # BLOCK UNSAFE OUTPUT
    # ========================================================
    if not output_result["allowed"]:
        return {
            "status": "blocked",
            "stage": "output_guardrail",
            "category": output_result["category"],
            "message": output_result["message"],
            "response": None
        }
    # ========================================================
    # STEP 4
    # SUCCESS
    # ========================================================
    return {
        "status": "success",
        "stage": "completed",
        "category": "SAFE",
        "message": (
            "Response generated successfully."
        ),
        "response": model_response
    }

# run app use this command =uvicorn app:app --reload
# stop app: pkill -f "uvicorn app:app"