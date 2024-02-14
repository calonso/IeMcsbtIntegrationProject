# Deploy a React Application to Google Cloud Storage

## Objective
Deploy a basic React application to Google Cloud Storage.

## Prerequisites
- [A Google Cloud account.](https://cloud.google.com)
- [Google Cloud SDK CLI installed.](https://cloud.google.com/cli?hl=en)
- A React application that is working and ready to be deployed

## Instructions

### Step 1: Prepare for Deployment

1. Ensure the Google Cloud SDK is installed and initialized: 
    ```
    gcloud init
    ```
    1. Make sure you log in with your `@student.ie.edu` account
    1. When prompted, create a new project named `mcsbt-integration` (if not exists yet)
1. Ensure you claim your student credits (look for Carlos' email)
1. Enable billing on your brand new project
    1. Navigate to `https://console.cloud.google.com/billing/projects`
    1. `My Projects` tab
    1. Find `mcsbt-integration` project, and click on `Change billing` entry under Actions section.
    1. Assign `Billing Account for Education` billing account.

### Step 2: Create a Google Cloud Storage Bucket
1. Create a new bucket (replace `YOUR_UNIQUE_BUCKET_NAME` with a unique bucket name):
    ```
	gsutil mb gs://YOUR_UNIQUE_BUCKET_NAME/
	```
1. Make the bucket publicly accessible:
    ```
    gsutil iam ch allUsers:objectViewer gs://YOUR_UNIQUE_BUCKET_NAME
    ```

### Step 3: Configure the Bucket for Static Website Hosting
1. Set the main page and error page (typically index.html and 404.html):
    ```
    gsutil web set -m index.html -e 404.html gs://YOUR_UNIQUE_BUCKET_NAME
    ```

### Step 4: Build Your React Application
1. Navigate to your React app directory and run:
    ```
    npm run build
    ```

This compiles your app into static files in the build directory.

### Step 5: Upload Your Build Directory to the Bucket
1. Navigate to your React app's build directory.
1. Use gsutil to copy the files to your bucket:
    ```
    gsutil -h "Cache-Control:no-cache, max-age=0" -m cp -r ./* gs://YOUR_UNIQUE_BUCKET_NAME/
    ```

The -m flag enables parallel uploads for faster transfer, and -r is for recursive copying to handle the directory structure.

### Step 6: Access Your Deployed React App

1. Your React app will now be accessible via http://YOUR_UNIQUE_BUCKET_NAME.storage.googleapis.com/index.html.
    1. Replace YOUR_UNIQUE_BUCKET_NAME with the name of your bucket.

### Step 7: Visualize your bucket from Google Cloud console

1. Navigate to cloud.google.com, type 'Cloud Storage' in the search bar and find your newly created bucket. See the assets inside.

### Step 8: Update the contents

1. If you need to upload a new version, first delete all the contents in the bucket, then repeat this process.
1. Make sure you clear your browser's cache before reloading.
