from pipelines.deployment_pipeline import continuous_deployment_pipeline
import click
from rich import print
from zenml.integrations.mlflow.mlflow_utils import get_tracking_uri
from zenml.integrations.mlflow.model_deployers.mlflow_model_deployer import MLFlowModelDeployer
from zenml.integrations.mlflow.services import MLFlowDeploymentService
from typing import cast

DEPLOY = "deploy"
PREDICT = "predict"
DEPLOY_AND_PREDICT = "deploy_and_predict"

@click.command()

@click.option(
    "--config",
    "-c",
    type=click.Choice([DEPLOY, PREDICT, DEPLOY_AND_PREDICT]),
    default=DEPLOY_AND_PREDICT,
    help="Optionally you can choose to only run the deployment pipeline to train and deploy a model ('deploy'), or to only run a prediction against the deployed model ('predict'). By default both will be run ('deploy_and_predict).",
)

@click.option(
    "--min-accuracy",
    default=0.92,
    help="Minimum accuracy required to deploy the model"
)

def run_deployement(config: str, min_accuracy: float):
    mlflow_model_deployer_component = MLFlowModelDeployer.get_active_model_deployer()
    deploy = config == DEPLOY or config == DEPLOY_AND_PREDICT
    predict = config == PREDICT or DEPLOY_AND_PREDICT

    if DEPLOY:
        continuous_deployment_pipeline(
            data_path=r"C:\Users\nickc\OneDrive\Desktop\Code\Personal Projects\CustomerReviewsMLOpsProject\data\olist_customers_dataset.csv",
            min_accuracy=min_accuracy,
            workers=3,
            timeout=60
            )
    if PREDICT:
        # inference_pipeline()
        print()
    
    print(f"You can run: mlflow ui --backend-store-uri '{get_tracking_uri()}' to inspect you experiemnt runs within MLFlow UI. You cna find your runs tracked within the 'mlflow_example_pipeline' experiment. There you'll also be able to compare 2 or more runs.")

    existing_services = mlflow_model_deployer_component.find_model_server(
        pipeline_name="continuous_deployment_pipeline",
        pipeline_step_name="mlflow_model_deployer_step",
        model_name="model"
    )

    if existing_services:
        service = cast(MLFlowDeploymentService, existing_services[0])
        if service.is_running:
            print(f"The MLFlow prediction server is running locally as a daemon process service and accepts inference requests at: {service.prediction_url}. To stop the servce run 'zenml model_deployer models delete {str(service.uuid)}")
        elif service.is_failed:
            print(f"The MLFlow prediction server is in a failed state: Last state: '{service.status.state.value}' Last error: '{service.status.last_error}'")
        else:
            print("No MLflow prediction server is currently running. The deployment pipeline must run first to train a model and deploy it. Execute the same command with the '--deploy' argument to deploy a model")

if __name__ == "__main__":
    run_deployement()