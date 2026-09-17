# LangGraph Basic Tutorials

This directory contains foundational tutorials and examples for learning **LangGraph**, a powerful framework for building applications with Large Language Models (LLMs). LangGraph allows you to create structured workflows that combine programmatic logic and (optionally) LLM calls to solve real-world tasks. The notebooks here progress from simple, non-LLM examples to advanced, LLM-powered orchestration patterns.

---

## 📚 Programs Overview

### 1. **BMI Calculator** 
- **File:** `1_BMI_Calculator.ipynb`
- **Description:** A beginner-friendly introduction to LangGraph using a simple BMI (Body Mass Index) calculator. This notebook demonstrates how to:
   - Create basic workflows without LLM calls
   - Accept user input (height and weight)
   - Process mathematical calculations 
   - Display results in a structured format
- **Key Concepts:** Basic workflow setup, input/output handling, data processing
- **Use Case:** Perfect for understanding the fundamentals of LangGraph workflows without LLM integration
- **Uses LLM:** ❌ No

---

### 2. **BMI Calculator with Category Classification**
- **File:** `2_BMI_Calculator_Category.ipynb`
- **Description:** An extension of the BMI calculator that adds intelligent categorization using conditional logic. This notebook shows how to:
   - Calculate BMI values
   - Use conditional logic to classify BMI results (Underweight, Normal, Overweight, Obese)
   - Create multi-step workflows with sequential decision-making
   - Return categorized results based on calculated values
- **Key Concepts:** Conditional workflows, sequential node execution, output classification
- **Use Case:** Learning how to add intelligent decision-making to your LangGraph applications without requiring external API calls
- **Uses LLM:** ❌ No

---

### 3. **LLM Question Answering System**
- **File:** `3_LLM_QA.ipynb`
- **Description:** A straightforward Q&A system built with LangGraph that demonstrates:
   - Creating a question-answering pipeline with LLM
   - Context handling for better responses
   - Multi-turn conversation capabilities
   - Answer generation and formatting by LLM
- **Key Concepts:** Conversation chains, context management, QA workflows, LLM integration
- **Use Case:** Foundation for building chatbots and information retrieval systems
- **Uses LLM:** ✅ Yes

---

### 4. **Prompt Chaining**
- **File:** `4_Prompt Chaining.ipynb`
- **Description:** An exploration of advanced prompt chaining techniques where multiple LLM calls are connected sequentially. This notebook covers:
   - Breaking down complex problems into multiple steps (e.g., outline generation → blog content generation)
   - Passing outputs from one LLM call as inputs to the next
   - Building multi-stage reasoning workflows
   - Handling dependencies between LLM calls
   - Generating comprehensive blog posts from titles using structured workflows
- **Key Concepts:** Sequential processing, prompt engineering, multi-stage workflows, LLM orchestration
- **Use Case:** Complex tasks like content generation, data transformation, and multi-step reasoning
- **Uses LLM:** ✅ Yes

---

### 5. **Cricket Statistics - Parallel Workflow**
- **File:** `5_Cricket_Parallel_workflow.ipynb`
- **Description:** Demonstrates parallel processing in LangGraph using cricket statistics as a domain example. This notebook illustrates:
   - Running multiple independent calculations simultaneously (Strike Rate, Balls per Boundary, Boundary Percentage)
   - Aggregating results from parallel operations
   - Performance optimization through parallelization
   - Handling multiple independent sub-tasks without LLM calls
- **Key Concepts:** Parallel execution, result aggregation, workflow optimization, independent task processing
- **Use Case:** Processing multiple independent calculations concurrently for improved performance
- **Uses LLM:** ❌ No

---

### 6. **Essay Evaluation with Parallelization**
- **File:** `6_Evaluate_Essay_parallelization_workflow.ipynb`
- **Description:** An advanced example using LangGraph to evaluate essays through multiple parallel evaluation criteria with LLM. This notebook demonstrates:
   - Creating parallel evaluation nodes (Clarity of Thought, Depth of Analysis, Language Quality)
   - Running multiple LLM evaluators simultaneously for different criteria
   - Combining parallel results into comprehensive feedback
   - Scoring and aggregating LLM-based evaluations
   - Calculating final scores based on multiple evaluation dimensions
   - Providing detailed, multi-faceted LLM-generated feedback
- **Key Concepts:** Advanced parallelization, multi-criterion LLM evaluation, result synthesis, reducer functions, workflow orchestration
- **Use Case:** Building sophisticated evaluation systems, AI-powered feedback systems, and quality assessment tools
- **Uses LLM:** ✅ Yes

---

