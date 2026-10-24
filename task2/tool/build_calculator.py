"""Embeds data.json into the template -> credit_calculator.html (single self-contained file)."""
import json, os
here = os.path.dirname(os.path.abspath(__file__))
data = open(os.path.join(here, "data.json")).read()
html = open(os.path.join(here, "calculator_template.html"), encoding="utf-8").read().replace("__DATA__", data)
open(os.path.join(here, "credit_calculator.html"), "w", encoding="utf-8").write(html)
print("built", len(html)//1024, "KB")
