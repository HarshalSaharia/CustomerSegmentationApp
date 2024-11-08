from sklearn.cluster import KMeans
import numpy as np
from .models import CustomerData, ClusterResult

def kmeans_clustering(n_clusters=5):
    customers = CustomerData.objects.all()

    if len(customers) < n_clusters:
        raise ValueError("Number of customers is less than number of clusters.")

    data = np.array([(c.age, c.annual_income, c.spending_score) for c in customers])
    
    model = KMeans(n_clusters=n_clusters)
    clusters = model.fit_predict(data)

    # Clear previous cluster results
    ClusterResult.objects.all().delete()

    # Reset customer cluster assignments
    CustomerData.objects.update(cluster_id=None)

    # Calculate averages per cluster and update each customer’s cluster_id
    cluster_averages = {}
    for idx, cluster_id in enumerate(clusters):
        customer = customers[idx]
        customer.cluster_id = cluster_id
        customer.save()  # Save cluster_id for each customer

        if cluster_id not in cluster_averages:
            cluster_averages[cluster_id] = {
                'total_spending_score': 0,
                'total_income': 0,
                'count': 0
            }

        cluster_averages[cluster_id]['total_spending_score'] += customer.spending_score
        cluster_averages[cluster_id]['total_income'] += customer.annual_income
        cluster_averages[cluster_id]['count'] += 1

    # Create ClusterResult entries based on averages
    for cluster_id, metrics in cluster_averages.items():
        avg_spending = metrics['total_spending_score'] / metrics['count']
        avg_income = metrics['total_income'] / metrics['count']

        cluster_result = ClusterResult.objects.create(
            cluster_id=cluster_id,
            description=f"Average metrics for cluster {cluster_id}",
            avg_spending_score=avg_spending,
            avg_annual_income=avg_income,
            customer_count=metrics['count'],
            marketing_recommendation="Target based on cluster preferences."
        )
        print(f"Created ClusterResult: {cluster_result}")

    # Return model and cluster centers if needed
    return model, model.cluster_centers_
