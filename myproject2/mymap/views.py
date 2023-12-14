from django.shortcuts import render

import os, json
import pandas as pd
import plotly.express as px
import plotly.offline as opy


import matplotlib.pyplot as plt
import seaborn as sns
from django.conf import settings



def map_view(request):
    # Replace this with your actual data and plot creation
    import folium

    m = folium.Map(location=[37.55, 126.90],
               zoom_start=10,
               tiles= "cartodb positron")
    # geojson 파일절대경로 저장-서울시 대상 이므로 hangjeongdong_서울특별시.geojson파일만 있으면 됨.
    geojson_file_path = os.path.join(settings.BASE_DIR, 'static', 'hangjeongdong_서울특별시.geojson')
    print(geojson_file_path)

    with open(geojson_file_path, 'r') as f:
        seoul_geo = json.load(f)
    
    # csv파일 절대경로 저장 
    csv_file_path = os.path.join(settings.BASE_DIR,  'static', 'sample.txt')
    print(csv_file_path)

    seoul_info = pd.read_csv(csv_file_path, delimiter='\t')
    seoul_info = seoul_info.iloc[3:,:]
    seoul_info = seoul_info[seoul_info['동']!='소계']
    seoul_info['full_name'] = '서울특별시'+' '+seoul_info['자치구']+' '+seoul_info['동']
    seoul_info['full_name'] = seoul_info['full_name'].apply(lambda x: x.replace('.','·'))
    seoul_info['인구'] = seoul_info['인구'].apply(lambda x: int(''.join(x.split(','))))

    fig = px.choropleth_mapbox(seoul_info,
                           geojson=seoul_geo,
                           locations='full_name',
                           color='인구',
                           color_continuous_scale='viridis', featureidkey = 'properties.adm_nm',
                           mapbox_style='carto-positron',
                           zoom=9.5,
                           center = {"lat": 37.563383, "lon": 126.996039},
                           opacity=0.5,
                          )

#fig
    # Generate HTML code for the figure
    plot_div = opy.plot(fig, auto_open=False, output_type='div')

    # Pass the plot_div variable to the template
    return render(request, 'mymap/map.html', {'plot_div': plot_div})


def hospital_chart(request):
    # CSV file path
    csv_file_path = os.path.join(settings.BASE_DIR, 'static', '서울병원정보서비스.csv')

    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file_path, encoding='UTF-8')

    # Group by '시군구명' and count the number of hospitals
    df_mpg = df.groupby('시군구명', as_index=False).agg(n=('시군구명', 'count')).sort_values('n', ascending=False)

    # Create an interactive bar chart using Plotly Express
    fig = px.bar(df_mpg, x='시군구명', y='n', labels={'n': 'Number of Hospitals'}, title='Hospital Chart')

    # Convert the plot to HTML
    plot_html = fig.to_html(full_html=False)

    return render(request, 'mymap/hospital_chart.html', {'plot_html': plot_html})


def seoul_hospital_plots(request):
    # CSV file path
    csv_file_path = os.path.join(settings.BASE_DIR, 'static', '서울병원정보서비스.csv')

    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file_path, encoding='UTF-8')

    # Filter DataFrame for Seoul
    df_seoul = df[df["시도명"] == "서울"].copy()

    # Create an interactive bar plot
    fig_bar = px.bar(df_seoul, x='시군구명', title='Number of Hospitals in Seoul by District', labels={'시군구명': 'District', 'count': 'Number of Hospitals'})
    bar_plot_html = fig_bar.to_html(full_html=False)

    # Create an interactive scatter plot
    fig_scatter = px.scatter(df_seoul, x='경도', y='위도', title='Geographical Distribution of Hospitals in Seoul', labels={'경도': 'Longitude', '위도': 'Latitude'})
    scatter_plot_html = fig_scatter.to_html(full_html=False)

    return render(
        request,
        'mymap/seoul_hospital_plots.html',
        {'bar_plot_html': bar_plot_html, 'scatter_plot_html': scatter_plot_html}
    )


