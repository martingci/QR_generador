---
on:
  workflow_dispatch:
permissions:
  contents: read
engine:
  id: codex
  model: openai/gpt-5.6-luna
  env:
    # Route Codex inference to OpenRouter instead of api.openai.com.
    # Setting this also makes gh-aw emit apiProxy.modelFallback.enabled: false so the
    # provider-qualified model slug is passed through verbatim.
    # The credential is NOT declared here: the Codex engine already defaults
    # OPENAI_API_KEY to ${{ secrets.CODEX_API_KEY || secrets.OPENAI_API_KEY }}, so the
    # repo secret is simply named OPENAI_API_KEY. Its VALUE is an OpenRouter key
    # (sk-or-v1-...), despite the name.
    OPENAI_BASE_URL: https://openrouter.ai/api/v1
    # gh-aw strips the "openai/" provider prefix before handing the model to the Codex CLI
    # (codexModelID in pkg/workflow/codex_engine.go), but OpenRouter requires the full
    # "vendor/model" slug. engine.env is merged over the compiler-set model variable, so
    # re-declaring it here restores the prefix. The detection job reads its own variable.
    GH_AW_MODEL_AGENT_CODEX: openai/gpt-5.6-luna
    GH_AW_MODEL_DETECTION_CODEX: openai/gpt-5.6-luna
network:
  allowed:
    - defaults
    - openrouter.ai
safe-outputs:
  create-issue:
    max: 1
jobs:
  security-scan:
    name: Run CodeQL and Grype
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
    outputs:
      summary: ${{ steps.summarize.outputs.summary }}
    steps:
      - name: Checkout repository
        uses: actions/checkout@v7
        with:
          fetch-depth: 1
          persist-credentials: false

      - name: Prepare report directory
        run: mkdir -p security-scan-reports

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: python
          queries: security-and-quality

      - name: Perform CodeQL analysis
        uses: github/codeql-action/analyze@v3
        with:
          category: /language:python
          upload: false
          output: security-scan-reports/codeql

      - name: Run Grype dependency scan
        uses: anchore/scan-action@v6
        with:
          path: .
          fail-build: false
          output-format: sarif
          output-file: security-scan-reports/grype.sarif

      - name: Summarize SARIF reports
        id: summarize
        shell: bash
        run: |
          python3 .github/scripts/summarize_sarif.py security-scan-reports

          # Use a delimiter that cannot appear in the report's code snippets.
          {\
            echo 'summary<<GH_AW_SECURITY_SCAN_EOF'
            cat security-scan-reports/summary.md
            echo GH_AW_SECURITY_SCAN_EOF
          } >> "$GITHUB_OUTPUT"

      - name: Upload security scan reports
        uses: actions/upload-artifact@v7
        with:
          name: security-scan-reports
          path: security-scan-reports
          if-no-files-found: error

---
# codex-security-scan

Run a CodeQL security analysis using the Python codebase and run Grype against the project's dependencies. Create one GitHub issue containing the findings from both tools. Include severity, affected files or packages, evidence, and recommended remediation. If a tool cannot run, report that clearly in the issue.

Use the deterministic security scan report below to create one GitHub issue containing the CodeQL and Grype findings. Do not inspect local files, invoke file-reading tools, or invent findings. If both scanners report no findings, call `noop` with a message explaining that the scan completed without findings.

Every finding you report must include, in this order:

1. **Severity** exactly as given in the report.
2. **Rule ID** (for example `py/mixed-returns` or the CVE identifier).
3. **Location** as `path/to/file.py:LINE`. Always give the file and line number; the report already contains them, so never drop or guess them.
4. **Evidence** — a fenced code block reproducing the reported snippet with the offending line visible, so a reader can see the problem without opening the file.
5. **Remediation** — the specific change to make, taken from the report.

Group findings by tool, order each group by descending severity, and keep the report's findings that fit under the limits. Do not merge distinct rules into a single bullet, and do not add findings that are absent from the report.

## Security scan report

${{ needs.security-scan.outputs.summary }}
