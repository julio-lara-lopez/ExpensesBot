# Use the uv bookworm slim image
FROM ghcr.io/astral-sh/uv:bookworm-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies using uv
RUN uv sync

# Expose backend port
EXPOSE 8000

# Set environment variables if needed (example)
# ENV DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/expenses

# Run your backend (replace with your actual entrypoint, e.g. main.py or uvicorn)
CMD ["uv","run","uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]