# DE Module

## Description

As the data engineer in your team, you need to provide clean, up-to-date data to your team members, as well as set up the data infrastructure.
This involves:

* setting up a "production" database (for the purposes of this challenge, the local implementation will serve as the production database).
* fetching the source data, processing it, and storing it on the database.
* setting up a workflow orchestrator to run the data processing ETLs.
* creating a feature store to allow training the model.

## Implementation Requirements

### Workflow Orchestrator

You should create a Dockerfile with a workflow orchestrator, which you can use to schedule and trigger your data processing workflows.
This orchestrator needs to:

* have a graphical interface.
* allow scheduling your workflows.
* allow for automatic backfilling (i.e.: it should be able to identify failed part runs and allow you to re-trigger them).

You should include a docker container created from this image on the `docker-compose.yml` file.

We strongly recommend you use Airflow DAGs here, as they meet all the requirements above. If you do so, please deploy the Airflow UI on port `8082`.
Feel free to implement things differently, as long as everything is properly documented and the end-to-end system is functional!

## Database

You should include a database service in the `docker-compose.yml` file, to store the data that is fetched and processed by the data workflows. We recommend you use Postgres for this, but feel free to implement the database of your choice, as long as:

* the data is accessible on port `5432` through SQL.
* the docker-compose service is called `operational-db`.

This is what the other modules are expecting, so if you want to change this, you'll also have to make changes to the other modules!

Set up the database in the following way:

* database name: `companydata`
* schema name: `public`
* users (_don't worry about having the passwords for these users in the code_):
    * user: `admin`, password: `admin`
    * user: `ds_user`, password: `ds_user`
    * user: `mle_user`, password: `mle_user`
* permissions:
    * `admin` user should have full control of the database.
    * `ds_user` should have the `ds_user_role` role, with READ-ONLY permissions on the public schema.
    * `mle_user` should have the `mle_user_role` role, with all permissions on the public schema.

### Data Processing Workflows

The source data can be found in the **public** S3 bucket `daredata-technical-challenge-data`.
Here is a brief description of the data files:

* `customer_activity.csv`: contains some features related to the activity of your clients. Each row has a `valid_from` and a `valid_to` date, which allows keeping track of changes in the clients' activity. A null `valid_to` date represents the most recent activity.
* `customer_profiles.csv`: profiles for each customer, composed of a few static features.
* `labels.csv`: label (`0`or `1`) for each client.
* `sales/YYYY-MM-DD/sales.csv`: each sales file has the daily sales for a given month.
* `stores.csv`: information about the company's stores and respective locations.

You must implement the following workflows:

1. Customer Data Load: this workflow is a one-off workflow. It should fetch the customer-related files from the source, and write them to the database exactly as they are, and with the same name as the file (minus the extension)
1. Sales Data Load and Aggregation:
  * this workflow is a **monthly** workflow. It should run automatically at the start of each month, fetch **only** the sales file corresponding to the previous month, and insert it into an already existing `sales` table (this table can be created during the workflow, if it doesn't exist, but you can also create it when booting up the database).
  * furthermore, it should also aggregate the sales from the previous month, and insert them into an already existing `monthly_sales` table. Make sure you only process the data for that month, to avoid duplicating data or reprocessing past data. This table should contain the columns `store_idx`, `location`, `sale_month`, `value`
1. Feature store: this workflow should join the customer profiles, customer activity, and labels into a single table called `feature_store`. This table should only contain one row per client, and should only contain the latest activity features for each client. The `feature_store` table should have the following columns, which you can find in the different input files: 
    * `idx`
    * `attr_a`
    * `attr_b`
    * `scd_a`
    * `scd_b`
    * `label`

Don't forget to give read-access to all tables to both the DS and MLE users!