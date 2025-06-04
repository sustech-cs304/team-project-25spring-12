pip install -r requirements.txt
flake8 mjc > flake8_report.txt
liazrd mjc > liazrd_report.txt
sudo docker build -t mjc .
