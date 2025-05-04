from fastapi import APIRouter

router = APIRouter()

# TODO: check token
@router.post(
    '/chat', 
    summary="Send a message to the chatbot and receive a reply",
    description=""
)
async def chat_completetion(): 
    ...

@router.get(
    '/history', 
    summary="Retrieve conversation history by session",
    description=""
)
async def chat_history(): 
    ...
    

@router.post(
    '/clear', 
    summary="Clear conversation memory by session",
    description=""
)
async def chat_clear(): 
    ...

@router.get(
    '/status', 
    summary="Check chatbot online status",
    description=""
)
async def chat_status(): 
    ...
    