# DS Module

## Docker Containers

### Model Training

Defined in `docker/modelling/Dockerfile`.
When building the image, make sure you build it from the context of the `modules` parent folder. This is because the build process needs to copy the MLE module into the image, as it is a dependency of the data science Python code.

Waits until a database called  `company_data` is available at `$DB_HOSTNAME:$DB_PORT`, and a `feature_store` table is available on the `public` schema of this database.
When it is, connect using username `$DS_DB_PASSWORD` and password `$DS_DB_PASSWORD`. (`$` denotes an environment variable passed to the Docker container upon running)

Afterwards, trains a simple model, and saves both the model and the one-hot encoder required to process non-numerical data in the `/models` folder inside the container, which can be connected to a volume in order to be accessible outside the container.

## Folder Structure

* `ds_package`: defines a pip-installable data science package called `data_science`.
* `docker`: configures the Docker image for model training