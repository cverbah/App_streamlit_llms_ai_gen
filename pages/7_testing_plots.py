import streamlit as st
import pandas as pd
import io
import contextlib
import matplotlib.pyplot as plt


# Function to execute the code snippet
def execute_code(snippet, df: pd.DataFrame):
    # Strip the code snippet
    code = snippet.strip().strip('```python').strip('```').strip()

    # Define a local scope dictionary to pass to exec()
    local_vars = {'df': df, 'plt': plt}

    # Redirect standard output to capture `print()` statements
    output_capture = io.StringIO()
    try:
        with contextlib.redirect_stdout(output_capture):
            exec(code, globals(), local_vars)
        # Get the captured output
        output = output_capture.getvalue()
        return local_vars, output
    except Exception as e:
        # Handle and display any errors
        return {}, f"Error: {e}"


# Streamlit App
st.title("Dynamic Execution and Plotting of Python Code Snippet")

# Sample DataFrame for demonstration
data = {
    'nombre del producto': ['Producto A', 'Producto B', 'Producto C', 'Producto D', 'Producto E', 'Producto F'],
    'categoría': ['gato', 'gato', 'perro', 'gato', 'perro', 'gato'],
    'best for pets precio final': [10.99, 15.49, 8.99, 20.00, 13.25, 18.75]
}
df = pd.DataFrame(data)

# Display the sample DataFrame
st.write("Sample DataFrame:")
st.dataframe(df)

# Input for the code snippet
code_snippet = st.text_area("Enter your code snippet:", """```python
df_gatos = df[df['categoría'] == 'gato'].copy()
df_gatos_sorted = df_gatos.sort_values(by=['best for pets precio final'], ascending=False)
top_5_gatos = df_gatos_sorted.head(5)

# Plotting
plt.figure(figsize=(10, 6))
plt.bar(top_5_gatos['nombre del producto'], top_5_gatos['best for pets precio final'])
plt.xlabel('Nombre del Producto')
plt.ylabel('Precio Final')
plt.title('Top 5 Productos para Gatos')
plt.grid(True)
plt.show()
```""")

# Button to execute the code
if st.button("Execute Code"):
    # Execute the stripped code and capture the result
    local_vars, output = execute_code(code_snippet, df)

    # Display the captured output from print statements
    st.write("Captured Output:")
    st.text(output)

    # Display the plot
    if 'plt' in local_vars:
        st.write("Generated Plot:")
        st.pyplot(local_vars['plt'].gcf())

    # Optionally, display the resulting DataFrame if created
    if 'top_5_gatos' in local_vars:
        st.write("Top 5 Gatos DataFrame 'top_5_gatos':")
        st.dataframe(local_vars['top_5_gatos'])