# HIBP PDF Generator

This project queries the [Have I Been Pwned](https://haveibeenpwned.com/) API for a list of email addresses and generates a structured PDF report showing which emails were found in public data breaches.

It is designed to assist individuals, IT teams, and small organizations with monitoring exposure without relying on online tools.

## Features

- Queries the HIBP API using your API key
- Generates a clean, professional PDF report
- Differentiates between breached and safe emails
- Includes breach names, dates, and leaked data types
- Optional Unicode font support (for full character rendering)

## Requirements

- Python 3.7 or higher
- A valid [Have I Been Pwned API key](https://haveibeenpwned.com/API/Key)

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/YOUR_USERNAME/HIBP-pdf-generator.git
cd HIBP-pdf-generator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

## Configuration

### 1. Set your HIBP API key

Export the API key as an environment variable:

```bash
export HIBP_API_KEY="your_hibp_api_key"
```

Alternatively, you can edit the script to hardcode it, though this is not recommended for security reasons.

### 2. Configure target emails

Edit `config.json` with the emails you want to scan:

```json
{
  "emails": [
    "user1@example.com",
    "user2@example.com"
  ]
}
```

You may also include placeholders for usernames, IPs, domains, or passwords for future functionality, but they are not used in this version.

## Usage

Run the script:

```bash
python hibp_pdf_generator.py
```

Output:

* A file named `darkweb_monitoring_report.pdf` will be generated in the current directory.
* Breached emails and their breach details will be listed and categorized separately from safe ones.

## File Structure

| File                    | Purpose                                   |
| ----------------------- | ----------------------------------------- |
| `hibp_pdf_generator.py` | Main script to generate the PDF report    |
| `config.json.sample`    | Example configuration file                |
| `requirements.txt`      | Python dependencies                       |
| `LICENSE`               | License information (MIT)                 |
| `README.md`             | Project documentation                     |
| `DejaVuSans.ttf`        | Optional font file for Unicode PDF output |

## Sample Output

The generated PDF includes:

* Title page with timestamp
* Lists of breached and safe emails
* Per-email breach breakdown with dates and data types
* Summary of all breaches found (name, date, fields exposed)

## Notes

* The HIBP API enforces rate limits. The script includes a `time.sleep(1.6)` delay between requests to avoid hitting the limit.
* If `DejaVuSans.ttf` is placed in the script directory, it will be used for better Unicode compatibility in the PDF.
* The `user-agent` is set as `"DarkWebMonitor/1.0"` in API requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
