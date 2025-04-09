FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY setup.py .
RUN pip install -e .

COPY . .

# Define the entry point for the container.
# This uses the console_scripts entry point defined in setup.py.
ENTRYPOINT ["myapp"]

# Provide a default command-line argument, e.g. "J.K. Rowling".
# This can be overridden when running the container.
CMD ["J.K. Rowling"]
