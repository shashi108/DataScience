# LangGraph Basic Tutorials

This directory contains a practical set of beginner-to-advanced notebooks for learning and experimenting with LangGraph, a framework for building stateful, graph-based workflows around Large Language Models (LLMs).

The examples in this folder progressively cover:
- basic workflow construction,
- conditional logic,
- parallel execution,
- prompt chaining,
- iterative generation,
- LLM-powered Q&A,
- chatbot workflows,
- persistence and UI-based application patterns.

---

## Contents Overview

| No. | Notebook | Focus Area | Uses LLM |
|-----|----------|------------|----------|
| 1 | `1_BMI_Calculator.ipynb` | Basic workflow and calculation logic | No |
| 2 | `2_BMI_Calculator_Category.ipynb` | Conditional classification logic | No |
| 3 | `3_LLM_QA.ipynb` | Q&A workflow with LLM | Yes |
| 4 | `4_Prompt Chaining.ipynb` | Sequential prompt chaining | Yes |
| 5 | `5_Cricket_Parallel_workflow.ipynb` | Parallel task execution | No |
| 6 | `6_Evaluate_Essay_parallelization_workflow.ipynb` | Parallel LLM evaluation | Yes |
| 7 | `7_Quadratic Equation Conditional Workflow (Without LLM).ipynb` | Branching logic without LLM | No |
| 8 | `8_LLM Based Review handling conditional workflow.ipynb` | Conditional LLM routing and review handling | Yes |
| 9 | `9_Iterative work flow_generate tweet.ipynb` | Iterative generation workflow | Yes |
| 10 | `10_Chatbot_without Persistance.ipynb` | Stateless chatbot example | Yes |
| 11 | `11_Chatbot_with Persistance.ipynb` | Stateful chatbot with persistence | Yes |
| 12 | `12_Chatbot_Case Study_With_UI.ipynb` | Chatbot UI case study | Yes |

Additional folders:
- `chatbot_LLM/` - chatbot-related assets and supporting materials
- `image/` - images and diagram references for visual understanding

---

## Notebook Details

### 1. BMI Calculator
- File: `1_BMI_Calculator.ipynb`
- Description: A beginner-friendly LangGraph example that calculates BMI from user inputs and returns structured output.
- Concepts: basic graph nodes, input handling, workflow execution.
- Use case: building your first workflow without an LLM.

### 2. BMI Calculator with Category Classification
- File: `2_BMI_Calculator_Category.ipynb`
- Description: Extends the BMI calculator with conditional logic to classify results into categories such as underweight, normal, overweight, and obese.
- Concepts: branching, decision-based execution, workflow routing.

### 3. LLM Question Answering System
- File: `3_LLM_QA.ipynb`
- Description: Introduces LLM-based question-answering with a conversational workflow.
- Concepts: LLM integration, context handling, answer generation.

### 4. Prompt Chaining
- File: `4_Prompt Chaining.ipynb`
- Description: Demonstrates multistage prompt chaining where one LLM call feeds into the next.
- Concepts: sequential processing, prompt engineering, multi-step orchestration.

### 5. Cricket Statistics Parallel Workflow
- File: `5_Cricket_Parallel_workflow.ipynb`
- Description: Shows how multiple independent calculations can run in parallel.
- Concepts: parallel execution, aggregation, performance optimization.

### 6. Essay Evaluation with Parallelization
- File: `6_Evaluate_Essay_parallelization_workflow.ipynb`
- Description: Evaluates an essay using multiple parallel criteria and combines the results into a final assessment.
- Concepts: parallel LLM judges, aggregation, scoring systems.

### 7. Quadratic Equation Conditional Workflow (Without LLM)
- File: `7_Quadratic Equation Conditional Workflow (Without LLM).ipynb`
- Description: Builds a conditional workflow for solving quadratic equations based on the discriminant.
- Concepts: branching logic, mathematical computation, decision routing.

