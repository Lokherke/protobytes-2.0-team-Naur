import json
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import ChatSession, ChatMessage


# Knowledge base for the AI chatbot
KNOWLEDGE_BASE = {
    'claim_process': {
        'keywords': ['claim process', 'how to claim', 'file claim', 'claim procedure'],
        'response': """Here's how to file an insurance claim in Nepal:

1. **Report the Incident**: Notify your insurance company within 24-48 hours
2. **Document the Damage**: Take clear photos from multiple angles
3. **File an FIR**: Required for major accidents (at police station)
4. **Submit Documents**: Provide policy, registration, license, and photos
5. **Get Survey**: Insurance surveyor will assess the damage
6. **Repair Authorization**: Wait for approval before repairs
7. **Submit Bills**: Provide repair bills for reimbursement

Would you like more details about any step?"""
    },
    'required_documents': {
        'keywords': ['documents', 'papers', 'needed', 'required'],
        'response': """Required documents for vehicle insurance claims:

**Essential Documents:**
- Valid Driving License
- Vehicle Registration Certificate (Blue Book)
- Insurance Policy Document
- Claim Form (filled and signed)
- Damage Photos (multiple angles)

**Additional (if applicable):**
- FIR Copy (for accidents/major damage)
- Repair Estimate from Workshop
- Medical Reports (if injuries)
- Witness Statements
- Police Report

Keep both original and photocopies ready."""
    },
    'claim_rejection': {
        'keywords': ['rejection', 'denied', 'refused', 'why rejected'],
        'response': """Common reasons for claim rejection in Nepal:

1. **Policy Exclusions**: Damage not covered in your policy
2. **Late Reporting**: Delayed claim notification (>48 hours)
3. **Invalid License**: Expired or incorrect license
4. **Drunk Driving**: Incident under alcohol influence
5. **Unauthorized Repairs**: Repairs done without approval
6. **Pre-existing Damage**: Damage before policy start
7. **Commercial Use**: Using private vehicle commercially
8. **Missing Documents**: Incomplete documentation

**Tip**: Always read your policy document carefully and report incidents promptly."""
    },
    'coverage': {
        'keywords': ['coverage', 'covered', 'what is covered', 'include'],
        'response': """Standard Vehicle Insurance Coverage:"""

"""Third-Party Insurance (Mandatory):
- Damage to other vehicles
- Injury to third parties
- Property damage to others

**Comprehensive Insurance:**
- Own vehicle damage (accident)
- Theft of vehicle
- Fire damage
- Natural disasters (flood, earthquake)
- Vandalism
- Personal accident cover

**Not Covered:**
- Normal wear and tear
- Mechanical/electrical failure
- Driving without license
- Drunk driving incidents
- Commercial use (in private policy)

Would you like to know about specific coverage?"""
    },
    'time_limit': {
        'keywords': ['time limit', 'how long', 'deadline', 'when to claim'],
        'response': """Time Limits for Insurance Claims:"""

"""**Time Limits:**

- **Immediate Reporting**: Within 24-48 hours of incident
- **Claim Submission**: Within 7-30 days (varies by insurer)
- **Document Submission**: Within 15 days of claim filing
- **Repair Completion**: Within 30-60 days of approval

**Important**: Late reporting can lead to claim rejection. Always notify your insurer as soon as possible, even if you don't have all documents ready.

Emergency claims can be reported 24/7 through insurer hotlines."""
    },
    'deductible': {
        'keywords': ['deductible', 'excess', 'own expense', 'pay myself'],
        'response': """**Understanding Deductibles (Excess):**

**What is Deductible?**
Amount you must pay before insurance covers the rest.

**Typical Deductibles in Nepal:**
- **Normal Claims**: NPR 1,000 - 3,000
- **Major Claims**: NPR 5,000 - 10,000
- **Windshield Only**: NPR 500 - 1,000

**Example:**
- Repair Cost: NPR 50,000
- Deductible: NPR 3,000
- Insurance Pays: NPR 47,000
- You Pay: NPR 3,000

**Zero Depreciation Add-on**: Eliminates deductible for new vehicles (usually first 1-2 years)."""
    },
    'premium': {
        'keywords': ['premium', 'cost', 'price', 'how much'],
        'response': """**Vehicle Insurance Premium Factors:**

**What Affects Your Premium:**
- Vehicle value and age
- Engine capacity (CC)
- Vehicle type (car, bike, commercial)
- Your age and driving experience
- Claim history (no-claim bonus)
- Location (city/rural)
- Add-on covers selected

**Ways to Reduce Premium:**
- Maintain claim-free years (No-Claim Bonus: 10-50% discount)
- Install security devices
- Choose higher deductible
- Compare quotes from multiple insurers
- Bundle policies (if available)

**Average Premiums (Annual):**
- Motorcycles: NPR 1,500 - 5,000
- Cars: NPR 15,000 - 50,000
- Commercial: NPR 25,000 - 100,000+"""
    },
    'no_claim_bonus': {
        'keywords': ['no claim bonus', 'ncb', 'discount', 'no claim'],
        'response': """**No-Claim Bonus (NCB) Benefits:**

**What is NCB?**
Discount on premium for not making claims.

**NCB Slabs:**
- 1 claim-free year: 10% discount
- 2 claim-free years: 20% discount
- 3 claim-free years: 30% discount
- 4 claim-free years: 40% discount
- 5+ claim-free years: 50% discount (maximum)

**Important Notes:**
- NCB is linked to the policyholder, not vehicle
- Transferable when you buy new vehicle
- Lost if you make a claim
- Some insurers offer NCB protection add-on
- Valid for 90 days after policy expiry

**Tip**: For minor damages, compare repair cost vs. NCB loss before claiming."""
    },
    'greeting': {
        'keywords': ['hello', 'hi', 'namaste', 'hey', 'good morning'],
        'response': "Namaste! I'm your Insurance AI Assistant. I can help you with:\n\n- Understanding claim processes\n- Required documents\n- Coverage details\n- Claim rejection reasons\n- Time limits\n- Premium information\n- And much more!\n\nWhat would you like to know about insurance claims in Nepal?"
    },
    'help': {
        'keywords': ['help', 'assist', 'support', 'what can you do'],
        'response': "I can help you with:\n\n- **Claim Process**: Step-by-step guidance\n- **Documents**: What you need to submit\n- **Coverage**: What's covered and what's not\n- **Rejection Reasons**: Why claims get denied\n- **Time Limits**: When to file claims\n- **Deductibles**: Understanding your share\n- **Premium**: Cost factors and savings\n- **No-Claim Bonus**: Discount benefits\n\nJust ask your question in simple language!"
    },
}


