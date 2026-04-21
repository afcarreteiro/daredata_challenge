# Technical Assessment

## Introduction

In this technical assessment, you will simulate being in a team of 3 people: a data scientist, a data engineer, and a machine learning engineer working together. Each one of them worked on a module. Now you, the 3rd member, should complete your own module as well as handle the model deployment.

Your company has some information about its clients' profiles and activity, and wants to create a machine learning model that classifies them into two different groups, with labels `0` and `1`. This is a supervised classification problem.
This will require a system with four distinct modules, all of which can be found in the `modules` directory:

* `de`: the data engineering module, which sets up the ETL workflow orchestrator, and creates a few ETLs to fetch and process the data.
* `ds`: the data science module, where the data above is explored, and a model is trained to classify the clients.
* `mle`: the machine learning engineering module, whose responsibility is to supply the data scientist with the tools to easily productize their model.
* `deployment`: this module handles the deployment of the final model to a cloud-based service, including provisioning the required infrastructure.

We recommend you read this entire document, as well as each module's documentation before starting (for your module and the deployment module: `IMPLEMENTATION.md`; for other modules: `README.md`).

## Instructions

### Task 1 - Implement your functional module

According to your profile (DS, DE or MLE), you will have to fully implement the corresponding module. You can find detailed instructions about the module's expected behaviour on the `IMPLEMENTATION.md` file inside the respective module folder.

You also have to add the Docker image(s) you created for your module to the `docker-compose.yml` file, which represents the full system.

The idea here is that you should be able to understand the end-to-end system, and seamlessly integrate your module into it, while respecting the "service-level agreements" with the other modules (i.e.: the output that they expect coming from your module).

### Task 2 - Complete small tasks on the other modules

You should also be able to help your dear teammates with some of their tasks! This is often required in real life scenarios, as a lot of our projects are cross-disciplinary and collaborative.
On the `EXTRA_TASKS.md` document of the other modules' (excluding the `deployment` module), you will find a list of short tasks. You must select one extra task **from each other module** and implement them as well!

### Task 3 - Implement the deployment module

It's very important that you have the ability to deploy your solutions using modern tools and techniques. You have to fully implement the deployment module, whose purpose is to deploy the classification model, as well as an API to serve it, to some cloud-based service. Check the `IMPLEMENTATION.md` file for the implementation details.

## Running the Final System

* Set the required environment variables for the `docker-compose.yml` file.
* Run `docker-compose up` to run the entire system.
* If you're not a `DE`, in order to have the data available, you should navigate to `localhost:8082` and activate the Airflow DAGs in the following order: `load_client_data`, `load_sales_data`, and when both of them have successfully run, `process_data`.
* The `DS` component should be waiting until the `feature_store` table is available, and then trigger the model training.

The output should be a newly trained model in the `ds/models` folder (along with any other required artifacts such as the model's one-hot encoder).

## How to Share Your Challenge Solution

After you finish your challenge, you should do the following in order to share the solution with us:

* create an empty Git repository, making a commit to the `main` branch with the base code that we have provided you
* share the repo with ruimgf, nunobbras and ivopbernardo
* push your implementation of the code to a separate branch.
* create a pull request from your working branch to the `main` branch, and share this pull request with us.
* include a `SOLUTION.md` file at the root of the repository. This file should contain:
    * a description of the final solution, with particular emphasis on the deployment module. Feel free to use diagrams, charts, etc. to illustrate your implementation
    * a detailed timeline of the implementation: time taken for each task, implementation order, etc.
    * documentation about design decisions taken (and motives behind them), difficulties faced, and any other thoughts you think are relevant.

## Evaluation Checklist

Here is a checklist to help you keep track of the deliverables:

- [ ] Fully implement your module (DS, DE or MLE, depending on the challenge you've received)
- [ ] Implement the extra tasks (1 for each other module)
- [ ] Implement the deployment module
- [ ] Include your module in the `docker-compose.yml` file, and ensure it works
- [ ] Include a `SOLUTION.md` document in the root of the repository, containing:
  - [ ] A description of the final solution and deployment, decisions taken, etc.
  - [ ] Screenshots of the deployed model in action
  - [ ] A high-level implementation timeline

Other than that, it's also important to have:

* clean and "dry" code.
* a well structured repository.

Good luck and we hope you enjoy this challenge!