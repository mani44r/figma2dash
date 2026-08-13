# 🚀 Deploy to AWS NOW - Quick Start Guide

## Prerequisites Check

✅ AWS EB CLI installed  
✅ Project files ready  
✅ API keys configured locally  

---

## 🎯 One-Command Deployment

Run this command to deploy everything automatically:

```powershell
.\deploy-aws.ps1
```

---

## 📋 Manual Step-by-Step Deployment

### Step 1: Configure AWS Credentials

If you haven't configured AWS CLI yet:

```bash
aws configure
```

**You'll need:**
- AWS Access Key ID
- AWS Secret Access Key
- Default region: `us-east-1` (or your preferred region)
- Default output format: `json`

**To get AWS credentials:**
1. Go to [AWS Console](https://console.aws.amazon.com/)
2. Click your name (top right) → Security Credentials
3. Access keys → Create access key
4. Download the CSV file with your credentials

### Step 2: Initialize Elastic Beanstalk

```bash
eb init
```

**Answer the prompts:**
- Select region: `us-east-1` (or your preference)
- Application name: `figma-to-dashboard`
- Platform: `Python 3.12`
- Setup SSH: `yes` (recommended for debugging)

### Step 3: Create Environment and Deploy

```bash
eb create figma-to-dashboard-env
```

This will:
- Create EC2 instance
- Install dependencies
- Deploy your application
- Takes ~5-10 minutes

###Step 4: Set Environment Variables

```bash
eb setenv FIGMA_TOKEN=figd_WeiP_Q0_R7fO-N2lsgNV3SCHMUXE79vX_AiFiFV9 GEMINI_API_KEY=AIzaSyCAQ.Ab8RN6KxgYbpRiXoXC68RjVKCHGs__hHcgm1l7XeOraGKlc-1A
```

### Step 5: Open Your Application

```bash
eb open
```

🎉 **Your application is now live!**

---

## 🔍 Monitoring and Management

### View application status:
```bash
eb status
```

### View logs:
```bash
eb logs
```

### View real-time logs:
```bash
eb logs --stream
```

### SSH into instance:
```bash
eb ssh
```

---

## 🔄 Updating Your Application

After making code changes:

```bash
git add .
git commit -m "Your update message"
git push origin main
eb deploy
```

---

## 💰 Cost Information

**FREE TIER (First 12 months):**
- 750 hours/month of t2.micro or t3.micro

**After Free Tier:**
- t3.micro: ~$0.0104/hour = ~$7.50/month
- Storage: ~$1/month
- Data Transfer: First 100GB free

**Total: ~$10/month**

---

## 🛑 Stopping/Terminating

### Temporarily stop (saves money):
```bash
eb scale 0
```

### Resume:
```bash
eb scale 1
```

### Permanently delete (saves all costs):
```bash
eb terminate figma-to-dashboard-env
```

⚠️ Warning: This deletes everything!

---

## 🐛 Troubleshooting

### Deployment failed?

1. **Check logs:**
   ```bash
   eb logs
   ```

2. **Common issues:**
   - Missing `application.py` → Already added ✅
   - Wrong Python version → Set to 3.12 ✅
   - Environment variables not set → Run `eb setenv` again

3. **Verify environment variables:**
   ```bash
   eb printenv
   ```

### Application not responding?

1. **Check health:**
   ```bash
   eb health
   ```

2. **Restart:**
   ```bash
   eb restart
   ```

### Out of memory?

Upgrade instance type:
```bash
eb scale --instance-type t3.small
```

---

## 📊 Monitoring

### AWS Console

1. Go to [AWS Console](https://console.aws.amazon.com/)
2. Services → Elastic Beanstalk
3. Select your environment
4. View:
   - Health dashboard
   - Monitoring (CPU, Network, Requests)
   - Logs
   - Configuration

### CloudWatch

Automatic logging to CloudWatch:
- Service → CloudWatch
- Logs → Log groups
- Find: `/aws/elasticbeanstalk/figma-to-dashboard-env`

---

## ✅ Post-Deployment Checklist

- [ ] Application deployed successfully
- [ ] Can access via EB URL
- [ ] Environment variables set
- [ ] Health status is "Ok" (green)
- [ ] Tested with sample Figma URL
- [ ] Monitoring set up in CloudWatch
- [ ] Cost alerts configured (optional)

---

## 🔐 Security Best Practices

1. **Enable HTTPS:**
   ```bash
   eb config
   ```
   Add SSL certificate (EB provides one)

2. **Set up monitoring alerts:**
   - Go to CloudWatch
   - Create alarms for CPU, memory, errors

3. **Regular updates:**
   ```bash
   eb upgrade
   ```

4. **Backup strategy:**
   - Your code is in GitHub ✅
   - Environment config can be saved:
     ```bash
     eb config save
     ```

---

## 🎯 Your Deployment URLs

After deployment, you'll get:
- **Application URL:** `figma-to-dashboard-env.us-east-1.elasticbeanstalk.com`
- **Health Dashboard:** AWS Console → Elastic Beanstalk
- **Logs:** CloudWatch → Log Groups

---

## 🆘 Need Help?

- **EB CLI Commands:** `eb --help`
- **AWS Documentation:** https://docs.aws.amazon.com/elasticbeanstalk/
- **Community:** Stack Overflow + AWS Forums

---

## 🚀 Ready to Deploy?

Run this now:

```powershell
.\deploy-aws.ps1
```

Or manual deployment:

```bash
eb init
eb create figma-to-dashboard-env
eb setenv FIGMA_TOKEN=your_token GEMINI_API_KEY=your_key
eb open
```

**Deployment time: 5-10 minutes** ⏱️

🎉 **Your app will be live on AWS!**
