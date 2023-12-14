from django.shortcuts import render
import plotly.express as px
import plotly.offline as opy

def map_view(request):
    # Replace this with your actual data and plot creation
    fig = px.scatter(x=[1, 2, 3], y=[4, 5, 6])

    # Generate HTML code for the figure
    plot_div = opy.plot(fig, auto_open=False, output_type='div')

    # Pass the plot_div variable to the template
    return render(request, 'mymap/map.html', {'plot_div': plot_div})
