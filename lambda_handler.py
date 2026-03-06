"""
Indic-Setu AWS Lambda Handler
Connects to Amazon Bedrock Claude 3 Sonnet for government scheme eligibility assessment
"""

import json
import boto3
import base64
from botocore.exceptions import ClientError

# Initialize Bedrock client
bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    """
    Main Lambda handler for Indic-Setu
    
    Expected input JSON:
    {
        "query": "What schemes am I eligible for?",
        "income": 80000,
        "occupation": "Farmer"
    }
    """
    
    # CORS headers for frontend connectivity
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type": "application/json"
    }
    
    try:
        # Parse request body
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event
        
        query = body.get('query', '')
        income = body.get('income', 0)
        occupation = body.get('occupation', '')
        
        # Validate inputs
        if not query or income < 0 or not occupation:
            return {
                'statusCode': 400,
                'headers': cors_headers,
                'body': json.dumps({
                    'error': 'Missing required fields: query, income, occupation',
                    'answer': 'कृपया सभी जानकारी भरें। Please fill all information.',
                    'eligibility_status': 'Invalid Input',
                    'voice_text': 'कृपया सभी जानकारी भरें।'
                })
            }
        
        # Determine eligibility status based on income and occupation
        priority_occupations = ['Farmer', 'Labourer', 'Khet Mazdoor', 'Krishi Mazdoor']
        is_high_priority = (income < 100000 and 
                           any(occ.lower() in occupation.lower() for occ in priority_occupations))
        
        eligibility_status = "High-Priority" if is_high_priority else "Standard"
        
        # Create prompt for Claude 3 Sonnet
        system_prompt = """You are an experienced Government Caseworker (Sarkari Karmchari) for rural India with deep knowledge of government schemes and welfare programs.

Your role:
- Assess eligibility for government schemes (MGNREGA, PM-Kisan, PMJDY, PMAY, SSY, etc.)
- Provide personalized, compassionate guidance in simple Hindi-English mix
- Consider income, occupation, and specific circumstances
- Be encouraging and supportive

Always respond in a mix of Hindi and English that rural people understand.
Format your response clearly with:
1. Direct answer to their question
2. Specific schemes they might qualify for
3. Next steps they should take

Keep language simple and warm."""
        
        user_message = f"""
Customer Details:
- Income: ₹{income} per year
- Occupation: {occupation}
- Priority Status: {'High-Priority (Income < 1L)' if is_high_priority else 'Standard'}
- Question: {query}

Please provide personalized government scheme recommendations for this person.
"""
        
        # Call Bedrock Claude 3 Sonnet
        response = bedrock_client.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-06-01',
                'max_tokens': 1024,
                'system': system_prompt,
                'messages': [
                    {
                        'role': 'user',
                        'content': user_message
                    }
                ]
            })
        )
        
        # Parse Bedrock response
        response_body = json.loads(response['body'].read().decode('utf-8'))
        ai_answer = response_body['content'][0]['text']
        
        # Create voice-friendly text (for text-to-speech)
        voice_text = create_voice_text(ai_answer, occupation, income, is_high_priority)
        
        # Return response with CORS headers
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({
                'answer': ai_answer,
                'eligibility_status': eligibility_status,
                'voice_text': voice_text,
                'income': income,
                'occupation': occupation,
                'is_high_priority': is_high_priority
            }, ensure_ascii=False, indent=2)
        }
        
    except ClientError as e:
        error_message = str(e)
        print(f"Bedrock API Error: {error_message}")
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({
                'error': 'Bedrock service error',
                'answer': 'क्षमा करें, सेवा अभी उपलब्ध नहीं है। Sorry, service temporarily unavailable.',
                'eligibility_status': 'Service Error',
                'voice_text': 'क्षमा करें, सेवा अभी उपलब्ध नहीं है।'
            })
        }
    
    except Exception as e:
        error_message = str(e)
        print(f"Unexpected Error: {error_message}")
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({
                'error': f'Server error: {error_message}',
                'answer': 'कोई त्रुटि हुई। कृपया पुनः प्रयास करें। An error occurred. Please try again.',
                'eligibility_status': 'Error',
                'voice_text': 'कोई त्रुटि हुई। कृपया पुनः प्रयास करें।'
            })
        }


def create_voice_text(ai_answer, occupation, income, is_high_priority):
    """
    Create a voice-friendly version of the response
    Optimized for text-to-speech in Hindi-English
    """
    voice_greeting = "नमस्ते, " if is_high_priority else "हेलो, "
    
    # Extract first 300 characters for voice (TTS friendly)
    summary = ai_answer[:500] if len(ai_answer) > 500 else ai_answer
    
    # Remove complex formatting
    summary = summary.replace('**', '').replace('##', '')
    
    priority_text = (
        "आप उच्च प्राथमिकता के लिए योग्य हैं। "
        "You are HIGH PRIORITY eligible. " 
        if is_high_priority 
        else "आपके लिए कई योजनाएं उपलब्ध हैं। Several schemes available for you. "
    )
    
    voice_text = f"{voice_greeting} {priority_text} {summary}"
    
    return voice_text