def seoul_doctors_charts(request):
    # CSV file path
    csv_file_path = os.path.join(settings.BASE_DIR, 'static', '서울병원정보서비스.csv')

    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file_path, encoding='UTF-8')

    # Filter DataFrame for Seoul
    df_seoul = df[df["시도명"] == "서울"].copy()

    # Scatter plot with total doctors and district names using Plotly Express
    fig_scatter = px.scatter(df_seoul, x='총의사수', y='시군구명', title='Interactive Scatter Plot of Total Doctors in Seoul by District',
                             labels={'총의사수': 'Total Doctors', '시군구명': 'District'})
    scatter_plot_html = fig_scatter.to_html(full_html=False)

    # Bar plot with district names and total doctors using Plotly Express
    fig_bar = px.bar(df_seoul, x='시군구명', y='총의사수', title='Interactive Bar Plot of Total Doctors in Seoul by District',
                     labels={'시군구명': 'District', '총의사수': 'Total Doctors'})
    bar_plot_html = fig_bar.to_html(full_html=False)

    # Count plot with district names using Plotly Express
    fig_count = px.bar(df_seoul, x='시군구명', title='Interactive Count Plot of Districts in Seoul',
                       labels={'시군구명': 'District', 'count': 'Count'})
    count_plot_html = fig_count.to_html(full_html=False)

    # Scatter plot with latitude, longitude, and district names using Plotly Express
    fig_geographical = px.scatter(df_seoul, x='경도', y='위도', color='시군구명',
                                  title='Interactive Scatter Plot of Geographical Distribution of Hospitals in Seoul',
                                  labels={'경도': 'Longitude', '위도': 'Latitude', '시군구명': 'District'})
    geographical_plot_html = fig_geographical.to_html(full_html=False)

    return render(
        request,
        'mymap/seoul_doctors_plots.html',
        {'scatter_plot_html': scatter_plot_html, 'bar_plot_html': bar_plot_html,
         'count_plot_html': count_plot_html, 'geographical_plot_html': geographical_plot_html}
    )


def combined_pie_charts(request):
    labels = ["강남구", "서초구", "송파구", "강서구", "강동구", "영동포구", "마포구", "노원구", "관악구", "은평구", "양천구", "동대문구", "구로구", "동작구", "중구", "광진구", "중량구", "성북구", "종로구", "성동구", "강북구", "서대문구", "도봉구", "금천구", "용산구"]
    values = [2837, 1402, 1246, 932, 875, 799, 766, 754, 708, 705, 664, 605, 596, 594, 588, 570, 556, 547, 482, 472, 461, 444, 377, 365, 323]

    # Create a simple pie chart using Plotly Express
    fig_simple_pie = px.pie(names=labels, values=values, title='Distribution of Hospitals in Seoul by District')
    
    # Convert Plotly Express simple pie chart to HTML
    simple_pie_html = fig_simple_pie.to_html(full_html=False)

    # Create an interactive pie chart with custom wedge properties using Plotly Express
    fig_interactive_pie = px.pie(names=labels, values=values, title='Distribution of Hospitals in Seoul by District',
                                width=500, height=500,
                                template='seaborn',  # You can change the template if needed
                                )
    
    # Set custom wedge properties
    fig_interactive_pie.update_traces(marker=dict(line=dict(color='white', width=1)),  # Set edge color and width
                                      textinfo='percent+label',  # Show percentage and label
                                      pull=[0.1] * len(labels),  # Pull all slices by 10%
                                      )

    # Convert Plotly Express interactive pie chart to HTML
    interactive_pie_html = fig_interactive_pie.to_html(full_html=False)

    return render(
        request,
        'mymap/combined_pie_charts.html',
        {'simple_pie_html': simple_pie_html, 'interactive_pie_html': interactive_pie_html}
    )