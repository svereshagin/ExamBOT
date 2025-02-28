FROM rapidfort/python-chromedriver

# Set environment variables
ENV POETRY_VERSION=1.8.4 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH="/project/code"
# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory
WORKDIR /project/code

# Copy dependency files
COPY poetry.lock pyproject.toml /project/code/

# Install pip and Poetry, then install dependencies
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir poetry==1.8.4 \
    && poetry config virtualenvs.create false \
    && poetry install --without dev --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts} \
# Copy the rest of the application code
COPY ./bot /project/code/bot
COPY ./core /project/code/core
