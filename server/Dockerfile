FROM python:latest

WORKDIR /app

# Copy over requirements.txt bc caching improvement
COPY ./requirements.txt .

RUN pip install -r requirements.txt

# Now copy over the rest
COPY . .

# may be able to replace serve.py with src.serve.py?
ENTRYPOINT [ "python3", "-m", "src" ]