def get_bot_response(user_message):
    """Generate bot response based on user message"""
    message_lower = user_message.lower()
    
    # Check for keyword matches
    for category, data in KNOWLEDGE_BASE.items():
        for keyword in data['keywords']:
            if keyword in message_lower:
                return data['response']
    
    # Default response if no match
    default_responses = [
        "I understand you're asking about insurance claims. Could you please be more specific? You can ask about:\n\n- Claim process\n- Required documents\n- Coverage details\n- Why claims are rejected\n- Time limits\n- Premium costs",
        
        "I'm here to help with insurance claims in Nepal. Could you rephrase your question? Try asking about:\n\n- How to file a claim\n- What documents are needed\n- What's covered\n- Common rejection reasons",
        
        "I want to make sure I help you correctly. Can you tell me more specifically what you need? For example:\n\n- 'How do I file a claim?'\n- 'What documents do I need?'\n- 'Why was my claim rejected?'",
    ]
    
    import random
    return random.choice(default_responses)


@csrf_exempt
@require_http_methods(["POST"])
def chat_message(request):
    """API endpoint to handle chat messages"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        message = data.get('message', '').strip()
        
        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # Create or get session
        if not session_id:
            session_id = str(uuid.uuid4())
            session = ChatSession.objects.create(session_id=session_id)
        else:
            session, created = ChatSession.objects.get_or_create(session_id=session_id)
        
        # Save user message
        ChatMessage.objects.create(
            session=session,
            message_type='user',
            content=message
        )
        
        # Generate bot response
        bot_response = get_bot_response(message)
        
        # Save bot response
        ChatMessage.objects.create(
            session=session,
            message_type='bot',
            content=bot_response
        )
        
        return JsonResponse({
            'success': True,
            'session_id': session_id,
            'response': bot_response,
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def get_chat_history(request, session_id):
    """API endpoint to get chat history"""
    try:
        session = ChatSession.objects.get(session_id=session_id)
        messages = session.messages.all()
        
        history = []
        for msg in messages:
            history.append({
                'type': msg.message_type,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat(),
            })
        
        return JsonResponse({
            'success': True,
            'session_id': session_id,
            'messages': history,
        })
        
    except ChatSession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def clear_chat(request):
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        
        if session_id:
            ChatSession.objects.filter(session_id=session_id).delete()
        
        new_session_id = str(uuid.uuid4())
        
        return JsonResponse({
            'success': True,
            'session_id': new_session_id,
            'message': 'Chat history cleared',
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
