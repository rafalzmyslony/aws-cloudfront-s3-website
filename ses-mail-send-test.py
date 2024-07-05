import json
import boto3

def lambda_handler():
    ses = boto3.client('ses', region_name='eu-central-1')  # Update region if necessary
    subject = 'subject 1111'
    content = 'Pie eating'
    email_from = 'ra.zmyslony@gmail.com'  # Use your verified email address
    email_to = 'ra.zmyslony@gmail.com'  # The recipient email address

    response = ses.send_email(
        Source=email_from,
        Destination={
            'ToAddresses': [email_to],
        },
        Message={
            'Subject': {
                'Data': subject,
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': content,
                    'Charset': 'UTF-8'
                }
            }
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Email sent.')
    }


a = lambda_handler()
print(a)