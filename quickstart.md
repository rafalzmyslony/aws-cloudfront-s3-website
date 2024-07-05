```shell
export HOSTED_ZONE_ID="/hostedzone/Z0444904IRSUOB0SGBLV"  
export BUCKET_NAME=my-cv-website-from-cli-29052024
```
1. Create/make bucket:  
```shell
aws s3 mb s3://$BUCKET_NAME
```

2. Upload the index.html file.  
```
aws s3 cp index.html s3://$BUCKET_NAME
```

3. Enable static website hosting.  
```
aws s3 website s3://$BUCKET_NAME/ --index-document index.html
```

4. Paste name of S3 bucket into `cloudfront-config.json` - `Origins` and `TargetOriginId` sections.  

5. Create SSL Certificate for website.  
```
aws acm request-certificate --domain-name resume.zmyslony.ovh --validation-method DNS --region us-east-1
```

6. Copy output (arn) to cloudront-config.json in `ACMCertificateArn` section.  

7. Make ssl dns validation (you can also choose email verification), otherwise status is pending. 
Copy and paste CNAME records to this file `create-route53-record.json`:  
```
aws route53 change-resource-record-sets --hosted-zone-id "/hostedzone/Z0444904IRSUOB0SGBLV" --change-batch file://create-route53-record.json 
```


8. Create cloudfront distrobution. 
Customize remaining fields e.g. `cloudfront-config.json` `Aliases` section  
```
aws cloudfront create-distribution --distribution-config file://cloudfront-config.json --region us-east-1
```

9. Create A record to point `resume.zmyslony.ovh` to cloudfront distro.
Then you can see new created record.  
```
aws route53 list-resource-record-sets --hosted-zone-id  "/hostedzone/Z0444904IRSUOB0SGBLV" | jq .ResourceRecordSets
```
where output can look like this:
```
  {
    "Name": "resume.zmyslony.ovh.",
    "Type": "A",
    "AliasTarget": {
      "HostedZoneId": "Z2FDTNDATAQYW2",
      "DNSName": "d3s3xv9posocgm.cloudfront.net.",
      "EvaluateTargetHealth": false
    }
```
10. Add manually javscript code to provide Basic Auth (you must type login and password e.g. John Foobar). You must create function, publish and associate with a given cloudfront distrobution.

You can also via cli:

Display actuall function code
```shell
aws cloudfront get-function --name auth-func --output text output-js-script.text
```
Create function: 
```
aws cloudfront create-function \
    --name MaxAge \
    --function-config '{"Comment":"Max Age 2 years","Runtime":"cloudfront-js-2.0"}' \
    --function-code fileb://cloudfront-function-basic-auth.js
```

Publish function:
```
aws cloudfront get-distribution-config \
    --id DistributionID \
    --output yaml > dist-config.yaml
```

Associate with distro
```
aws cloudfront get-distribution-config \
    --id DistributionID \
    --output yaml > dist-config.yaml
```

11. Clean-up.  


Get Etag
```
aws cloudfront get-distribution-config --id EIVCV622KS7P0 --query 'ETag' --output text
```

Dump distrobution config  
```
aws cloudfront get-distribution-config --id EIVCV622KS7P0 | jq '. | .DistributionConfig' > output-config.tmp
```

In output file find section and set to false:  
```
"DefaultRootObject": null,
"PriceClass": "PriceClass_All",
"Enabled": true,  <-- Set to false
```

Run this command to disable cloudfront distrobution
```
aws cloudfront update-distribution --id EIVCV622KS7P0 --if-match E2O9Z7XMLS873 --region us-east-1 --distribution-config file://output-config.tmp
```


Delete distrobution:  
```
aws cloudfront get-distribution-config --id EIVCV622KS7P0 --query 'ETag' --output text
aws cloudfront delete-distribution --id "EIVCV622KS7P0" --if-match E2ABVKZHMR4PDY  --region us-east-1
```

(optional) Get Etag and ID of cloudfront cache policy 
```shell
aws cloudfront list-cache-policies
aws cloudfront get-cache-policy --id "658327ea-f89d-4fab-a63d-7e88639e58f6" # -> E23ZP02F085DFQ"
aws cloudfront delete-cache-policy --id "658327ea-f89d-4fab-a63d-7e88639e58f6" --if-match E23ZP02F085DFQ --region us-east-1
```

Remove ssl certificate
```
aws acm list-certificates --region us-east-1 | jq .CertificateSummaryList
aws acm delete-certificate --region us-east-1 --certificate-arn "arn:aws:acm:us-east-1:743241827577:certificate/95a0be50-90fc-47b3-a3e1-1010e79c921b"
```

Remove IAM policies:
```
aws iam delete-policy --policy-arn arn:aws:iam::743241827577:policy/SESSendEmailPolicy
```

To remove IAM role first detach IAM policy
```
aws iam detach-role-policy --policy-arn arn:aws:iam::743241827577:policy/SESSendEmailPolicy --role-name send-message-coming-from-contact-form-ses
```
Then remove role
```
aws iam delete-role --role-name send-message-coming-from-contact-form-ses
```

There is also remaining Route53 record A, but we don't pay for it :D

Delete 
```bash
# Get UUID
aws lambda list-event-source-mappings
# Delete
aws lambda delete-event-source-mapping --uuid bd61c523-a462-4a59-8f6b-522a6b9345a8
```