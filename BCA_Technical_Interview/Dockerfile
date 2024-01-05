FROM python:3

WORKDIR /bca

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "collatz_conjecture.py" ]