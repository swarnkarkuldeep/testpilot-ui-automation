#!/bin/sh
# Runs the test suite once on container start, then serves the project
# showcase site and the generated report over HTTP — so a plain
# `docker run` (or clicking "Run" in Docker Desktop) is the entire demo,
# nothing to type or remember.
set -u

SUITE="${TEST_SUITE:-regression}"
PORT="${PORT:-8000}"

echo "============================================================"
echo " TestPilot UI Automation"
echo " Running the $SUITE suite against $BASE_URL ..."
echo "============================================================"
echo ""

# Don't let a flaky network hiccup against the live external site kill the
# container before the demo server comes up.
pytest -m "$SUITE" --alluredir=allure-results
TEST_EXIT_CODE=$?

echo ""
echo "============================================================"
if [ "$TEST_EXIT_CODE" -eq 0 ]; then
  echo " All tests passed."
else
  echo " Some tests failed (exit code $TEST_EXIT_CODE) — see the report below."
fi
echo ""
echo " Demo is ready:"
echo "   Project overview : http://localhost:$PORT/site/"
echo "   Test report      : http://localhost:$PORT/reports/report.html"
echo "============================================================"
echo ""

exec python -m http.server "$PORT"
