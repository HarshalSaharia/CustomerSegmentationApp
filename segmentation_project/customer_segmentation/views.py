from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .models import CustomerData, ClusterResult
from .clustering import kmeans_clustering
import pandas as pd
import numpy as np
import plotly.express as px
import json

# View for uploading data
def upload_data(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['file']
            # Read CSV using Pandas
            data = pd.read_csv(csv_file)
            # Save each row to CustomerData model
            for _, row in data.iterrows():
                CustomerData.objects.create(
                    customer_id=row['CustomerID'],
                    gender=row['Gender'],
                    age=row['Age'],
                    annual_income=row['Annual Income (k$)'],
                    spending_score=row['Spending Score (1-100)']
                )
            # Redirect to dashboard after upload
            return redirect('segment')
    else:
        form = CSVUploadForm()
    return render(request, 'customer_segmentation/upload.html', {'form': form})

# View for customer segmentation dashboard
def segment_customers(request):
    # Get customer data and clusters
    customer_data = CustomerData.objects.all()
    clusters = ClusterResult.objects.all()

    # Debugging output
    print(f'Number of customers: {customer_data.count()}')
    print(f'Number of clusters: {clusters.count()}')

    # Prepare data for visualization
    if not customer_data or not clusters:
        return render(request, 'customer_segmentation/dashboard.html', {'error': 'No data available for segmentation.'})

    # Prepare the data for Plotly
    data = np.array([(c.age, c.annual_income, c.spending_score) for c in customer_data])
    cluster_ids = [cluster.cluster_id for cluster in clusters]

    # Create a DataFrame for Plotly
    df = pd.DataFrame(data, columns=['Age', 'Annual Income', 'Spending Score'])
    
    # Ensure the lengths match
    if len(cluster_ids) != len(df):
        return render(request, 'customer_segmentation/dashboard.html', {'error': 'Cluster IDs do not match customer data.'})

    df['Cluster'] = cluster_ids

    # Define a color palette
    color_map = px.colors.qualitative.Plotly
    fig = px.scatter_3d(df, x='Age', y='Annual Income', z='Spending Score', color='Cluster',
                         color_continuous_scale=color_map)

    # Convert plot to HTML
    plot_html = fig.to_html(full_html=False)

    # Prepare average metrics for display
    avg_metrics = {cluster.cluster_id: {'avg_income': cluster.avg_annual_income, 'avg_spending': cluster.avg_spending_score} for cluster in clusters}

    # Prepare context for rendering
    context = {
        'avg_metrics': avg_metrics,
        'plot_html': plot_html,
    }
    
    return render(request, 'customer_segmentation/dashboard.html', context)
