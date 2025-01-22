FROM python:latest

WORKDIR /app

# Copy over requirements.txt bc caching improvement
COPY ./requirements.txt .

RUN pip install -r requirements.txt

# Now copy over the rest
COPY . .

ENTRYPOINT [ "python3", "-m", "src" ]