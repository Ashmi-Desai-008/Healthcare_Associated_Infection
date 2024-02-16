import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def main():
    st.title('Healthcare Associated Infections Analysis')
    st.sidebar.title('Filters')

    # Load the dataset with specified encoding
    def load_data():
        try:
            data = pd.read_csv('Healthcare_Associated_Infections-Hospital.csv', encoding='ISO-8859-1')  
            # Convert 'Score' column to numeric
            data['Score'] = pd.to_numeric(data['Score'], errors='coerce')
            return data
        except Exception as e:
            st.error(f"Error loading dataset: {e}")
            return None

    data = load_data()

    if data is not None:
        # Display the dataset
        st.write('### Dataset')
        st.write(data)

        # Filter by state
        selected_state = st.sidebar.selectbox('Select State', data['State'].unique())
        filtered_data = data[data['State'] == selected_state]

        # Check if 'Score' column exists and is numeric
        if 'Score' in filtered_data.columns and pd.api.types.is_numeric_dtype(filtered_data['Score']):
            # Filter by score
            min_score, max_score = st.sidebar.slider('Select Score Range', min_value=filtered_data['Score'].min(), max_value=filtered_data['Score'].max(), value=(filtered_data['Score'].min(), filtered_data['Score'].max()))
            filtered_data = filtered_data[(filtered_data['Score'] >= min_score) & (filtered_data['Score'] <= max_score)]

            # Display filtered dataset
            st.write('### Filtered Dataset')
            st.write(filtered_data)

            # Visualizations
            st.write('### Data Visualization')

            # Distribution of Scores
            st.write('#### Distribution of Scores')
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.histplot(filtered_data['Score'], bins=20, kde=True, ax=ax)
            plt.xlabel('Score')
            plt.ylabel('Count')
            plt.title('Distribution of Scores')
            st.pyplot(fig)

            # Top Facilities by Score
            st.write('#### Top Facilities by Score')
            top_facilities = filtered_data.sort_values(by='Score', ascending=False).head(10)
            st.write(top_facilities[['Facility Name', 'Score']])

            # Add more features here...

            # Interactive Table
            st.write('### Interactive Table')
            st.write(filtered_data)

            # Scatter plot of Scores vs. ZIP Code
            st.write('#### Scatter plot of Scores vs. ZIP Code')
            fig_scatter = px.scatter(filtered_data, x='ZIP Code', y='Score', color='County/Parish', hover_name='Facility Name', title='Scores vs. ZIP Code')
            st.plotly_chart(fig_scatter)

            # Box plot of Scores by Measure Name
            st.write('#### Box plot of Scores by Measure Name')
            fig_boxplot = px.box(filtered_data, x='Measure Name', y='Score', color='County/Parish', title='Scores by Measure Name')
            st.plotly_chart(fig_boxplot)

            # Pairplot of numeric columns
            st.write('#### Pairplot of Numeric Columns')
            numeric_columns = filtered_data.select_dtypes(include=['int64', 'float64']).columns
            pairplot = sns.pairplot(filtered_data[numeric_columns])
            st.pyplot(pairplot)

             # Data Export
            st.write('### Data Export')
            if st.button('Download Filtered Data as CSV'):
                csv = filtered_data.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="filtered_data.csv">Download CSV File</a>'
                st.markdown(href, unsafe_allow_html=True)

        else:
            st.error("Score column not found or not numeric in the dataset.")
    else:
        st.error("Failed to load dataset.")

if __name__ == '__main__':
    main()
