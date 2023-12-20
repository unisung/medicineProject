from django.shortcuts import render

# Create your views here.
import os, json
import pandas as pd
import plotly.express as px
import plotly.offline as opy


import matplotlib.pyplot as plt
import seaborn as sns
from django.conf import settings

import folium
from folium.plugins import MarkerCluster


def index(request):

    return render(request,'medicmap/index.html')

def map_population(request):
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
    plot_div = opy.plot(fig, auto_open=False, output_type='div', include_plotlyjs=False, show_link=False)
    plot_div = plot_div.replace('<div>', f'<div style="width: 100%; height: 75vh;">', 1)

    # Pass the plot_div variable to the template
    return render(request,'medicmap/map_population.html',{'plot_div': plot_div})

def district_graph(request):

    # CSV file path
    csv_file_path = os.path.join(settings.BASE_DIR, 'static', '서울병원정보서비스.csv')
    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file_path, encoding='UTF-8')
    # Group by '시군구명' and count the number of hospitals
    df_mpg = df.groupby('시군구명', as_index=False).agg(n=('시군구명', 'count')).sort_values('n', ascending=False)
    # Create an interactive bar chart using Plotly Express
    fig = px.bar(df_mpg, x='시군구명', y='n', labels={'n': 'Number of Hospitals'}, width = 1000, height = 350)
     # Convert the plot to HTML
    plot_html = fig.to_html(full_html=False)

    df_mpg2 = df.groupby('시군구명', as_index=False).agg(n=('시군구명', 'count')).sort_values('n', ascending=False)
    fig = px.scatter(df_mpg2, x='시군구명', y='n', labels={'n': '수'},  width = 1000, height = 350)
    plot_html2 = fig.to_html(full_html=False)

    return render(request, 'medicmap/district_graph.html', {'plot_html': plot_html, 'plot_html2': plot_html2})

from django.shortcuts import render
import folium
import os
import json
from django.conf import settings

def map_view(request):
    # Create a Folium figure
    fig = folium.Figure()

    # Create a Folium map
    m = folium.Map(
        location=[37.559819, 126.963895],
        zoom_start=11,
        tiles='cartodbpositron'
    )

    # Path to the GeoJSON file containing Seoul's municipal boundaries
    geojson_file_path = os.path.join(settings.BASE_DIR, 'static', 'seoul_municipalities_geo_simple.json')

    with open(geojson_file_path, 'r', encoding='UTF-8') as f:
        seoul_geo = json.load(f)

    # Add GeoJSON layer to the map
    geojson_layer = folium.GeoJson(seoul_geo, name='서울시 구별')

    geojson_layer.add_child(folium.GeoJsonPopup(fields=['name'], labels=True, sticky=False, parse_html=False, max_width=200))
    geojson_layer.add_child(folium.GeoJsonTooltip(fields=['name'], labels=True, sticky=False, max_width=200))
    geojson_layer.add_to(m)

    # Add markers with district names and click event
    for feature in seoul_geo['features']:
        district_name = feature['properties']['name']
        district_url = feature['properties']['name_eng']
        try:
            center_lat, center_lng = feature['geometry']['coordinates'][0][0][1], \
            feature['geometry']['coordinates'][0][0][0]
            # Embed an HTML link in the popup content
            popup_content = f'district: {district_name}<br><a href="/medicmap/map_view_hospitals/{district_name}" target="_blank">Click me!</a>'
            folium.Marker(
                location=[center_lat, center_lng],
                popup=popup_content,
                tooltip=district_name,
                icon=folium.Icon(color='blue', icon='info-sign'),
            ).add_to(m)
        except (IndexError, KeyError):
            print(f"Error processing feature: {district_name}")

    # Add the map to the figure
    m.add_to(fig)

    # Convert Folium figure to HTML
    map_html = fig._repr_html_()

    context = {'plot_div': map_html}

    return render(request, 'medicmap/map_view.html', context)

