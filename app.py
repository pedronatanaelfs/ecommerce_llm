import os
import yaml
import streamlit as st
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# Load API key from config.yaml
with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)
os.environ["GOOGLE_API_KEY"] = config["GOOGLE_API_KEY"]

# Initialize Google AI model
googleai = ChatGoogleGenerativeAI(model="gemini-pro")

# Define prompt template
template = """
You are a data analyst specialized in e-commerce analysis.
Your task is to write a comprehensive sales report for the selected Brazilian state(s): {state}.

The report must include the following:
1. **Introduction**:
   - Provide a summary of the dataset and its scope.
   - Mention the key focus areas of the analysis.

2. **Data Overview**:
   - Present a table summarizing the main metrics for the purchases:
     - Total number of purchases.
     - Average purchase value (with and without shipping).
     - Total revenue generated.
   - Provide a table showing customer demographics:
     - Age distribution (minimum, maximum, mean).
     - Income distribution (minimum, maximum, mean).
     - States of birth distribution.

3. **Detailed Analyses**:
   {analyses}

4. **Visualizations (Text Description)**:
   - Suggest how the data could be visualized (e.g., bar charts, line graphs, pie charts) for each analysis performed.

5. **Insights and Conclusions**:
   - Highlight key trends and patterns observed in the data.
   - Include actionable insights for business decision-making.

### Notes:
- Use only the data provided in the following tables:
1. Purchases Table:
{purchases_table}

2. Customers Table:
{customers_table}

- Present all numerical summaries in tables when applicable.
- Ensure the report is written in {language}.

"""

prompt_template = PromptTemplate.from_template(template=template)

# Function to load data with caching
@st.cache_data
def load_data(file_path, sheet_name):
    return pd.read_excel(file_path, sheet_name=sheet_name)

# Load data using cached function
data_path = "data_base_ecommerce.xlsx"
purchase_data = load_data(data_path, "base compra")
customer_data = load_data(data_path, "Base cliente")

# Streamlit interface
st.title("E-commerce Sales Dashboard with LLM Integration")

# Sidebar filters
st.sidebar.header("Filters")
selected_department = st.sidebar.multiselect(
    "Select Department", purchase_data["Nome_Departamento"].unique()
)
selected_state = st.sidebar.multiselect(
    "Select Brazilian State", purchase_data["estado"].unique()
)
selected_age_range = st.sidebar.slider("Select Age Range", 18, 100, (18, 100))

# User input for report generation
st.sidebar.header("Report Options")
language = st.sidebar.selectbox(
    "Select Language", ["English", "Portuguese", "Spanish", "French", "German"]
)
analyses = st.sidebar.multiselect(
    "Select Analyses",
    [
        "Sales performance by department",
        "Revenue analysis by state",
        "Customer demographic trends",
        "Profitability by sales channel",
        "Key insights and recommendations",
    ],
    default=["Sales performance by department", "Revenue analysis by state"],
)

# Button for generating report
if st.button("Generate Report"):
    st.write("Generating report...")

    # Combine filtered data for analysis
    filtered_data = purchase_data[
        (purchase_data["Nome_Departamento"].isin(selected_department))
        & (purchase_data["estado"].isin(selected_state))
    ]
    combined_data = pd.merge(
        filtered_data, customer_data, left_on="cliente_Log", right_on="cliente_Log"
    )
    combined_filtered = combined_data[
        (combined_data["idade"] >= selected_age_range[0])
        & (combined_data["idade"] <= selected_age_range[1])
    ]

    # Prepare preview of the data
    purchases_preview = filtered_data.head(5).to_string(index=False)
    customers_preview = customer_data.head(5).to_string(index=False)

    # Prepare prompt for LLM
    states_text = ", ".join(selected_state)
    analyses_text = "\n".join([f"- {analysis}" for analysis in analyses])
    prompt = prompt_template.format(
        state=states_text,
        language=language,
        analyses=analyses_text,
        purchases_table=purchases_preview,
        customers_table=customers_preview,
    )

    # Invoke LLM for generating the report
    response = googleai.invoke(prompt)

    # Display the generated report
    st.subheader("Generated Sales Report")
    st.write(response.content)
