from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch  
from fastapi import FastAPI 
from pydantic import BaseModel 
from uvicorn.workers import UvicornWorker


model_name = "/gpfs/scratch/acad/trail/Meta-Llama-3.1-70B-Instruct"

model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)
tokenizer = AutoTokenizer.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)

 
# use this model for GPT Neo 125M
 # model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-125m", torch_dtype=torch.float16, low_cpu_mem_usage=True).cuda() 

generate_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    # device=0,  # Use device 0 for initial input; the model is already distributed
    max_new_tokens=1500,
    temperature=0.1,
    top_k=50,
    top_p=0.9,
    repetition_penalty=1.1,
)
    
app = FastAPI() 

class InputPrompt(BaseModel):     
    text: str  

class GeneratedText(BaseModel):     
    text: str  

@app.post("/generate", response_model=GeneratedText) 
async def generate_func(prompt: InputPrompt):     
    output = generate_pipeline(prompt.text)          
    return {"text": output[0]["generated_text"]}