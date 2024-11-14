
# Customer Segmentation App
## Project Overview

The **Customer Segmentation App** is a Django-based web application designed to segment customers into clusters using the K-Means clustering algorithm. This tool is aimed at businesses that want to identify customer groups based on their demographics and spending behavior, helping with targeted marketing and tailored strategies.

### Key Features

- **Data Upload**: Allows users to upload CSV files with customer data (age, annual income, spending score).
- **Clustering Analysis**: Uses K-Means clustering to group customers and analyze each cluster's average metrics.
- **Dashboard**: Displays segmentation results, including average income, spending score, customer count, and marketing recommendations for each cluster.
- **Data Visualization**: Provides visual insights to help users better understand customer clusters.



## Setup Instructions

### Prerequisites

- **Python 3.0**: Make sure Python is installed on your machine.
- **Django**: Install Django using `pip install django`.
- **Google Cloud SDK**: Required for deployment to Google App Engine (GAE).
## Installation

1. Clone the repository:

```bash
  git clone https://github.com/HarshalSaharia/CustomerSegmentationApp.git
  cd CustomerSegmentationApp
```
2. Create and activate a virtual environment:

```bash
  python -m venv env
  On Windows: env\Scripts\activate
```
3. Install the dependencies:

```bash
  pip install -r requirements.txt
```
4. Apply Migrations:
```bash
  python manage.py migrate
```
5. Start Django Server:
```bash
  python manage.py runserver
```
6. Visit http://127.0.0.1:8000/ to access the app locally.


    
## Deployment to Google App Engine (GAE)
   1. Set up Google Cloud SDK and authenticate:
   ```bash
    gcloud init
   ```
2. Ensure that app.yaml and requirements.txt are correctly set up in your project directory.

3. Deploy to GAE:
```bash
  gcloud app deploy
```

## Sample 
For testing, you can use the provided sample file: sample.csv
## License

  Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

## Authors

- [@HarshalSaharia](https://www.github.com/HarshalSaharia)

