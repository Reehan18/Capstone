# Ollama Integration with Django - Setup Guide

## Overview
This guide explains how to use Ollama with your Django-based customized education platform. The integration provides AI-powered features for educational content processing, quiz generation, study plan creation, and more.

## Prerequisites
- Python 3.8+
- Django 5.2+
- Ollama installed and running
- gemma3:4b model (or any compatible model)

## Installation Steps

### 1. Install Required Python Packages
```bash
pip install ollama
pip install djangorestframework
```

### 2. Install and Setup Ollama
```bash
# Install Ollama (if not already installed)
# Download from: https://ollama.ai/

# Pull the gemma3:4b model
ollama pull gemma3:4b

# Start Ollama server
ollama serve
```

### 3. Verify Installation
Run the test script to verify everything is working:
```bash
python test_ai_service_direct.py
```

## API Endpoints

### 1. AI Status Check
**Endpoint:** `GET /api/prediction/status/`
**Description:** Check if Ollama service is available
**Authentication:** Not required

**Response:**
```json
{
    "available": true,
    "model": "gemma3:4b",
    "message": "Ollama is running"
}
```

### 2. Chat with AI
**Endpoint:** `POST /api/prediction/chat/`
**Description:** Simple chat interface with the AI model
**Authentication:** Not required

**Request:**
```json
{
    "input": "Explain photosynthesis to a 10-year-old"
}
```

**Response:**
```json
{
    "result": "Photosynthesis is like cooking for plants! Plants use sunlight, water, and air to make their own food...",
    "model": "gemma3:4b",
    "status": "success"
}
```

### 3. Generate Educational Content
**Endpoint:** `POST /api/prediction/generate/`
**Description:** Generate summaries, quizzes, or study plans
**Authentication:** Required

**Request for Summary:**
```json
{
    "type": "summary",
    "content": "Long educational text to summarize..."
}
```

**Request for Quiz:**
```json
{
    "type": "quiz",
    "topic": "Photosynthesis",
    "num_questions": 5
}
```

**Request for Study Plan:**
```json
{
    "type": "study_plan",
    "materials": ["Biology Chapter 1", "Chemistry Basics"],
    "days": 7
}
```

### 4. Study App AI Endpoints
**Base URL:** `/api/ai/`

- `GET /api/ai/status/` - AI service status
- `POST /api/ai/summarize/` - Summarize study materials
- `POST /api/ai/study-plan/` - Generate study plans
- `POST /api/ai/quiz/` - Generate quiz questions
- `POST /api/ai/chat/` - Chat with AI assistant

## Usage Examples for Your Education Platform

### 1. Document Processing and Summarization
When a student uploads a syllabus or document:

```python
# In your view
from ai_service import ollama_service

def process_uploaded_document(request):
    # Get uploaded document content
    document_content = extract_text_from_document(request.FILES['document'])
    
    # Generate summary
    summary = ollama_service.summarize_text(document_content)
    
    # Save to database
    StudyMaterial.objects.create(
        user=request.user,
        title=request.data.get('title'),
        content=document_content,
        summary=summary
    )
```

### 2. Personalized Study Plan Generation
```python
def create_study_plan(request):
    # Get user's materials
    materials = StudyMaterial.objects.filter(user=request.user)
    material_titles = [m.title for m in materials]
    
    # Get study period
    end_date = request.data.get('end_date')
    days = calculate_days_until(end_date)
    
    # Generate AI study plan
    study_plan = ollama_service.generate_study_plan(material_titles, days)
    
    # Save plan
    StudyPlan.objects.create(
        user=request.user,
        plan_data=study_plan,
        end_date=end_date
    )
```

### 3. Daily Quiz Generation
```python
def generate_daily_quiz(request):
    # Get today's study topics
    today_topics = get_todays_study_topics(request.user)
    
    # Generate quiz for each topic
    quizzes = []
    for topic in today_topics:
        quiz = ollama_service.generate_quiz_questions(topic, 3)
        quizzes.extend(quiz)
    
    return Response({'quizzes': quizzes})
```

### 4. Learning Level Analysis
```python
def analyze_student_progress(request):
    # Get student's quiz responses
    responses = QuizResponse.objects.filter(user=request.user)
    
    # Get study content
    content = get_user_study_content(request.user)
    
    # Analyze learning level
    analysis = ollama_service.analyze_learning_level(
        responses, 
        content
    )
    
    return Response(analysis)
```

## Configuration Options

### Model Selection
You can change the AI model in `ai_service.py`:
```python
# For different models
ollama_service = OllamaService("llama3:8b")  # Larger model
ollama_service = OllamaService("llama3.2:latest")  # Latest version
```

### Custom Prompts
Modify system prompts for different educational contexts:
```python
# In ai_service.py
system_prompt = """You are an AI tutor specializing in [SUBJECT]. 
Provide clear explanations suitable for [GRADE_LEVEL] students."""
```

## Troubleshooting

### Common Issues

1. **"Ollama service not available"**
   - Ensure Ollama is running: `ollama serve`
   - Check if the model is pulled: `ollama list`

2. **"Model not found"**
   - Pull the required model: `ollama pull gemma3:4b`

3. **Slow responses**
   - Consider using a smaller model for faster responses
   - Implement caching for frequently requested content

4. **Memory issues**
   - Monitor system resources
   - Consider using model quantization

### Performance Tips

1. **Caching:** Implement Redis caching for AI responses
2. **Async Processing:** Use Celery for long-running AI tasks
3. **Model Management:** Load models on-demand to save memory
4. **Response Streaming:** Stream responses for better UX

## Next Steps

1. **Implement file upload processing** for PDFs, DOCX, etc.
2. **Add progress tracking** for study plans
3. **Create adaptive learning** based on quiz performance
4. **Implement offline capabilities** with local model storage
5. **Add multi-language support** for international students

## Security Considerations

1. **Rate limiting:** Implement rate limiting for AI endpoints
2. **Input validation:** Sanitize all user inputs
3. **Authentication:** Secure sensitive endpoints
4. **Data privacy:** Handle student data according to regulations
