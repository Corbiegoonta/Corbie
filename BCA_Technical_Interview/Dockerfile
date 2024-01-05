FROM python:3

WORKDIR /bca

COPY . .

RUN pip install --no-cache-dir -r /bca/requirements.txt

CMD [ "python", "collatz_conjecture.py" ]