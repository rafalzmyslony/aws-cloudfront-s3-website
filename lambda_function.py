import json
import boto3

''' Lambda receive form data like subject and message and sends it to my address email via aws SES

Event `body` may contains something like this:
{
  "name": "aa",
  "email": "asffsaf@afs.com",
  "subject": "Jabroni test",
  "message": "What is Lorem Ips"
}

BUT if you used Api Gateway as endpoint, and Lambda is only intergration, then in `event` there is no `body` dictionary. JSON which is passed is directly
in this format:
{'name': 'aa', 'email': 'asffsaf@afs.com', 'subject': 'Jabroni test', 'message': 'What is Lorem Ips'}

!!! event is already dictionary
'''
def send_email(recipient, name, subject, content):
    ses = boto3.client('ses', region_name='eu-central-1')  # Update region if necessary
    subject = subject
    content = content
    name = name
    email_from = 'ra.zmyslony@gmail.com'  # Use your verified email address
    email_to = 'ra.zmyslony@gmail.com'  # The recipient email address
    
    try:
        
        # For testing purposes
        # raise Exception('Exception message to break try statement')
        response = ses.send_email(
            Source=email_from,
            Destination={
                'ToAddresses': [email_to],
            },
            Message={
                'Subject': {
                    'Data': subject + ' from '+ recipient,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': 'Name of sender is: ' + name + ' Here is a content: ' + content,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        print('Function send_email  logs: ')
        print(response)
        return_json = {
            'statusCode': 201,
            'body': json.dumps('Email sent.')
        }
    except Exception as e:
        print(e)
        return_json = {
            'statusCode': 202,
            'body': json.dumps('Email has not been sent.')
        }
    print(return_json)
    return return_json
    
    
def lambda_handler(event, context):
    print('Lets see event:')
    print(event)
    print('Lets see context:')
    print(context)
    print('records       ')
    for record in event['Records']:
        print(record['body'])
        message_body = record['body']
        print(type(message_body))
        print(message_body)

        try:
            '''If only Lambda URL as endpoint, then
            print('Try statement:')
            message_body = event.get('body')
            print(message_body)
            print(type(message_body))
            message_body = json.loads(message_body)    
            
            # If Api Gateway and Lamba integration, then
            print('Try statement:')
            message_body = event
            print(message_body)
            print(type(message_body))
            '''
            #If Api GW + SQS + Lambda then
            message_body = json.loads(record['body']) 
            
            email = message_body.get('email')
            name = message_body.get('name')
            subject = message_body.get('subject')
            message = message_body.get('message')
            print(message_body)
            response = send_email(email, name, subject, message)
            print('Here response from send_email in lambda_handler function:')
            print(response)
            if response.get('statusCode') == 202:
                return {
                    'statusCode': 202,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',  # Allow requests from any origin
                        'Access-Control-Allow-Methods': 'POST',
                        'Access-Control-Allow-Headers': 'Content-Type'
                    },
                    'body': json.dumps({'error': response.get('body')})
                } 
            return {
                'statusCode': 201,
                'headers': {
                    'Access-Control-Allow-Origin': '*',  # Allow requests from any origin
                    'Access-Control-Allow-Methods': 'POST',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'Status': 'Success'})
            }
        except Exception as e:
            print('Exception statement:')
            return {
                'statusCode': 202,
                'headers': {
                    'Access-Control-Allow-Origin': '*',  # Allow requests from any origin
                    'Access-Control-Allow-Methods': 'POST',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'error': str('Something is wrong in Lamda function. You should check CloudWatch. Probaly there is no specific keys in body dictionary. Make sure, you invoke this function from my contact form on my website.')})
            }
