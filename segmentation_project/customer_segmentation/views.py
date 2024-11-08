from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .models import CustomerData, ClusterResult
from .clustering import kmeans_clustering
import pandas as pd
import numpy as np
import plotly.express as px

# View for uploading data
def upload_data(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['file']
            data = pd.read_csv(csv_file)
            if data['CustomerID'].duplicated().any():
                form.add_error('file', 'The uploaded CSV contains duplicate CustomerIDs.')
                return render(request, 'customer_segmentation/upload.html', {'form': form})
                
            for _, row in data.iterrows():
                customer_id = row['CustomerID']
                customer, created = CustomerData.objects.get_or_create(
                    customer_id=customer_id,
                    defaults={
                        'gender': row['Gender'],
                        'age': row['Age'],
                        'annual_income': row['Annual Income (k$)'],
                        'spending_score': row['Spending Score (1-100)']
                    }
                )
                if not created:
                    customer.gender = row['Gender']
                    customer.age = row['Age']
                    customer.annual_income = row['Annual Income (k$)']
                    customer.spending_score = row['Spending Score (1-100)']
                    customer.save()
            
            # Perform clustering after saving CustomerData
            kmeans_clustering(n_clusters=5)

            # Check number of clusters created
            cluster_count = ClusterResult.objects.count()
            print(f"Number of clusters created: {cluster_count}")

            clusters = ClusterResult.objects.all()
            print("Cluster results:")
            for cluster in clusters:
                print(cluster)

            return redirect('segment')
    else:
        form = CSVUploadForm()
    return render(request, 'customer_segmentation/upload.html', {'form': form})


# Test function to validate the clustering
def test():
    # Simple test to ensure clustering results exist
    clusters = ClusterResult.objects.all()
    if clusters.exists():
        print("Test passed: Clusters exist.")
    else:
        print("Test failed: No clusters found.")


# View for customer segmentation dashboard
# View for customer segmentation dashboard
def segment_customers(request):
    # Get customer data and clusters
    customer_data = CustomerData.objects.all()
    clusters = ClusterResult.objects.all()

    # Prepare cluster assignments for each customer
    customer_cluster_ids = [c.cluster_id for c in customer_data]  # Ensure CustomerData has cluster_id

    # Create the DataFrame with correct lengths
    data = np.array([(c.age, c.annual_income, c.spending_score) for c in customer_data])
    df = pd.DataFrame(data, columns=['Age', 'Annual Income', 'Spending Score'])
    df['Cluster'] = customer_cluster_ids  # Assigns a cluster ID for each customer

    # Prepare Plotly figure
    fig = px.scatter_3d(df, x='Age', y='Annual Income', z='Spending Score', color='Cluster', color_continuous_scale=px.colors.qualitative.Plotly)
    plot_html = fig.to_html(full_html=False)

    # Prepare average metrics for display
    avg_metrics = {
        cluster.cluster_id: {
            'avg_income': cluster.avg_annual_income,
            'avg_spending': cluster.avg_spending_score,
            'customer_count': cluster.customer_count,
            'marketing_recommendation': cluster.marketing_recommendation
        }
        for cluster in clusters
    }

    # Debugging output
    print("avg_metrics dictionary passed to template:", avg_metrics)

    context = {
        'avg_metrics': avg_metrics,
        'plot_html': plot_html,
    }

    return render(request, 'customer_segmentation/dashboard.html', context)
