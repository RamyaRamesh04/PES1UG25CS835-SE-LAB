\# Lab 5: Static Code Analysis — Issues Log



\*\*Project:\*\* Public Transit Fare Calculator  

\*\*Source file:\*\* `fare\_calculator.py`



| Issue | Type | Line(s) | Description | Fix Approach |

|---|---|---|---|---|

| Unverified SSH host key | Security — High | 80 | Automatically trusts unknown SSH hosts. | Use verified host keys and reject unknown hosts. |

| Remote command construction | Security — Medium | 82 | Builds a remote command by concatenating a filename. | Validate the filename and avoid unsafe command construction. |

| MD5 checksum | Security — Medium | 60 | Uses an insecure hash algorithm. | Replace MD5 with SHA-256 if compatible with the checksum requirements. |

| Unsafe XML parsing | Security — Medium | 75 | Parses XML using `xml.sax.parseString`. | Use the corresponding `defusedxml` SAX parser. |

| XML SAX import | Security — Low | 2 | Imports the parser flagged by Bandit. | Replace the import with the safe parser after updating the parsing code. |

| Mutable default argument | Code quality | 46 | `categories=\[]` uses a mutable default. | Use `None` and initialize a fresh list inside the function. |

| Daily cap implementation | Functional bug | 35–40 | The cap check does not change the accumulated total. | Apply the daily cap to the running or final total according to the intended fare rules. |

| Naming and documentation | Maintainability | Multiple | Several functions use non-snake\_case names and lack docstrings. | Use consistent naming and add descriptive docstrings. |

| Formatting issues | Style | Multiple | Unused imports, lambda assignment, blank-line and line-length violations. | Apply the reported Flake8 corrections. |



