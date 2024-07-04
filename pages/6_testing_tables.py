import streamlit as st
import pandas as pd
import io
import contextlib

# Set the title of the app
st.title("Test tables Python Code Snippet")

# Create a sample DataFrame for demonstration
data = {
    'nombre del producto': ['Producto A', 'Producto B', 'Producto C', 'Producto D', 'Producto E', 'Producto F'],
    'categoría': ['gato', 'gato', 'perro', 'gato', 'perro', 'gato'],
    'best for pets precio final': [10.99, 15.49, 8.99, 20.00, 13.25, 18.75]
}
df = pd.DataFrame(data)
st.write("Sample DataFrame:")
st.dataframe(df)


code_snippet = st.text_area("Enter your code snippet:", """```python
df_gatos = df[df['categoría'] == 'gato'].copy()
df_gatos_sorted = df_gatos.sort_values(by=['best for pets precio final'], ascending=False)
top_5_gatos = df_gatos_sorted.head(5)
print(top_5_gatos[['nombre del producto', 'best for pets precio final']])
```""")


# Function to strip and execute the code
def execute_code(snippet, df):
    # Strip the code snippet
    code = snippet.strip().strip('```python').strip('```').strip()
    local_vars = {'df': df}
    # Redirect standard output to capture `print()` statements
    output_capture = io.StringIO()
    try:
        with contextlib.redirect_stdout(output_capture):
            exec(code, globals(), local_vars)
        output = output_capture.getvalue()
        return local_vars, output
    except Exception as e:
        return {}, f"Error: {e}"


if st.button("Execute Code"):
    local_vars, output = execute_code(code_snippet, df)

    st.write("Captured Output:")
    st.text(output)

    if 'top_5_gatos' in local_vars:
        st.write("Resulting DataFrame 'top_5_gatos':")
        st.dataframe(local_vars['top_5_gatos'])