import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def main():
    st.title('Facility Analysis')
    st.sidebar.title('Filters')

    # Load the dataset with specified encoding
    @st.cache
    def load_data():
        try:
            data = pd.read_csv('Healthcare_Associated_Infections-Hospital.csv')  
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

        # Filter by score
        min_score, max_score = st.sidebar.slider('Select Score Range', min_value=data['Score'].min(), max_value=data['Score'].max(), value=(data['Score'].min(), data['Score'].max()))
        filtered_data = filtered_data[(filtered_data['Score'] >= min_score) & (filtered_data['Score'] <= max_score)]

        # Display filtered dataset
        st.write('### Filtered Dataset')
        st.write(filtered_data)

        # Visualizations
        st.write('### Data Visualization')

        # Distribution of Scores
        st.write('#### Distribution of Scores')
        plt.figure(figsize=(8, 6))
        sns.histplot(filtered_data['Score'], bins=20, kde=True)
        plt.xlabel('Score')
        plt.ylabel('Count')
        plt.title('Distribution of Scores')
        st.pyplot()

        # Top Facilities by Score
        st.write('#### Top Facilities by Score')
        top_facilities = filtered_data.sort_values(by='Score', ascending=False).head(10)
        st.write(top_facilities[['Facility Name', 'Score']])

        # Map of Facilities by Location
        st.write('#### Map of Facilities by Location')
        fig = px.scatter_geo(filtered_data, lat='Latitude', lon='Longitude', color='Score',
                             hover_name='Facility Name', size='Score', size_max=15, projection='natural earth')
        fig.update_geos(showcountries=True, countrywidth=0.5, countrycolor='Black')
        st.plotly_chart(fig)
    else:
        st.error("Failed to load dataset.")

if __name__ == '__main__':
    main()