### 7. **Quadratic Equation - Conditional Workflow (Without LLM)**
- **File:** `7_Quadratic Equation Conditional Workflow (Without LLM).ipynb`
- **Description:** Demonstrates conditional workflows using a quadratic equation solver as the domain example. This notebook shows how to:
   - Compute the discriminant and determine the nature of roots (real & distinct, real & equal, complex)
   - Use conditional nodes to route execution based on discriminant
   - Return formatted solutions for different root types
   - Build workflows that require decision logic but do not call an LLM
- **Key Concepts:** Conditional routing, numeric processing, branching workflows
- **Use Case:** Educational example for decision-making in LangGraph workflows without external APIs
- **Uses LLM:** ❌ No

---

### 8. **LLM-Based Review Handling Conditional Workflow**
- **File:** `8_LLM Based Review handling conditional workflow.ipynb`
- **Description:** An example of conditional workflows that incorporate LLMs to handle review and moderation style tasks. This notebook demonstrates:
   - Using LLMs to generate or evaluate textual reviews
   - Routing outputs based on LLM-evaluated criteria (e.g., pass/fail, accept/reject, needs revision)
   - Combining programmatic checks with LLM judgments in conditional branches
   - Producing final structured recommendations based on combined signals
- **Key Concepts:** Conditional workflows, LLM evaluation & routing, hybrid programmatic+LLM decision logic
- **Use Case:** Moderation pipelines, review automation, and adaptive content workflows
- **Uses LLM:** ✅ Yes

---

## 🎯 Learning Path

1. **Start Here:** `1_BMI_Calculator.ipynb` - Get comfortable with basic LangGraph concepts
2. **Next:** `2_BMI_Calculator_Category.ipynb` - Add conditional logic and multi-step workflows
3. **Then:** `3_LLM_QA.ipynb` - Build conversational systems with LLM
4. **Advanced:** `4_Prompt Chaining.ipynb` - Master sequential multi-step LLM workflows
5. **Performance:** `5_Cricket_Parallel_workflow.ipynb` - Learn parallel execution patterns without LLM
6. **Expert:** `6_Evaluate_Essay_parallelization_workflow.ipynb` - Build complex systems with parallel LLM processing
7. **Conditional Workflows (Non-LLM):** `7_Quadratic Equation Conditional Workflow (Without LLM).ipynb`
8. **Conditional Workflows (LLM):** `8_LLM Based Review handling conditional workflow.ipynb`

---

## 🛠️ Prerequisites

- Python 3.8+
- LangGraph library
- LLM API keys (OpenAI, Anthropic, Ollama, or your preferred provider) - *required for programs 3, 4, 6, and 8*
- Jupyter Notebook or similar environment

---

## 📖 Key Concepts Covered

| Concept | Notebooks | Uses LLM |
|---------|-----------|----------|
| Basic Workflows | 1, 5 | ❌ No |
| Conditional Logic | 2, 7, 8 | 2,7: ❌ No, 8: ✅ Yes |
| LLM Integration | 3, 4, 6, 8 | ✅ Yes |
| Multi-turn Conversations | 3 | ✅ Yes |
| Prompt Chaining | 4 | ✅ Yes |
| Sequential Workflows | 2, 4 | 2: ❌ No, 4: ✅ Yes |
| Parallel Execution | 5, 6 | 5: ❌ No, 6: ✅ Yes |
| Result Aggregation | 5, 6 | 5: ❌ No, 6: ✅ Yes |
| Workflow Orchestration | 2, 5, 6, 8 | 2: ❌ No, 5: ❌ No, 6: ✅ Yes, 8: ✅ Yes |

---

## 🚀 Quick Start

1. Clone or download this repository
2. Install required dependencies: `pip install langgraph langchain`
3. For LLM-based notebooks, set up your API keys:
   - **OpenAI:** `export OPENAI_API_KEY="your-key"`
   - **Ollama (Local):** `pip install langchain_ollama`
   - **Google Generative AI:** `pip install langchain_google_genai`
4. Open any notebook in Jupyter and run the cells sequentially
5. Follow the comments and explanations in each notebook

---

## 📝 Notes

- Each notebook is standalone and can be run independently
- Comments and markdown cells provide detailed explanations
- **No LLM Required:** Programs 1, 2, 5, and 7 do NOT require LLM API keys
- **LLM Required:** Programs 3, 4, 6, and 8 require active LLM API credentials
- Modify parameters and prompts to experiment and learn
- Check the `image` folder for any diagrams or references

---

## 🤝 Contributing

Feel free to extend these examples with additional use cases, optimizations, or variations!

---

**Created:** 2026 | **Language:** Python | **Framework:** LangGraph
