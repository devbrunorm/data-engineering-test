# Test Attempt
## Disclaimers
1. I tried to find an open-source and automatic way of extracting the granular data from the .xls file, with no success. So, I came up with an manual approach that will be detailed below.
2. As I focused at "containerizing" my applications, I have stumbled across some obstacules at orchestrating with Airflow. My issue was running my local Docker images inside Airflow instead of using an image repository (as recommended by DockerOperator). As I may not have enough time to came up with a solution, the pipeline was "orchestrated" with docker-compose instead.
3. I chose to use Pandas instead of Spark because of two reasons:
- The dataset is small, making Pandas and beter solution than Pyspark
- PySpark environments are more complex to set up.

## 1 - Getting the "unpivoted" data
The source data consists of aggregated data inside a Pivot Table on an Excel File (.xls). As the original data source are not available, the only way to retrieve it was to get the pivot tables' cache. My workaround was to convert the .xls to .xlsx format (so I could preserve all the cache and data from the original file), rename the file extension to .zip (which is present inside the assets folder of this repo) and then unzip this same file:
```sh
unzip vendas-combustiveis-m3.zip
```

With this procedure, I was able to retrieve the pivot tables' cache inside some .xml files.

## 2 - Running the application
As already explained, my "orchestration" choice was to use docker-compose. Therefore, I created two containers, one responsable for the extraction process and another responsable for the transformation process. When the extraction is successfully completed, the transformation container will be started.

For data persistency between containers and to work as the output folder for this project, I created an "datalake" folder, with two directories: bronze (raw data) and silver (finished and partitioned data).

The pivot tables' cache are separated into two .xml files. The first beening responsable for storing the "metadata" (such as, table columns and filters) and the second responsible for the data itself. So the extraction container extracts the data present at these two files and concats it. After this, a small data verification is done to assert that the created dataframe is correct.

Another issue in the extract process is that the data from the tables are granularly different. For example, one of them is separated by product, year and then uf, and the another table is separated by year, product and then uf. To solve this, I created different orders of execution for the cross joins in each table.

Inside the transformation container, the dataframe columns are renamed and casted to the correct data type. I chose to partitioned only one column, so the container wouldn't create hundreds, or even, thousands of folders. And the column chosen to be partitioned was "uf", as I thougth that the "month_year" would generate many partitions with complex directory names. In my opinion, the "product" column would be another good column to partition on.

Finally, to run the project, you need Docker and docker-compose. Go to the root directory of this project and run the follwing command:
```
docker-compose up
```