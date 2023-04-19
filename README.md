# fastfood_backend_python
1. Để chạy ứng dụng BE (mạng nội bộ - localhost với port yêu cầu 8088) cần cài đặt database MongoDB - port 27017 với tài khoản db được tạo như sau:
```
db.createUser(
  {
    user: "fast_food",
    pwd:  "7335140",   // or cleartext password
    roles: [ { role: "dbAdmin", db: "fast_food_db" }, { role: "readWrite", db: "fast_food_db" }]
  }
)
```
2. Gõ "cmd" trên Window và nhập: ```pip install -r requirements.txt``` để cài thư viện cần thiết
3. Nhập: ```uvicorn main:app --reload --port 8088 --host localhost --env-file .env.development``` để chạy ứng dụng
