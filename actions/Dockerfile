FROM rasa/rasa-sdk:2.8.1
WORKDIR /app
COPY requirement.txt requirement.txt
USER root
RUN pip install -r requirement.txt
EXPOSE 5055
USER 1001
