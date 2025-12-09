import os
import json
import urllib.request
import urllib.error
import datetime
from dataclasses import dataclass
from typing import List, Dict, Any


# 1. Custom Exceptions
class AppError(Exception):
    """Base class for other application-specific exceptions"""
    pass

class APIConnectionError(AppError):
    """Raised when the external API connection fails"""
    pass

class DataParseError(AppError):
    """Raised when fetched data cannot be parsed correctly"""
    pass

# ==========================================
# 2. Data Models
# ==========================================
@dataclass
class UserData:
    """
    Data class to represent user data.
    """
    id: int
    name: str
    username: str
    email: str
    company_name: str
    city: str

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> 'UserData':
        try:
            return cls(
                id=data.get('id'),
                name=data.get('name'),
                username=data.get('username'),
                email=data.get('email'),
                company_name=data.get('company', {}).get('name', 'N/A'),
                city=data.get('address', {}).get('city', 'N/A')
            )
        except AttributeError as e:
            raise ValueError(f"Invalid data structure: {e}")

# ==========================================
# 3. API Client (Standard Library Implementation)
# ==========================================
class ApiClient:
    """
    Class to handle external API interactions using standard 'urllib'.
    No external dependencies (pip install) required.
    """
    BASE_URL = "https://jsonplaceholder.typicode.com/users"

    def fetch_data(self) -> List[UserData]:
        print(f"Fetching data from {self.BASE_URL}...")
        try:
            with urllib.request.urlopen(self.BASE_URL, timeout=10) as response:
                if response.status != 200:
                    raise APIConnectionError(f"HTTP Error: {response.status}")
                
                data = response.read()
                data_list = json.loads(data)
                
                users = []
                for item in data_list:
                    users.append(UserData.from_json(item))
                
                print(f"Successfully fetched {len(users)} records.")
                return users

        except urllib.error.URLError as e:
            raise APIConnectionError(f"Network Error: {e.reason}")
        except json.JSONDecodeError as e:
            raise DataParseError(f"JSON Decode Error: {e}")
        except Exception as e:
            raise AppError(f"Unexpected Error: {e}")


# 4. Report Generator
class ReportGenerator:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except OSError:
                pass # Ignore if exists

    def generate_text_report(self, users: List[UserData]) -> str:
        lines = []
        lines.append("=" * 60)
        lines.append(f"{'PORTABLE DOC REPORT':^60}")
        lines.append("=" * 60)
        lines.append(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("-" * 60)
        
        for user in users:
            lines.append(f"ID       : {user.id}")
            lines.append(f"Name     : {user.name}")
            lines.append(f"Username : {user.username}")
            lines.append(f"Email    : {user.email}")
            lines.append(f"Company  : {user.company_name}")
            lines.append(f"City     : {user.city}")
            lines.append("-" * 30)
            
        lines.append(f"Total Users: {len(users)}")
        return "\n".join(lines)

    def save_to_file(self, content: str, filename: str):
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Report saved to: {os.path.abspath(filepath)}")


# 5. Main Execution
if __name__ == "__main__":
    print("Starting Portable DOC Generator (Zero-Dependency)...")
    try:
        client = ApiClient()
        users = client.fetch_data()
        
        generator = ReportGenerator("portable_reports")
        report_content = generator.generate_text_report(users)
        
        filename = f"Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        generator.save_to_file(report_content, filename)
        
        print("Done.")
        
    except Exception as e:
        print(f"Fatal Error: {e}")
        input("Press Enter to exit...") # Keeps window open if double-clicked
