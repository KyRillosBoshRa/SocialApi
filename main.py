from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def root():
  return 'this is just a social media api you can see how it works from /docs'
