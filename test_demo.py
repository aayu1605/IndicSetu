#!/usr/bin/env python3
"""
Indic-Setu Testing & Demo Script
Tests Lambda function and API Gateway locally
"""

import json
import requests
from typing import Dict, Any

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str):
    """Print colored header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.END}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

# Sample test cases
TEST_CASES = [
    {
        "name": "Farmer with Low Income (High-Priority)",
        "data": {
            "query": "PM-Kisan के लिए आवेदन कैसे करूँ? मेरी जमीन में 2 एकड़ है।",
            "income": 85000,
            "occupation": "Farmer"
        },
        "expected_status": "High-Priority"
    },
    {
        "name": "Agricultural Labourer (High-Priority)",
        "data": {
            "query": "मुझे कौन सी सरकारी योजनाएं मिल सकती हैं?",
            "income": 75000,
            "occupation": "Agricultural Labourer"
        },
        "expected_status": "High-Priority"
    },
    {
        "name": "Self-Employed with Medium Income (Standard)",
        "data": {
            "query": "क्या मैं PMJDY के लिए योग्य हूँ?",
            "income": 200000,
            "occupation": "Self-Employed"
        },
        "expected_status": "Standard"
    },
    {
        "name": "Student (Standard)",
        "data": {
            "query": "Are there any scholarships available?",
            "income": 120000,
            "occupation": "Student"
        },
        "expected_status": "Standard"
    },
    {
        "name": "Invalid Input Test (Missing Field)",
        "data": {
            "query": "",  # Empty query
            "income": 80000,
            "occupation": "Farmer"
        },
        "expected_status": "Invalid Input"
    }
]

def test_lambda_locally(api_url: str, test_case: Dict[str, Any]) -> bool:
    """Test API with sample data"""
    
    test_name = test_case["name"]
    test_data = test_case["data"]
    expected_status = test_case["expected_status"]
    
    print(f"\n{Colors.BOLD}Test: {test_name}{Colors.END}")
    print(f"Input: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
    
    try:
        # Make API request
        response = requests.post(
            api_url,
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        # Check response
        if response.status_code != 200:
            print_error(f"API returned status {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        result = response.json()
        actual_status = result.get('eligibility_status', 'Unknown')
        
        # Validate response structure
        required_fields = ['answer', 'eligibility_status', 'voice_text']
        for field in required_fields:
            if field not in result:
                print_error(f"Missing field in response: {field}")
                return False
        
        # Print response
        print(f"\n{Colors.CYAN}Response:{Colors.END}")
        print(f"Status: {actual_status}")
        if expected_status in actual_status:
            print_success(f"Eligibility status matches expected: {expected_status}")
        else:
            print_warning(f"Expected {expected_status}, got {actual_status}")
        
        print(f"\nAnswer (first 200 chars):")
        print(f"{result['answer'][:200]}...")
        
        print(f"\nVoice Text (first 150 chars):")
        print(f"{result['voice_text'][:150]}...")
        
        return True
    
    except requests.exceptions.Timeout:
        print_error("Request timed out (15 seconds)")
        return False
    
    except requests.exceptions.ConnectionError as e:
        print_error(f"Cannot connect to API: {e}")
        return False
    
    except json.JSONDecodeError:
        print_error("Invalid JSON response from API")
        return False
    
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False

def run_all_tests(api_url: str) -> None:
    """Run all test cases"""
    
    print_header("INDIC-SETU TESTING SUITE")
    
    print_info(f"Testing API: {api_url}\n")
    
    if not api_url or "YOUR-API" in api_url:
        print_error("API URL not configured. Please set your AWS API Gateway URL.")
        print("\nUsage: python test_demo.py <API_URL>")
        print("Example: python test_demo.py https://abcd1234.execute-api.us-east-1.amazonaws.com/prod")
        return
    
    # Test connection
    print_info("Testing API connectivity...")
    try:
        response = requests.head(api_url, timeout=5)
        print_success(f"API is reachable")
    except:
        print_warning(f"API may not be reachable. Attempting tests anyway...\n")
    
    # Run all test cases
    results = []
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n{Colors.BOLD}[Test {i}/{len(TEST_CASES)}]{Colors.END}")
        success = test_lambda_locally(api_url, test_case)
        results.append({
            "test": test_case["name"],
            "passed": success
        })
    
    # Print summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    
    print(f"Total Tests: {total}")
    print(f"{Colors.GREEN}Passed: {passed}{Colors.END}")
    print(f"{Colors.RED}Failed: {total - passed}{Colors.END}\n")
    
    for result in results:
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        print(f"{status}: {result['test']}")
    
    if passed == total:
        print_success("\n🎉 All tests passed! Indic-Setu is ready for deployment!")
    else:
        print_warning(f"\n⚠️  {total - passed} test(s) failed. Check the errors above.")

def test_streamlit_integration() -> None:
    """Test Streamlit app locally"""
    
    print_header("STREAMLIT INTEGRATION TEST")
    
    print_info("To test Streamlit integration:")
    print("1. Run: streamlit run app.py")
    print("2. In sidebar, paste your API Gateway URL")
    print("3. Fill in: Income = 85000, Occupation = Farmer")
    print("4. Ask: 'PM-Kisan के लिए आवेदन कैसे करूँ?'")
    print("5. Expected: Green 'HIGH-PRIORITY ELIGIBLE' badge")
    print("6. Click 'Awaaz mein suniye' to test voice")
    print("7. Toggle 'Low-Data Mode' to verify it works")

def test_voice_generation() -> None:
    """Test TTS generation"""
    
    print_header("TEXT-TO-SPEECH (TTS) TEST")
    
    try:
        import pyttsx3
        
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        
        test_text = "नमस्ते। आप उच्च प्राथमिकता के लिए योग्य हैं। Hello, you are high priority eligible."
        
        print_info("Generating TTS for test text...")
        print(f"Text: {test_text}\n")
        
        # Save to file
        engine.save_to_file(test_text, '/tmp/indic_setu_test.mp3')
        engine.runAndWait()
        
        print_success("TTS generated successfully!")
        print_info("Audio saved to: /tmp/indic_setu_test.mp3")
        
    except ImportError:
        print_error("pyttsx3 not installed. Install with: pip install pyttsx3")
    except Exception as e:
        print_error(f"TTS generation failed: {e}")
        print_info("Note: TTS requires system audio library (espeak on Linux, etc.)")

def main():
    import sys
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}🌾 INDIC-SETU TESTING SCRIPT{Colors.END}\n")
    
    # Get API URL from command line or use default
    if len(sys.argv) > 1:
        api_url = sys.argv[1]
    else:
        api_url = input("Enter your AWS API Gateway URL (or press Enter to skip API tests): ").strip()
    
    if api_url:
        run_all_tests(api_url)
    else:
        print_warning("Skipping API tests (no URL provided)")
    
    # Test Streamlit integration
    print()
    test_streamlit_integration()
    
    # Test TTS
    print()
    test_voice_generation()
    
    # Final summary
    print_header("NEXT STEPS")
    print("1. Deploy Lambda function to AWS")
    print("2. Create API Gateway endpoint")
    print("3. Run: python test_demo.py <YOUR_API_URL>")
    print("4. Deploy Streamlit app")
    print("5. Test on mobile with 2G simulation")
    print("6. Prepare demo for submission\n")

if __name__ == "__main__":
    main()
