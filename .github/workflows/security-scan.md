---
on:
  workflow_dispatch:
permissions:
  contents: read
  copilot-requests: write
engine:
  id: copilot
steps:
  - name: Download security scan reports
    uses: actions/download-artifact@v8
    with:
      name: security-scan-reports
      path: security-scan-reports
safe-outputs:
  create-issue:
    max: 1
jobs:
  security-scan:
    name: Run CodeQL and Grype
    runs-on: ubuntu-latest
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

      - name: Upload security scan reports
        uses: actions/upload-artifact@v7
        with:
          name: security-scan-reports
          path: security-scan-reports
          if-no-files-found: error

---
# security-scan

Run a CodeQL security analysis using the Python codebase and run Grype against the project's dependencies. Create one GitHub issue containing the findings from both tools. Include severity, affected files or packages, evidence, and recommended remediation. If a tool cannot run, report that clearly in the issue.

Read the SARIF files in `security-scan-reports/`. Do not claim that a finding exists unless it is present in one of those reports. Create the issue with a concise summary, separate CodeQL and Grype findings, and remediation guidance. If both reports contain no findings, call `noop` with a message explaining that the scan completed without findings.