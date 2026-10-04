# Deployment

## Production Configuration
1. Set `APP_ENV=production`. This disables Flask's debug mode.
2. Expose port `5000`.

## AWS Elastic Beanstalk
The `.ebextensions` directory configures deployment for AWS.
Ensure you use `python application.py` as the startup command.
