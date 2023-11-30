#!/bin/bash

# app.py 파일에서 'app.run(debug=True)' 부분을 'app.run(host='0.0.0.0', debug=True)'로 변경
sed -i.bak "s/app.run(debug=True)/app.run(host='0.0.0.0', debug=True)/g" app.py

# 필요한 포트를 열어줍니다
sudo iptables -I INPUT 1 -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 1 -p tcp --dport 443 -j ACCEPT
sudo iptables -I INPUT 1 -p tcp --dport 5000 -j ACCEPT

# app.py를 백그라운드에서 실행합니다
nohup python3 -u app.py &
