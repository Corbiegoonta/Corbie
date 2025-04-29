from pipelines.training_pipeline import train_pipeline
from zenml.client import Client

if __name__ == "__main__":

    print(Client().active_stack.experiment_tracker.get_tracking_uri())
    train_pipeline(data_path=r"C:\Users\nickc\OneDrive\Desktop\Code\Personal Projects\CustomerReviewsMLOpsProject\data\olist_customers_dataset.csv")
    
    # Run MLFlow with 

    # mlflow ui --backend-store-uri "file:C:\Users\nickc\AppData\Roaming\zenml\local_stores\f626246b-dbd2-4b46-9283-f5f0b715d7fa\mlruns"