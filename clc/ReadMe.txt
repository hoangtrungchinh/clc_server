HOW TO DEPLOY CLC_SYSTEM ON UBUNTU/MAC

- Step 0: Download and install docker and docker-compose

- Step 1: Unzip this folder, Open Ternimal, cd to "clc" path and run:
set -a && source .env && set +a ;
docker-compose up ;

- Step 2: After Step 1 completed, Open another terminal and run:
docker exec clc_client_1 python3 /clc_client/manage.py makemigrations ;
docker exec clc_client_1 python3 /clc_client/manage.py migrate ;
docker exec clc_server_1 python3 /clc_server/manage.py makemigrations ;
docker exec clc_server_1 python3 /clc_server/manage.py migrate ;
docker exec clc_server_1 python3 /clc_server/manage.py loaddata cat/fixtures/initial_data.yaml ;

- Step 3: Accesss to http://127.0.0.1:7000/, login with account
username: chinh
pass: 123456789

NOTE:
-Khi tạo mới 1 project, chỉ được chọn Translation Service là My Memory và Open NMT. Hiện tại Service Google translate ko hoạt động do Google mới cập nhật chính sách xài miễn phí.
- Vì có ít dữ liệu, nên việc hiển thị ra câu tương đồng và glossary khá khó, => nên vào mục Config và hạ thấp độ ngưỡng tương đồng.
- Lần sau muốn chạy lại thì chỉ cần vào thư mục clc và chạy lệnh "docker-compose up"