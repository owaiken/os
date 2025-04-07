import os
import requests
import json
import streamlit as st
from datetime import datetime
import hashlib
import platform

class LicenseManager:
    def __init__(self, account_id=None, product_id=None):
        """
        Initialize the license manager with Keygen.sh credentials.
        
        Args:
            account_id: Your Keygen account ID
            product_id: Your Keygen product ID
        """
        self.base_url = "https://api.keygen.sh/v1"
        self.account_id = account_id or os.environ.get("KEYGEN_ACCOUNT_ID")
        self.product_id = product_id or os.environ.get("KEYGEN_PRODUCT_ID")
        self.license_key = None
        self.machine_fingerprint = self._generate_machine_fingerprint()
        self.license_file_path = os.path.join(os.path.expanduser("~"), ".owaiken_license")
        
    def _generate_machine_fingerprint(self):
        """Generate a unique fingerprint for the current machine."""
        system_info = {
            "hostname": platform.node(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "system": platform.system(),
            "version": platform.version(),
        }
        
        fingerprint = hashlib.sha256(json.dumps(system_info, sort_keys=True).encode()).hexdigest()
        return fingerprint
        
    def validate_license(self, license_key=None):
        """
        Validate a license key with Keygen.sh.
        
        Args:
            license_key: The license key to validate
            
        Returns:
            dict: License validation result with status and message
        """
        # Use provided key or try to load from saved file
        if license_key:
            self.license_key = license_key
        else:
            self.license_key = self._load_saved_license()
            
        if not self.license_key:
            return {"valid": False, "message": "No license key provided"}
            
        if not self.account_id or not self.product_id:
            return {"valid": False, "message": "Keygen account or product ID not configured"}
            
        try:
            # Validate the license with Keygen.sh
            headers = {
                "Content-Type": "application/vnd.api+json",
                "Accept": "application/vnd.api+json"
            }
            
            # First check if the license exists and is valid
            validate_url = f"{self.base_url}/accounts/{self.account_id}/licenses/actions/validate-key"
            payload = {
                "meta": {
                    "key": self.license_key,
                    "scope": {
                        "fingerprint": self.machine_fingerprint
                    }
                }
            }
            
            response = requests.post(validate_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                validation = data.get("meta", {}).get("valid", False)
                
                if validation:
                    # If valid, save the license locally
                    self._save_license(self.license_key)
                    return {"valid": True, "message": "License is valid", "data": data}
                else:
                    # Get the validation code to determine why it's invalid
                    code = data.get("meta", {}).get("code")
                    if code == "FINGERPRINT_SCOPE_MISMATCH":
                        return {"valid": False, "message": "License is already activated on another machine"}
                    elif code == "EXPIRED":
                        return {"valid": False, "message": "License has expired"}
                    elif code == "SUSPENDED":
                        return {"valid": False, "message": "License has been suspended"}
                    else:
                        return {"valid": False, "message": f"License is invalid: {code}"}
            else:
                return {"valid": False, "message": f"Error validating license: {response.status_code}"}
                
        except Exception as e:
            return {"valid": False, "message": f"Error connecting to license server: {str(e)}"}
    
    def activate_license(self, license_key):
        """
        Activate a license key for this machine.
        
        Args:
            license_key: The license key to activate
            
        Returns:
            dict: Activation result with status and message
        """
        if not license_key:
            return {"success": False, "message": "No license key provided"}
            
        if not self.account_id or not self.product_id:
            return {"success": False, "message": "Keygen account or product ID not configured"}
            
        try:
            # First validate the license
            validation = self.validate_license(license_key)
            if not validation.get("valid"):
                return {"success": False, "message": validation.get("message")}
                
            # Then activate it with the machine fingerprint
            headers = {
                "Content-Type": "application/vnd.api+json",
                "Accept": "application/vnd.api+json"
            }
            
            # Get the license ID
            license_url = f"{self.base_url}/accounts/{self.account_id}/licenses?key={license_key}"
            response = requests.get(license_url, headers=headers)
            
            if response.status_code != 200:
                return {"success": False, "message": f"Error retrieving license: {response.status_code}"}
                
            license_data = response.json()
            if not license_data.get("data"):
                return {"success": False, "message": "License not found"}
                
            license_id = license_data["data"][0]["id"]
            
            # Create a machine activation
            activation_url = f"{self.base_url}/accounts/{self.account_id}/machines"
            payload = {
                "data": {
                    "type": "machines",
                    "attributes": {
                        "fingerprint": self.machine_fingerprint,
                        "platform": platform.system(),
                        "name": platform.node()
                    },
                    "relationships": {
                        "license": {
                            "data": {
                                "type": "licenses",
                                "id": license_id
                            }
                        }
                    }
                }
            }
            
            response = requests.post(activation_url, headers=headers, json=payload)
            
            if response.status_code in (201, 200):
                # Save the license locally
                self._save_license(license_key)
                return {"success": True, "message": "License activated successfully"}
            else:
                return {"success": False, "message": f"Error activating license: {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "message": f"Error connecting to license server: {str(e)}"}
    
    def _save_license(self, license_key):
        """Save the license key to a local file."""
        try:
            with open(self.license_file_path, "w") as f:
                f.write(license_key)
            return True
        except Exception:
            return False
            
    def _load_saved_license(self):
        """Load the license key from a local file if it exists."""
        try:
            if os.path.exists(self.license_file_path):
                with open(self.license_file_path, "r") as f:
                    return f.read().strip()
        except Exception:
            pass
        return None
        
    def check_offline(self):
        """
        Check if a valid license exists locally for offline use.
        
        Returns:
            bool: True if a valid license exists locally
        """
        license_key = self._load_saved_license()
        return bool(license_key)  # In a real implementation, you'd want to check expiration, etc.

# Helper function to get the license manager instance
def get_license_manager():
    """Get or create a license manager instance."""
    if "license_manager" not in st.session_state:
        st.session_state.license_manager = LicenseManager()
    return st.session_state.license_manager
