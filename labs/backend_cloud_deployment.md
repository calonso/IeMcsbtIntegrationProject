# Deploy a Flask Application to Google App Engine

## Prerequisites
- [A Google Cloud account.](https://cloud.google.com)
- Python installed locally.
- [Google Cloud SDK CLI installed.](https://cloud.google.com/cli?hl=en)
- A Flask application that is working and ready to be deployed

## Instructions

### Step 1: Prepare for Deployment

1. Ensure the Google Cloud SDK is installed and initialized: 
    ```
    gcloud init
    ```
    1. Make sure you log in with your `@student.ie.edu` account
    1. When prompted, create a new project named `mcsbt-integration`
1. Ensure you claim your student credits (look for Carlos' email)
1. Enable billing on your brand new project
    1. Navigate to `https://console.cloud.google.com/billing/projects`
    1. `My Projects` tab
    1. Find `mcsbt-integration` project, and click on `Change billing` entry under Actions section.
    1. Assign `Billing Account for Education` billing account.

### Step 2: Deploy to Google App Engine
1. Create a file named `app.yaml` with the following contents
    ```
    runtime: python39
    ```
1. Make sure there's a `requirements.txt` file next to it that specifies the required dependencies
1. Deploy the function:
    ```
    gcloud app deploy
    ```

### Step 3: Access Your Deployed Flask Application

1. Run the recommended browse command
    ```
    gcloud app browse
    ```

### Step 4: Update

1. Whenever you want to update the code repeat
    ```
    gcloud app deploy
    ```