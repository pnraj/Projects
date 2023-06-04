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






There are Four Ways We Can Create A Bucket in S3:
