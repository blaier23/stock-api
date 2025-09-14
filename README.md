# Stock API (FastAPI)

## Run:
- cd dbAssignment
- docker build -t stock-api .
- docker run --env-file .env -p 8000:8000 stock-api
- http://localhost:8000/docs
- pytest tests/ -v

## Notes:
- Made use of Chatgpt 
- Requires docker
- Tested under python 3.11