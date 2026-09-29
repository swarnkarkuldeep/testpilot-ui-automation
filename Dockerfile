# Playwright's official image ships Chromium (and its OS-level dependencies)
# already installed, matching the playwright== version pinned in
# requirements.txt — avoids `playwright install --with-deps` at build time.
FROM mcr.microsoft.com/playwright/python:v1.47.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV HEADLESS=true \
    BASE_URL=https://www.saucedemo.com \
    PYTHONUNBUFFERED=1

# Default to the fast smoke suite; override at `docker run` time, e.g.:
#   docker run --rm testpilot-ui-automation pytest -m regression
CMD ["pytest", "-m", "smoke"]
