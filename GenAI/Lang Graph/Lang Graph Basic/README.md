# LangGraph Basic Tutorials

This directory contains foundational tutorials and examples for learning **LangGraph**, a powerful framework for building applications with Large Language Models (LLMs). LangGraph allows you to create complex, multi-step AI workflows and state machines.

---

## 📚 Programs Overview

### 1. **BMI Calculator** 
- **File:** `1_BMI_Calculator.ipynb`
- **Description:** A beginner-friendly introduction to LangGraph using a simple BMI (Body Mass Index) calculator. This notebook demonstrates how to:
  - Create basic LLM chains
  - Accept user input (height and weight)
  - Process calculations through an AI model
  - Display results in a structured format
- **Key Concepts:** Basic chain setup, LLM integration, input/output handling
- **Use Case:** Perfect for understanding the fundamentals of LangGraph workflows

---

### 2. **BMI Calculator with Category Classification**
- **File:** `2_BMI_Calculator_Category.ipynb`
- **Description:** An extension of the BMI calculator that adds intelligent categorization. This notebook shows how to:
  - Calculate BMI values
  - Use LLM to classify BMI results (Underweight, Normal, Overweight, Obese, etc.)
  - Create conditional logic based on LLM responses
  - Enhance user-facing feedback with categorization
- **Key Concepts:** Conditional workflows, LLM-based decision making, output parsing
- **Use Case:** Learning how to add intelligent decision-making to your LLM applications

---

### 3. **LLM Question Answering System**
- **File:** `3_LLM_QA.ipynb`
- **Description:** A straightforward Q&A system built with LangGraph that demonstrates:
  - Creating a question-answering pipeline
  - Context handling for better responses
  - Multi-turn conversation capabilities
  - Answer generation and formatting
- **Key Concepts:** Conversation chains, context management, QA workflows
- **Use Case:** Foundation for building chatbots and information retrieval systems

---

### 4. **Prompt Chaining**
- **File:** `4_Prompt Chaining.ipynb`
- **Description:** An exploration of advanced prompt chaining techniques where multiple LLM calls are connected sequentially. This notebook covers:
  - Breaking down complex problems into multiple steps
  - Passing outputs from one step as inputs to the next
  - Building multi-stage reasoning workflows
  - Handling dependencies between LLM calls
  - Error handling and fallback mechanisms
- **Key Concepts:** Sequential processing, prompt engineering, multi-stage workflows
- **Use Case:** Complex tasks like content generation, data transformation, and multi-step reasoning

---

### 5. **Cricket Statistics - Parallel Workflow**
- **File:** `5_Cricket_Parallel_workflow.ipynb`
- **Description:** Demonstrates parallel processing in LangGraph using cricket statistics as a domain example. This notebook illustrates:
  - Running multiple LLM tasks simultaneously
  - Aggregating results from parallel operations
  - Performance optimization through parallelization
  - Handling multiple independent sub-tasks
- **Key Concepts:** Parallel execution, async operations, result aggregation, workflow optimization
- **Use Case:** Processing multiple independent tasks concurrently for improved performance

---

### 6. **Essay Evaluation with Parallelization**
- **File:** `6_Evaluate_Essay_parallelization_workflow.ipynb`
- **Description:** An advanced example using LangGraph to evaluate essays through multiple parallel evaluation criteria. This notebook demonstrates:
  - Creating parallel evaluation nodes (grammar, content quality, structure, etc.)
  - Running multiple LLM evaluators simultaneously
  - Combining parallel results into comprehensive feedback
  - Scoring and aggregating evaluations
  - Providing detailed, multi-faceted feedback
- **Key Concepts:** Advanced parallelization, multi-criterion evaluation, result synthesis, workflow orchestration
- **Use Case:** Building sophisticated evaluation systems, AI-powered feedback systems, and quality assessment tools

---

## 🎯 Learning Path

1. **Start Here:** `1_BMI_Calculator.ipynb` - Get comfortable with basic LangGraph concepts
2. **Next:** `2_BMI_Calculator_Category.ipynb` - Add conditional logic and decision-making
3. **Then:** `3_LLM_QA.ipynb` - Build conversational systems
4. **Advanced:** `4_Prompt Chaining.ipynb` - Master sequential multi-step workflows
5. **Performance:** `5_Cricket_Parallel_workflow.ipynb` - Learn parallel execution
6. **Expert:** `6_Evaluate_Essay_parallelization_workflow.ipynb` - Build complex systems with parallelization

---

## 🛠️ Prerequisites

- Python 3.8+
- LangGraph library
- LLM API keys (OpenAI, Anthropic, or your preferred provider)
- Jupyter Notebook or similar environment

---

## 📖 Key Concepts Covered

| Concept | Notebooks |
|---------|-----------|
| Basic LLM Chains | 1, 2, 3 |
| Conditional Logic | 2 |
| Multi-turn Conversations | 3 |
| Prompt Chaining | 4 |
| Sequential Workflows | 4 |
| Parallel Execution | 5, 6 |
| Result Aggregation | 5, 6 |
| Workflow Orchestration | 5, 6 |

---

## 🚀 Quick Start

1. Clone or download this repository
2. Install required dependencies: `pip install langgraph langchain`
3. Set up your LLM API keys
4. Open any notebook in Jupyter and run the cells sequentially
5. Follow the comments and explanations in each notebook

---

## 📝 Notes

- Each notebook is standalone and can be run independently
- Comments and markdown cells provide detailed explanations
- Modify parameters and prompts to experiment and learn
- Check the `image` folder for any diagrams or references

---

## 🤝 Contributing

Feel free to extend these examples with additional use cases, optimizations, or variations!

---

**Created:** 2026 | **Language:** Python | **Framework:** LangGraph
