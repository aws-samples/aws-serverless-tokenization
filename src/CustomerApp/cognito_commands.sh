
YOUR_COGNITO_REGION=us-west-2
YOUR_COGNITO_APP_CLIENT_ID=
YOUR_EMAIL=
YOUR_PASSWORD=Testing@123

echo "Sign up new cognito User"
echo aws cognito-idp sign-up \--region $YOUR_COGNITO_REGION \--client-id $YOUR_COGNITO_APP_CLIENT_ID \--username $YOUR_EMAIL \--password $YOUR_PASSWORD

echo "Verify User"
echo aws cognito-idp confirm-sign-up \--client-id $YOUR_COGNITO_APP_CLIENT_ID \--username $YOUR_EMAIL \--confirmation-code CONFIRMATION_CODE_IN_EMAIL

echo "Get Id Token"
echo aws cognito-idp initiate-auth --auth-flow USER_PASSWORD_AUTH --client-id $YOUR_COGNITO_APP_CLIENT_ID --auth-parameters USERNAME=$YOUR_EMAIL,PASSWORD=$YOUR_PASSWORD

