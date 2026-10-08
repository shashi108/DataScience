// ============================================================
// ELEMENTS
// ============================================================

const promptElement =
    document.getElementById("prompt");

const sendButton =
    document.getElementById("sendButton");

const statusBox =
    document.getElementById("statusBox");

const securityBox =
    document.getElementById("securityBox");

const responseBox =
    document.getElementById("responseBox");

const responseText =
    document.getElementById("responseText");

const characterCount =
    document.getElementById("characterCount");


// Pipeline elements

const stepInput =
    document.getElementById("stepInput");

const stepGemini =
    document.getElementById("stepGemini");

const stepOutput =
    document.getElementById("stepOutput");

const stepResponse =
    document.getElementById("stepResponse");


// Security details

const stageValue =
    document.getElementById("stageValue");

const categoryValue =
    document.getElementById("categoryValue");

const messageValue =
    document.getElementById("messageValue");


// ============================================================
// CHARACTER COUNT
// ============================================================

promptElement.addEventListener(
    "input",
    function () {

        characterCount.innerText =
            promptElement.value.length;

    }
);


// ============================================================
// SEND PROMPT
// ============================================================

async function sendPrompt() {

    const prompt =
        promptElement.value.trim();


    // --------------------------------------------------------
    // Validate empty input on frontend
    // --------------------------------------------------------

    if (!prompt) {

        showStatus(
            "blocked",
            "🚫 Please enter a prompt."
        );

        resetPipeline();

        return;
    }


    // --------------------------------------------------------
    // Reset UI
    // --------------------------------------------------------

    resetPipeline();


    responseBox.className =
        "response hidden";


    securityBox.className =
        "security-box hidden";


    responseText.innerText =
        "";


    // --------------------------------------------------------
    // Disable button
    // --------------------------------------------------------

    sendButton.disabled = true;

    sendButton.innerText =
        "Processing...";


    // --------------------------------------------------------
    // Input Guardrail
    // --------------------------------------------------------

    stepInput.classList.add(
        "active"
    );


    showStatus(
        "success",
        "🛡️ Checking input guardrail..."
    );


    try {

        // ----------------------------------------------------
        // API REQUEST
        // ----------------------------------------------------

        const response =
            await fetch(
                "/generate",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        prompt: prompt
                    })
                }
            );


        // ----------------------------------------------------
        // HTTP ERROR
        // ----------------------------------------------------

        if (!response.ok) {

            throw new Error(
                "Server returned an error."
            );

        }


        // ----------------------------------------------------
        // JSON
        // ----------------------------------------------------

        const data =
            await response.json();


        // ====================================================
        // INPUT GUARDRAIL BLOCKED
        // ====================================================

        if (
            data.status === "blocked" &&
            data.stage === "input_guardrail"
        ) {

            stepInput.classList.remove(
                "active"
            );

            stepInput.classList.add(
                "blocked"
            );


            showStatus(
                "blocked",
                "🚫 Input blocked by guardrail."
            );


            showSecurityResult(
                data.stage,
                data.category,
                data.message
            );


            sendButton.disabled = false;

            sendButton.innerText =
                "🚀 Send Prompt";


            return;
        }


        // ====================================================
        // GEMINI
        // ====================================================

        stepInput.classList.remove(
            "active"
        );

        stepInput.classList.add(
            "success"
        );


        stepGemini.classList.add(
            "active"
        );


        showStatus(
            "success",
            "🤖 Gemini is generating a response..."
        );


        // ====================================================
        // OUTPUT GUARDRAIL
        // ====================================================

        stepGemini.classList.remove(
            "active"
        );

        stepGemini.classList.add(
            "success"
        );


        stepOutput.classList.add(
            "active"
        );


        // ====================================================
        // OUTPUT BLOCKED
        // ====================================================

        if (
            data.status === "blocked" &&
            data.stage === "output_guardrail"
        ) {

            stepOutput.classList.remove(
                "active"
            );

            stepOutput.classList.add(
                "blocked"
            );


            showStatus(
                "blocked",
                "🚫 Output blocked by guardrail."
            );


            showSecurityResult(
                data.stage,
                data.category,
                data.message
            );


            sendButton.disabled = false;

            sendButton.innerText =
                "🚀 Send Prompt";


            return;
        }


        // ====================================================
        // SUCCESS
        // ====================================================

        stepOutput.classList.remove(
            "active"
        );

        stepOutput.classList.add(
            "success"
        );


        stepResponse.classList.add(
            "success"
        );


        showStatus(
            "success",
            "✅ Response passed all guardrails."
        );


        showSecurityResult(
            data.stage,
            data.category,
            data.message
        );


        responseBox.className =
            "response";


        responseText.innerText =
            data.response || "";


    }

    catch (error) {

        console.error(error);


        showStatus(
            "error",
            "❌ Unable to connect to the server."
        );

    }


    finally {

        sendButton.disabled = false;

        sendButton.innerText =
            "🚀 Send Prompt";

    }

}


// ============================================================
// SHOW STATUS
// ============================================================

function showStatus(
    type,
    message
) {

    statusBox.className =
        "status " + type;

    statusBox.innerText =
        message;

}


// ============================================================
// SHOW SECURITY RESULT
// ============================================================

function showSecurityResult(
    stage,
    category,
    message
) {

    securityBox.className =
        "security-box";


    stageValue.innerText =
        formatText(stage);


    categoryValue.innerText =
        category;


    messageValue.innerText =
        message;

}


// ============================================================
// FORMAT TEXT
// ============================================================

function formatText(text) {

    if (!text) {

        return "-";

    }


    return text
        .replaceAll("_", " ")
        .toUpperCase();

}


// ============================================================
// RESET PIPELINE
// ============================================================

function resetPipeline() {

    const steps = [
        stepInput,
        stepGemini,
        stepOutput,
        stepResponse
    ];


    steps.forEach(
        function (step) {

            step.classList.remove(
                "active",
                "success",
                "blocked"
            );

        }
    );


    statusBox.className =
        "status hidden";


    securityBox.className =
        "security-box hidden";

}