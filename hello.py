import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Preswald Integration
from preswald import connect, get_df, query, table, text, plotly as preswald_plotly

# Page configuration
st.set_page_config(
    page_title="🧠 Personality Insights Hub",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple CSS styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }

    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load dataset using Preswald
connect()  # Connect to preswald.toml
df = get_df("my_dataset")

# Query the dataset using Preswald
sql = "SELECT * FROM my_dataset WHERE value > 50"
filtered_df = query(sql, "my_dataset")

def main():
    """Main application function"""
    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; font-size: 3rem;">🧠 PERSONALITY INSIGHTS HUB</h1>
        <p style="margin:0; font-size: 1.2rem; opacity: 0.9;">Discover the Hidden Patterns in Human Behavior!</p>
    </div>
    """, unsafe_allow_html=True)

    # --- Preswald UI ---
    text("## 🔍 Query Results from Preswald")
    table(filtered_df, title="Filtered Data")

    st.markdown("## 📊 Live Statistics Dashboard")

    extrovert_count = len(df[df['Personality'] == 'Extrovert'])
    introvert_count = len(df[df['Personality'] == 'Introvert'])
    total_records = len(df)

    col1a, col2a, col3a, col4a = st.columns(4)
    with col1a:
        st.markdown(f"""
        <div class="metric-container">
            <h2>🎯</h2><h3>{total_records:,}</h3><p>Total People</p>
        </div>""", unsafe_allow_html=True)

    with col2a:
        st.markdown(f"""
        <div class="metric-container">
            <h2>🌟</h2><h3>{extrovert_count:,}</h3><p>Extroverts</p>
        </div>""", unsafe_allow_html=True)

    with col3a:
        st.markdown(f"""
        <div class="metric-container">
            <h2>🤔</h2><h3>{introvert_count:,}</h3><p>Introverts</p>
        </div>""", unsafe_allow_html=True)

    with col4a:
        ratio = round(extrovert_count / introvert_count, 1) if introvert_count > 0 else 0
        st.markdown(f"""
        <div class="metric-container">
            <h2>⚖️</h2><h3>{ratio}:1</h3><p>E:I Ratio</p>
        </div>""", unsafe_allow_html=True)

    # --- Preswald plotly chart ---
    st.markdown("## 📈 Preswald Visualization")
    fig_preswald = px.scatter(df, x="column1", y="column2", color="category", title="Preswald Scatter Chart")
    preswald_plotly(fig_preswald)

    # --- Streamlit Visualizations ---
    col1b, col2b = st.columns(2)
    with col1b:
        personality_counts = df['Personality'].value_counts()
        fig1 = go.Figure(data=[go.Pie(
            labels=personality_counts.index,
            values=personality_counts.values,
            hole=0.6,
            marker=dict(colors=['#FF6B6B', '#4ECDC4'], line=dict(color='white', width=3))
        )])
        fig1.update_layout(title='🧠 Personality Distribution', height=300)
        st.plotly_chart(fig1, use_container_width=True)

    with col2b:
        social_avg = df.groupby('Personality')['Social_event_attendance'].mean() / 10 * 100
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=social_avg.index,
            y=social_avg.values,
            marker=dict(color=['#FF6B6B', '#4ECDC4'], line=dict(color='white', width=2)),
            text=[f'{v:.1f}%' for v in social_avg.values],
            textposition='outside'
        ))
        fig2.update_layout(
            title='🎉 Social Event Attendance',
            xaxis_title='Personality Type',
            yaxis_title='Average Attendance (%)',
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Stage fear
    st.markdown("## 🎭 Stage Fear Analysis")
    df['Stage_Fear_Numeric'] = df['Stage_fear'].map({'Yes': 1, 'No': 0})
    fear_avg = df.groupby('Personality')['Stage_Fear_Numeric'].mean() * 100

    col1c, col2c = st.columns(2)
    with col1c:
        st.metric("🌟 Extrovert Stage Fear", f"{fear_avg.get('Extrovert', 0):.1f}%")
    with col2c:
        st.metric("🤔 Introvert Stage Fear", f"{fear_avg.get('Introvert', 0):.1f}%")

    fig3 = px.bar(
        x=fear_avg.index,
        y=fear_avg.values,
        title="😰 Stage Fear by Personality",
        labels={'x': 'Personality', 'y': 'Stage Fear (%)'},
        color=fear_avg.index,
        color_discrete_map={'Extrovert': '#FF6B6B', 'Introvert': '#4ECDC4'}
    )
    fig3.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

    # Random sample section
    st.markdown("## 🎲 Random Sample (10 People)")
    col1d, col2d = st.columns(2)

    with col1d:
        st.markdown("### 🎉 Social Events Sample")
        if st.button("🔄 New Social Events Sample"):
            sample = df.sample(n=10).sort_values('Personality')
            st.dataframe(sample[['Personality', 'Social_event_attendance']], height=300)
            sample_avg = sample.groupby('Personality')['Social_event_attendance'].mean() / 10 * 100
            for personality in sample_avg.index:
                count = len(sample[sample['Personality'] == personality])
                st.write(f"**{personality}s:** {sample_avg[personality]:.1f}% attendance (n={count})")

    with col2d:
        st.markdown("### 🎭 Stage Fear Sample")
        if st.button("🔄 New Stage Fear Sample"):
            sample = df.sample(n=10).sort_values('Personality')
            st.dataframe(sample[['Personality', 'Stage_fear']], height=300)
            sample['Stage_Fear_Numeric'] = sample['Stage_fear'].map({'Yes': 1, 'No': 0})
            sample_avg = sample.groupby('Personality')['Stage_Fear_Numeric'].mean() * 100
            for personality in sample_avg.index:
                count = len(sample[sample['Personality'] == personality])
                st.write(f"**{personality}s:** {sample_avg[personality]:.1f}% have stage fear (n={count})")

    # Insights
    st.markdown("## 💡 Key Insights")

    if 'Extrovert' in social_avg and 'Introvert' in social_avg:
        diff = abs(social_avg['Extrovert'] - social_avg['Introvert'])
        if social_avg['Extrovert'] > social_avg['Introvert']:
            st.info(f"🎉 Extroverts attend {diff:.1f}% more social events!")
        else:
            st.info(f"🤯 Plot twist! Introverts attend {diff:.1f}% more events!")

    if 'Extrovert' in fear_avg and 'Introvert' in fear_avg:
        diff = fear_avg['Introvert'] - fear_avg['Extrovert']
        if diff > 0:
            st.info(f"🎭 Introverts have {diff:.1f}% more stage fear.")
        else:
            st.info(f"🎭 Surprisingly, extroverts have {abs(diff):.1f}% more stage fear.")

if __name__ == "__main__":
    main()
