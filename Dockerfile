ARG BUILD_FROM
FROM $BUILD_FROM

# Install dependencies early so that the build is cheap
# when changing other files.
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /iec62056-21

COPY . .

CMD ["./run.sh"]
