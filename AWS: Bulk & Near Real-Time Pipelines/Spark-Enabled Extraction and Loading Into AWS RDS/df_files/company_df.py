from pyspark.sql.functions import col
from pyspark.sql.types import *
from pyspark.sql import Row



def Company_table(jdf):

    company_df = jdf.select(col("name"),col("ein"),col("cik"),col("stateOfIncorporation"),col("phone"))

    company_df = company_df.dropna(how='all') #dropping the rows with "all null values"

    company_table = company_df.rdd.zipWithIndex().map(lambda r: Row(*r[0], r[1])).toDF()

    company_table = company_table.select(col("_1").alias("Company_Name"),
                        col("_2").alias("Employer_Identification_Number").cast(IntegerType()),
                        col("_3").alias("SEC_Central_Index_Key").cast(IntegerType()),
                        col("_4").alias("Registered_State"),
                        col("_5").alias("Phone_Number"), col("_6").alias("index").cast(IntegerType()))
    
    company_table.createOrReplaceTempView("Company_Table")
    com_df = spark.sql("select `index` as Company_index, Company_Name, Employer_Identification_Number, SEC_Central_Index_Key, \
                    Registered_State from Company_Table")
    
    return com_df, company_table