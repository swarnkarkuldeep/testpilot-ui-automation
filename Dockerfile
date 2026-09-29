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
    PYTHONUNBUFFERED=1 \
    TEST_SUITE=regression \
    PORT=8000

EXPOSE 8000

# Runs the test suite, then serves the project site + report — see
# docker-entrypoint.sh. Override the suite at `docker run` time, e.g.:
#   docker run -p 8000:8000 -e TEST_SUITE=smoke testpilot-ui-automation
CMD ["sh", "docker-entrypoint.sh"]
