# HOI-unlimited

**HOI-unlimited** is a DevOps-focused project that integrates various tools and technologies to streamline and automate development, deployment, and infrastructure management processes. This repository showcases the implementation of modern DevOps practices using tools like Docker, AWS EKS, Terraform, GitHub Actions, SonarQube, Trivy, and Slack notifications.

## Key Features

- **Containerization with Docker**: Applications are containerized for consistency and portability across environments.
- **Orchestration with AWS EKS**: Kubernetes clusters are deployed and managed on AWS Elastic Kubernetes Service (EKS).
- **Infrastructure as Code (IaC)**: Terraform is used for provisioning and managing infrastructure resources.
- **CI/CD Pipelines**: GitHub Actions is leveraged to automate build, test, and deployment workflows.
- **Code Quality and Security**:
  - **SonarQube**: Integrated for code quality and static analysis.
  - **Trivy**: Used for vulnerability scanning of Docker images and Kubernetes clusters.
- **Notifications**: Slack notifications are configured to alert about pipeline updates, security scans, and other critical events.
- **Shell Scripting**: Various scripts are included to automate repetitive tasks and enhance project efficiency.

## Technology Stack

- **HTML (50.2%)**: Used for front-end components or documentation.
- **Python (31%)**: For scripting, automation, or application logic.
- **HCL (9.8%)**: For defining infrastructure configurations via Terraform.
- **Shell (7.1%)**: For automation scripts.
- **Dockerfile (1.9%)**: For building Docker images.

## Getting Started

### Prerequisites

- AWS account with permissions to manage EC2 instances and EKS clusters.
- Terraform installed on the EC2 instance or virtual machine.
- SonarQube and Trivy set up on the EC2 instance or virtual machine.
- Slack workspace for receiving notifications.

### Installation and Deployment

All setup and deployment are performed **on EC2 instances or virtual machines**. There is no need to install tools on your local machine. Follow these steps:

1. **Clone the Repository**:
   - SSH into your EC2 instance or virtual machine.
   - Clone the repository:
     ```bash
     git clone https://github.com/VasuBhimani/HOI-unlimited.git
     cd HOI-unlimited
     ```

2. **Set up Docker**:
   - Build Docker images using the provided `Dockerfile`.
   - Run containers as specified in the documentation.

3. **Deploy to AWS EKS**:
   - Use the Terraform configuration files to provision the EKS cluster.
   - Apply the Terraform scripts:
     ```bash
     terraform init
     terraform apply
     ```

4. **Configure CI/CD with GitHub Actions**:
   - Ensure your repository secrets (e.g., AWS credentials, SonarQube tokens, Slack Webhook URL) are configured in GitHub.
   - Review the `.github/workflows` directory for pipeline configurations.

5. **Set up SonarQube and Trivy**:
   - Install and configure SonarQube on the EC2 instance for static code analysis.
   - Use Trivy for vulnerability scanning in Docker images and Kubernetes clusters.

6. **Configure Slack Notifications**:
   - Set up a Slack Webhook and integrate it with the CI/CD pipelines for real-time alerts.

## Usage

- **Development**: Use the EC2 instance or virtual machine as your development environment.
- **Deployment**: Deploy applications to AWS EKS using the CI/CD pipelines.
- **Code Quality and Security**: Run SonarQube and Trivy checks to ensure code and infrastructure security.
- **Notifications**: Receive updates and alerts via Slack for pipeline and scanning results.
