# AWS Deployment Guide

This guide will help you deploy the Figma to Dashboard Generator to AWS.

## 🚀 Deployment Options

### Option 1: AWS Elastic Beanstalk (Recommended - Easiest)
### Option 2: AWS Lambda + API Gateway (Serverless)
### Option 3: AWS ECS with Docker

---

## Option 1: AWS Elastic Beanstalk Deployment

### Prerequisites

1. **AWS Account** - [Sign up here](https://aws.amazon.com/)
2. **AWS CLI** - Install AWS CLI
3. **EB CLI** - Elastic Beanstalk CLI

### Step 1: Install AWS CLI

**Windows:**
```powershell
# Download and install from: https://aws.amazon.com/cli/
# Or use chocolatey:
choco install awscli
```

**Verify installation:**
```bash
aws --version
```

### Step 2: Configure AWS Credentials

```bash
aws configure
```

Enter your:
- AWS Access Key ID
- AWS Secret Access Key  
- Default region (e.g., `us-east-1`)
- Default output format (e.g., `json`)

**To get your AWS credentials:**
1. Go to AWS Console → IAM
2. Users → Your User → Security Credentials
3. Create Access Key

### Step 3: Install EB CLI

```bash
pip install awsebcli
```

Verify:
```bash
eb --version
```

### Step 4: Initialize Elastic Beanstalk

```bash
# Navigate to project directory
cd figma-to-dashboard

# Initialize EB
eb init -p python-3.12 figma-to-dashboard --region us-east-1
```

Follow the prompts:
- Select your region
- Enter application name: `figma-to-dashboard`
- Choose Python 3.12
- Setup SSH? (optional, say yes for debugging)

### Step 5: Create Environment and Deploy

```bash
# Create environment (first time)
eb create figma-to-dashboard-env --instance-type t3.micro --single
```

This will:
- Create an EC2 instance
- Set up load balancer (if needed)
- Deploy your application
- Configure security groups

### Step 6: Set Environment Variables

```bash
# Set your API keys
eb setenv FIGMA_TOKEN=your_figma_token_here GEMINI_API_KEY=your_gemini_key_here
```

### Step 7: Open Your Application

```bash
eb open
```

This opens your deployed application in the browser!

### Step 8: View Logs (if needed)

```bash
eb logs
```

### Managing Your Deployment

**Deploy updates:**
```bash
git add .
git commit -m "Update"
eb deploy
```

**Check status:**
```bash
eb status
```

**Terminate environment (to save costs):**
```bash
eb terminate figma-to-dashboard-env
```

---

## Option 2: AWS Lambda Deployment (Serverless)

### Prerequisites
- AWS SAM CLI or Serverless Framework
- Docker (for building Lambda layers)

### Using AWS SAM

1. **Install SAM CLI:**
```bash
pip install aws-sam-cli
```

2. **Create SAM template** (already created as `template.yaml`)

3. **Build:**
```bash
sam build
```

4. **Deploy:**
```bash
sam deploy --guided
```

5. **Set environment variables in Lambda console:**
   - Go to AWS Lambda Console
   - Select your function
   - Configuration → Environment variables
   - Add `FIGMA_TOKEN` and `GEMINI_API_KEY`

---

## Option 3: Windows PowerShell Quick Deploy

Simply run the deployment script:

```powershell
.\deploy-aws.ps1
```

This script will:
✅ Check if EB CLI is installed  
✅ Initialize Elastic Beanstalk  
✅ Create environment  
✅ Set environment variables  
✅ Deploy application  
✅ Open in browser  

---

## 🔐 Security Best Practices

1. **Never commit `.env` file** - Already in `.gitignore`
2. **Use AWS Secrets Manager** for production:
   ```bash
   # Store secrets
   aws secretsmanager create-secret --name figma-token --secret-string "your-token"
   aws secretsmanager create-secret --name gemini-key --secret-string "your-key"
   ```

3. **Enable HTTPS** - EB automatically provides SSL

4. **Set up monitoring** - CloudWatch is auto-configured

---

## 💰 Cost Estimation

**Elastic Beanstalk (t3.micro):**
- **Free Tier**: 750 hours/month for 12 months
- **After Free Tier**: ~$8-10/month
- **Storage**: ~$1/month (EBS)
- **Data Transfer**: First 100GB free

**Lambda (Serverless):**
- **Free Tier**: 1M requests + 400,000 GB-seconds/month
- **After Free Tier**: $0.20 per 1M requests
- **Best for**: Low-traffic applications

**Recommendation**: Start with t3.micro single instance (~$10/month)

---

## 🐛 Troubleshooting

### Issue: Deployment fails

**Check logs:**
```bash
eb logs
```

**Common fixes:**
1. Ensure Python 3.12 is selected
2. Check `requirements.txt` is present
3. Verify `application.py` exists

### Issue: Environment variables not set

```bash
# Re-set them
eb setenv FIGMA_TOKEN=xxx GEMINI_API_KEY=xxx

# Verify
eb printenv
```

### Issue: Application timeout

Increase timeout in `.ebextensions/python.config`:
```yaml
option_settings:
  aws:elasticbeanstalk:command:
    Timeout: 600
```

### Issue: Out of memory

Upgrade instance type:
```bash
eb scale --instance-type t3.small
```

---

## 📊 Monitoring

### CloudWatch Logs

View logs in AWS Console:
1. Go to CloudWatch
2. Log Groups
3. Find `/aws/elasticbeanstalk/figma-to-dashboard-env`

### Application Health

```bash
eb health
```

---

## 🔄 CI/CD with GitHub Actions

Create `.github/workflows/deploy.yml` (example provided in repo).

This enables automatic deployment on every push to `main` branch.

---

## 📞 Support

- **AWS Documentation**: https://docs.aws.amazon.com/elasticbeanstalk/
- **EB CLI Reference**: https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3.html
- **Pricing Calculator**: https://calculator.aws/

---

## ✅ Quick Checklist

- [ ] AWS account created
- [ ] AWS CLI installed and configured
- [ ] EB CLI installed
- [ ] Project pushed to GitHub
- [ ] EB initialized (`eb init`)
- [ ] Environment created (`eb create`)
- [ ] Environment variables set (`eb setenv`)
- [ ] Application tested (`eb open`)
- [ ] Monitoring set up (CloudWatch)

---

**Ready to deploy? Run:**

```powershell
.\deploy-aws.ps1
```

🎉 Your application will be live in 5-10 minutes!
