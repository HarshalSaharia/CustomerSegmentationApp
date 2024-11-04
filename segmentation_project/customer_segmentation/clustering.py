# customer_segmentation/clustering.py

from sklearn.cluster import KMeans
import numpy as np
from .models import CustomerData, ClusterResult

def kmeans_clustering(n_clusters=5):
    customers = CustomerData.objects.all()
    data = np.array([(c.age, c.annual_income, c.spending_score) for c in customers])
    
    model = KMeans(n_clusters=n_clusters)
    clusters = model.fit_predict(data)

    # Clear previous cluster results
    ClusterResult.objects.all().delete()

    # Calculate averages per cluster
    cluster_averages = {}
    for idx, cluster_id in enumerate(clusters):
        if cluster_id not in cluster_averages:
            cluster_averages[cluster_id] = {'total_spending_score': 0, 'total_income': 0, 'count': 0}
        
        cluster_averages[cluster_id]['total_spending_score'] += customers[idx].spending_score
        cluster_averages[cluster_id]['total_income'] += customers[idx].annual_income
        cluster_averages[cluster_id]['count'] += 1

        # Save cluster results
        ClusterResult.objects.create(
            cluster_id=cluster_id,
            description=f"Customer {customers[idx].customer_id} in cluster {cluster_id}",
            customer=customers[idx]
        )

    # Update cluster results with average metrics
    for cluster_id, metrics in cluster_averages.items():
        avg_spending = metrics['total_spending_score'] / metrics['count']
        avg_income = metrics['total_income'] / metrics['count']
        ClusterResult.objects.filter(cluster_id=cluster_id).update(
            avg_spending_score=avg_spending,
            avg_annual_income=avg_income
        )

    # Return model and cluster centers for visualization
    return model, model.cluster_centers_
