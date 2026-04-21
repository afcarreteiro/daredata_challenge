# Deployment Module

## Description

The goal of this module is to deploy to final classification module to a cloud-based service, where it can be accessed by the company's clients.
All roles (DS, DE, MLE) should perform this assignment.

For the purposes of this test, we consider your local development environment to be the _production_ environment where the final model is built. The only things that are moved to the cloud are:
* the model itself, plus the required artifacts for the model to be able to make new predictions (all of which can be found in the `models` folder of the `ds` module)
* a very simple API (in the `./deployment/api` folder) used to serve it.

This makes it more achievable to complete the technical assessment in time, and also to stay within the free tier of whatever cloud service you choose for the deployment.

Of course, in a real-life scenario, the final model should be produced in a proper production environment, separate from the local development environments, which should only be used for experimentation.

## Implementation Requirements

The evaluation criteria for this module are very loose, giving you the freedom to implement the final solution using your prefered set of tools. However, for each requirement, we also provide suggestions of a possible approach.

The implementation requirements are as follows:

* it should be possible for an end-user to make HTTP requests through the internet, to some `predict` route, and get back a label prediction for a new client.
    * Suggestion: `AWS EC2`, `AWS VPC` and `nginx` to set up a server, opening the right ports to provide HTTP (or preferably: HTTPS!) access to the outside world.
    * You can find some *pseudocode* for the implementation of the API in the `./api/app.py` file, as well as a valid example request in the `example_request.py` file.
* the deployment of a new model should be triggered whenever you push new code to the `main` branch of your repository. No manual steps should be required!
    * suggestion: `Github Workflows` or `Gitlab Actions` to create a CI/CD pipeline
* you should write a very simple test for your API, which should run automatically and prevent pushing a new model to production if the test fails. The python code should also be properly linted before a new deployment. 
    * `pytest` to run the test, and `black` to lint the python files.

As long as the criteria above are met, you are free to be creative with your solution and to use the tools you're most comfortable with. Above all, we value organization, clean code, and good practices.

## Important Notes

### Free Tier

We think the requirements specified above should be possible to implement using AWS' free tier, for example. We don't expect you to spend any of your own money during development!
If you hit some bottlenecks (disk, RAM, etc.) in your solution and are not able to implement it, please let us know the details so we can assess the issue and possibly adjust the challenge requirements on our end.

### After Delivery

You **don't need to leave the cloud system running after delivering the technical assessment solution**.

Make sure you take some screenshots to prove that the system is working, add them to your documentation, and then tear the system down to avoid incurring any unexpected infrastructure costs.

In some cases, we might ask you to get it up-and-running again so we can test it - **but we will let you know in advance and coordinate with you, in order to minimize uptime.**