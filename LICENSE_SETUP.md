# Setting Up Licensing with Keygen.sh

This guide explains how to set up and configure the licensing system for Owaiken using [Keygen.sh](https://keygen.sh).

## Overview

Owaiken now includes a licensing system powered by Keygen.sh, which allows you to:

- Restrict access to authorized users only
- Implement trial periods
- Track usage and installations
- Offer different license tiers (trial, standard, team, enterprise)
- Prevent unauthorized distribution

## Setup Instructions

### 1. Create a Keygen.sh Account

1. Sign up for a Keygen.sh account at [https://keygen.sh/signup/](https://keygen.sh/signup/)
2. After signing up, you'll be redirected to your dashboard

### 2. Create a Product

1. Navigate to the Products section in your Keygen.sh dashboard
2. Click "New Product"
3. Fill in the details for your Owaiken product:
   - Name: "Owaiken"
   - Platform: "Desktop"
   - Distribution: "Closed"
4. Click "Create Product"

### 3. Create License Policies

1. Navigate to the Policies section in your Keygen.sh dashboard
2. Create policies for each license tier you want to offer:
   - Trial License (e.g., 14-day expiration)
   - Standard License (e.g., perpetual, single machine)
   - Team License (e.g., perpetual, multiple machines)
   - Enterprise License (e.g., perpetual, unlimited machines)

### 4. Configure Owaiken with Keygen.sh Credentials

1. In your Keygen.sh dashboard, locate your Account ID (found in your account settings)
2. From your Products page, locate your Product ID for Owaiken
3. Add these values to your `.env` file:
   ```
   KEYGEN_ACCOUNT_ID=your_account_id_here
   KEYGEN_PRODUCT_ID=your_product_id_here
   ```
4. Alternatively, you can set these values through the Environment tab in the Owaiken UI

### 5. Generate License Keys

1. Navigate to the Licenses section in your Keygen.sh dashboard
2. Click "New License"
3. Select the appropriate policy
4. Generate the license key
5. Distribute this key to your users

## Using the Licensing System

### For Administrators

1. **Managing Licenses**: Use the Keygen.sh dashboard to create, revoke, or modify licenses
2. **Tracking Usage**: View activation data in the Keygen.sh dashboard
3. **User Management**: Associate licenses with specific users or organizations

### For Users

1. **Activating a License**: 
   - Launch Owaiken
   - Navigate to the License tab
   - Enter the license key
   - Click "Activate License"

2. **License Validation**:
   - Licenses are validated at startup
   - Each license is tied to a specific machine
   - If validation fails, users will be redirected to the License tab

## Troubleshooting

- **Invalid License**: Ensure the license key was entered correctly
- **Already Activated**: A license may be limited to a specific number of machines
- **Expired License**: Contact the administrator for a license renewal
- **Connection Issues**: Ensure internet connectivity for online validation

## Advanced Configuration

For advanced configuration options, refer to the [Keygen.sh documentation](https://keygen.sh/docs/).

You can customize:
- License validation frequency
- Offline grace periods
- Machine fingerprinting methods
- License entitlements and feature flags