def map_visualization(request):
    fig = folium.Figure()
    # 위도
    latitude = 37.50842
    # 경도
    longitude = 126.9999

    # CSV file path
    csv_file_path = os.path.join(settings.BASE_DIR, 'static', '서울병원정보서비스.csv')

    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file_path, encoding='UTF-8')

    sub_df = df.loc[df['시도명'].isin(['서울'])]

    m = folium.Map(location=[latitude, longitude], zoom_start=10)

    coords = sub_df[['위도', '경도', '주소']]

    marker_cluster = MarkerCluster().add_to(m)

    for lat, long in zip(coords['위도'], coords['경도']):
        folium.Marker([lat, long], icon=folium.Icon(color="green")).add_to(marker_cluster)

    # Add the map to the figure
    m.add_to(fig)

    # Convert Folium figure to HTML
    map_html = fig._repr_html_()

    context = {'plot_div': map_html}
    return render(request,'medicmap/map_visualization.html', context)

def district_pie_chart(request):

    labels = ["강남구", "서초구", "송파구", "강서구", "강동구", "영동포구", "마포구", "노원구", "관악구", "은평구", "양천구", "동대문구", "구로구", "동작구", "중구", "광진구", "중량구", "성북구", "종로구", "성동구", "강북구", "서대문구", "도봉구", "금천구", "용산구"]
    values = [2837, 1402, 1246, 932, 875, 799, 766, 754, 708, 705, 664, 605, 596, 594, 588, 570, 556, 547, 482, 472, 461, 444, 377, 365, 323]

    # Create a simple pie chart using Plotly Express
    fig_simple_pie = px.pie(names=labels, values=values, title='Distribution of Hospitals in Seoul by District',
                            width=400, height=960,)

    # Convert Plotly Express simple pie chart to HTML
    simple_pie_html = fig_simple_pie.to_html(full_html=False)

    # Create an interactive pie chart with custom wedge properties using Plotly Express
    fig_interactive_pie = px.pie(names=labels, values=values, title='Distribution of Hospitals in Seoul by District',
                                width=450, height=960,
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
        'medicmap/district_pie_chart.html',
        {'simple_pie_html': simple_pie_html, 'interactive_pie_html': interactive_pie_html}
    )


def district_distribution(request):
    return render(request,'medicmap/district_distribution.html')

def medical_institution_types(request):
    csv_file_path = os.path.join(settings.BASE_DIR, 'static', '서울병원정보서비스.csv')
    df = pd.read_csv(csv_file_path, encoding='UTF-8')

    df_mpg1 = df.groupby('종별명', as_index=False).agg(n=('시군구명', 'count')).sort_values('n', ascending=False)
    fig = px.line(df_mpg1, x='종별명', y='n', labels={'n': '수'}, title='line Chart', width=960,height=560)
    plot_html1 = fig.to_html(full_html=False)

    df_mpg2 = df.groupby('종별명', as_index=False).agg(n=('시군구명', 'count')).sort_values('n', ascending=False)
    fig = px.bar(df_mpg2, x='n', y='종별명', labels={'n': '수'}, title='graph Chart', width=960,height=560)
    plot_html2 = fig.to_html(full_html=False)


    return render(request,'medicmap/medical_institution_types.html', {'plot_html1': plot_html1, 'plot_html2': plot_html2})

def district_total_doctors(request):
    return render(request,'medicmap/district_total_doctors.html')


def map_view_hospitals(request, district):
    # CSV file path
    csv_file_path = os.path.join(settings.BASE_DIR, 'static', '서울병원정보서비스.csv')
    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file_path, encoding='UTF-8')

    print(district)
    city = df['시군구명'] == district
    print(city)
    city1 = df[city]
    print(city1)

    # Create an interactive Seaborn plot using Plotly Express
    fig = px.bar(city1, x='종별명')

    # Convert the Plotly figure to HTML
    plot_html = fig.to_html(full_html=False)

    context = {'plot_html': plot_html}
    context['district'] = district

    return render(request, 'medicmap/map_view_hospitals.html', context)