### 8. LLM-Based Review Handling Conditional Workflow
- File: `8_LLM Based Review handling conditional workflow.ipynb`
- Description: Uses LLM-based decision logic to handle reviews or moderation-style tasks based on conditional routing.
- Concepts: conditional branching, hybrid logic, review automation.

### 9. Iterative Workflow for Tweet Generation
- File: `9_Iterative work flow_generate tweet.ipynb`
- Description: Demonstrates iterative refinement in a workflow that generates and improves tweet content.
- Concepts: iteration, feedback loops, generation quality improvement.

### 10. Chatbot without Persistence
- File: `10_Chatbot_without Persistance.ipynb`
- Description: A simple chatbot example without remembering past conversation state.
- Concepts: stateless conversation handling, LLM interaction.

### 11. Chatbot with Persistence
- File: `11_Chatbot_with Persistance.ipynb`
- Description: Builds on the chatbot idea by adding persistence so the application retains memory across interactions.
- Concepts: conversation memory, storage, stateful chat apps.

### 12. Chatbot Case Study with UI
- File: `12_Chatbot_Case Study_With_UI.ipynb`
- Description: A practical chatbot case study with a user interface and more realistic application flow.
- Concepts: app integration, UI, real-world chatbot patterns.

---

## Learning Path

A suggested order to work through this folder:

1. `1_BMI_Calculator.ipynb` — start with basic graphs and node logic
2. `2_BMI_Calculator_Category.ipynb` — learn conditional routing
3. `3_LLM_QA.ipynb` — connect LangGraph with LLMs
4. `4_Prompt Chaining.ipynb` — explore multi-step LLM tasks
5. `5_Cricket_Parallel_workflow.ipynb` — understand parallel execution
6. `6_Evaluate_Essay_parallelization_workflow.ipynb` — advanced parallel LLM orchestration
7. `7_Quadratic Equation Conditional Workflow (Without LLM).ipynb` — branching logic without external models
8. `8_LLM Based Review handling conditional workflow.ipynb` — conditional LLM routing
9. `9_Iterative work flow_generate tweet.ipynb` — iterative generation workflows
10. `10_Chatbot_without Persistance.ipynb` — basic chatbot flow
11. `11_Chatbot_with Persistance.ipynb` — stateful conversations
12. `12_Chatbot_Case Study_With_UI.ipynb` — practical full application pattern

---

## Prerequisites

- Python 3.8+
- Jupyter Notebook or JupyterLab
- `langgraph`
- `langchain` or model-specific integrations
- LLM provider credentials for notebooks using LLMs

Typical installation:

```bash
pip install langgraph langchain
```

For LLM-based notebooks, you may also need provider-specific packages such as:

```bash
pip install langchain_openai
```

or other integrations depending on your chosen model provider.

---

## Quick Start

1. Clone or download this repository.
2. Open the folder `GenAI/Lang Graph/Lang Graph Basic`.
3. Launch Jupyter Notebook or JupyterLab.
4. Open any notebook and run the cells sequentially.
5. For LLM-based examples, ensure your environment variables or API keys are configured before execution.

Example environment variable for OpenAI:

```bash
export OPENAI_API_KEY="your-api-key"
```

---

## Key Concepts Covered

- Basic workflow creation
- Conditional routing
- Multi-step orchestration
- Prompt chaining
- Parallel execution
- Iterative refinement
- Stateful memory / persistence
- Chatbot application patterns
- LLM evaluation and summarization

---

## Notes

- Each notebook is designed to be mostly standalone.
- Some notebooks require LLM API access and may not run without configured credentials.
- Non-LLM notebooks are useful for understanding LangGraph flow design before adding model interactions.
- Use the `image` directory for visual references and diagrams.

---

## Contributing

Feel free to extend this collection with more examples, improvements, or advanced LangGraph use cases.

---

Created: 2026
Framework: LangGraph
Language: Python
