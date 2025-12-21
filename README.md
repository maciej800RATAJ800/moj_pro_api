## Installation & Run (WSL / Linux)

```bash
git clone https://github.com/maciej80RATAJ800/moj_pro_api.git
cd moj_pro_api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.app:app --reload

# test push
