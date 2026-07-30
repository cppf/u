FROM python:3.12-slim AS build
WORKDIR /src
COPY requirements.txt ./
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
RUN mkdir -p /data
COPY --from=build /root/.local /root/.local
COPY main.py ./
COPY deploy_config.py ./
COPY core/ ./core/
COPY rendering/ ./rendering/
COPY telegram_ui/ ./telegram_ui/
COPY stats/ ./stats/
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8080
ENTRYPOINT ["python", "main.py"]
