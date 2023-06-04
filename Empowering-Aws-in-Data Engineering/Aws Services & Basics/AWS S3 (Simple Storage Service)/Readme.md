# Features & Usecase of _`AWS S3`:_[Offcial Docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
## AWS S3:
- Amazon Simple Storage Service (Amazon S3) is an object storage service that offers industry-leading scalability, data availability, security, and performance. 
- Customers of all sizes and industries can use Amazon S3 to store and protect any amount of data for a range of use cases, such as data lakes, websites, mobile applications, backup and restore, archive, enterprise applications, IoT devices, and big data analytics. 
- Amazon S3 provides management features so that you can optimize, organize, and configure access to your data to meet your specific business, organizational, and compliance requirements.

## Buckets:
- A bucket is a container for objects stored in Amazon S3. You can store any number of objects in a bucket and can have up to 100 buckets in your account.
- Organize the Amazon S3 namespace at the highest level.
- Identify the account responsible for storage and data transfer charges.
- Provide access control options, such as bucket policies, access control lists (ACLs), and S3 Access Points, that you can use to manage access to your Amazon S3 resources.
- Serve as the unit of aggregation for usage reporting.

  ### Objects:
  - Objects are the fundamental entities stored in Amazon S3. Objects consist of **_object data and metadata._** 
  - **The metadata** is a set of name-value pairs that describe the object. 
  - These pairs include some default metadata, such as the date last modified, and standard _HTTP metadata_, such as Content-Type. 
  - You can also specify _custom metadata_ at the time that the object is stored.
  - An **_object_** is uniquely identified within a bucket by a __key__ (name) and a __version ID__ (if S3 Versioning is enabled on the bucket).
  
  ### Keys:
  - An object key (or key name) is the unique identifier for an object within a bucket. Every object in a bucket has exactly one key. 
  - The combination of a bucket, object key, and optionally, version ID (if S3 Versioning is enabled for the bucket) uniquely identify each object. 
  - So you can think of Amazon S3 as a basic data map between "bucket + key + version" and the object itself.
  - Every object in Amazon S3 can be uniquely addressed through the combination of the web service endpoint, bucket name, key, and optionally, a version.
  
  ### S3 Versioning:
  - You can use S3 Versioning to keep multiple variants of an object in the same bucket. 
  - With S3 Versioning, you can preserve, retrieve, and restore every version of every object stored in your buckets. 
  - You can easily recover from both unintended user actions and application failures.

  ### Bucket policy:
  - A bucket policy is a resource-based AWS Identity and Access Management (__IAM__) policy that you can use to grant access permissions to your bucket and the objects in it. 
  - Only the bucket owner can associate a policy with a bucket & Bucket policies are limited to _20 KB_ in size.
  - The permissions attached to the bucket apply to all of the objects in the bucket that are owned by the bucket owner. 
  - Bucket policies use **_JSON_**-based access policy language that is standard across AWS. 
  - You can use bucket policies to add or deny permissions for the objects in a bucket. 
  - Bucket policies allow or deny requests based on the elements in the policy, including the requester, S3 actions, resources, and aspects or conditions of the request
  ``` py
   bucket_policy = {
            'Version': '2012-10-17',
            'Statement': [{
                'Sid': 'PublicReadGetObject',
                'Effect': 'Allow',
                'Principal': '*',
                'Action': ['s3:GetObject'],
                'Resource': f'arn:aws:s3:::{bucketName}/*'
            }]
        }
     ```
    [`Bucket Policy Samples`](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html)
## Accessing AWS S3:

**AWS Management Console:**
- The console is a web-based user interface for managing Amazon S3 and AWS resources.
<p align="center">
  <img src="https://github.com/pnraj/Projects/assets/29162796/1d32379b-8f3b-4592-8578-01a71c988677" alt="S3 Console">
 </p>

**AWS Command Line Interface:**

- You can use the AWS command line tools to issue commands or build scripts at your system's command line to perform AWS (including S3) tasks.
<p align="center">
  <img src="https://github.com/pnraj/Projects/assets/29162796/3cda8557-d243-46c4-873b-28f4e3251dae" alt="AWS CMD">
 </p>
 
List the S3 bucket:
	aws s3 ls

Create bucket:
	
	aws s3 mb s3://your-bucket-name/ --region <use your region>

Create folder and upload a file:

	aws s3 cp file.txt s3://bucket-name/foldername/

Copy Complete folder into s3:

	aws s3 cp foldername/ s3://bucket-name/foldername/ --recursive   # if folder in working directory

Remove bucket:
	
	aws s3 rb foldername/ s3://bucket-name/foldername/

Move object in bucket: 
	
	aws s3 mv foldername/ s3://bucket-name/foldername/

Upload Object into s3:

	aws s3 cp myfile.txt s3://your-bucket-name/

List of Objects in s3:

	aws s3 ls s3://your-bucket-name/

Sync the folder with S3:

	aws s3 sync . s3://your-bucket-name/ 	  	# this for files in current directory 
	aws s3 sync <file path> s3://your-bucket-name/ 	# this for mentioning path to folder that needed to sync

Temp webfile:

	aws s3 presign s3://mybucket/myobject --expires-in 3600

Static Webfile:

	aws s3 website s3://your-bucket-name/ --index-document index.html
	aws s3 sync your-local-folder s3://your-bucket-name
	aws s3api get-bucket-website --bucket your-bucket-name

## AWS SDKs: 

- AWS provides SDKs ([software development kits](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html)) that consist of libraries and sample code for various programming languages and platforms 
- **_Java, Python, Ruby, .NET, iOS, Android_** etc..
- In order to use AWS SDKs we have to create **_aws_access_key_id_ & _aws_secret_access_key_**

  **List Buckets In S3:**
  
  ``` py
    # Python Based Lib boto3
    import boto3 
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    # Output the bucket names
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')
  ```    
  
  **Creating Bucket Using Boto3:**
  
  ``` py
  import boto3
  from botocore.exceptions import ClientError
  import os
  # defining function for creating a bucket
  def create_bucket(api_key,api_secret,bucketName, region=None):
    # if region is not entered bucket will create on default region (us-east-1)
    # try and exception for error handaling
    try:
      s3 = boto3.resource('s3', aws_access_key_id = api_key, aws_secret_access_key=api_secret)
      if region is None:
          s3.create_bucket(Bucket=bucketName)
      else:
          location = {'LocationConstraint': region}
          s3.create_bucket(Bucket=bucketName,
                                  CreateBucketConfiguration=location)
    except ClientError as e:
        return str(e)
    return "Succesfully Created"
    ```
    
    **Upload into s3:**
    
    ``` py
    
      def upload_to_bucket(api_key,api_secret,bucketName,file_path):
        try:
          s3 = boto3.resource('s3', aws_access_key_id = api_key, aws_secret_access_key=api_secret)
          key = os.path.basename(file_path)  # Specify the desired key (filename) in the bucket
          # Upload the file
          s3.Object(bucketName, key).upload_file(file_path)

        except ClientError as e:
          return str(e)
        return "Succefully Uploaded"
        
    ```
    



