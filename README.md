
# E-commerce Sales Dashboard with LLM Integration

This project leverages the LangChain library and Google's LLM to generate detailed sales reports based on e-commerce data. The data includes customer profiles and purchase history, and the interface is built using Streamlit.

![streamlit](https://github.com/user-attachments/assets/e5b669df-ac49-4090-b2fd-8398206cd10a)

## Features

### Interactive Streamlit Dashboard:
1. **Filters**:
   - Select department(s) from the e-commerce data.
   - Filter by state(s) where purchases were made.
   - Choose an age range for customer segmentation.
   
2. **Report Options**:
   - Select the language for the report:
     - English
     - Portuguese
     - Spanish
     - French
     - German
   - Pick one or more analyses to include in the report:
     - Sales performance by department.
     - Revenue analysis by state.
     - Customer demographic trends.
     - Profitability by sales channel.
     - Key insights and recommendations.

3. **Dynamic Report Generation**:
   - Uses Google's LLM to generate detailed reports based on selected filters and analysis options.
   - Displays the generated report in the dashboard.

### Performance Optimizations:
- Cached data loading to minimize repeated read operations from Excel files.
- Cached LLM responses for faster subsequent report generation.
- Efficient data filtering and merging for a smoother user experience.

## Requirements
- Python (3.8 or higher)
- Anaconda (for virtual environment management)

## Setup Instructions
1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. Create a virtual environment using Anaconda:
   ```bash
   conda create --name ecommerce_env python=3.9
   conda activate ecommerce_env
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add your Google API Key:
   - Create a `config.yaml` file in the project root with the following content:
     ```yaml
     GOOGLE_API_KEY: 'your_google_api_key_here'
     ```

5. Run the application:
   ```bash
   streamlit run app.py
   ```

## Project Structure
- **app.py**: Main application script.
- **data_base_ecommerce.xlsx**: The dataset for the e-commerce platform.
- **config.yaml**: Configuration file for the API key.
- **requirements.txt**: Contains all dependencies for the project.
