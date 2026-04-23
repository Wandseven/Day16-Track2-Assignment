# Cloud AI Environment Setup - Lab 16 (AWS)

Dự án này hướng dẫn cách thiết lập một môi trường Cloud AI hoàn chỉnh trên AWS sử dụng Terraform (Infrastructure as Code). Dự án bao gồm việc khởi tạo mạng VPC an toàn và triển khai mô hình Machine Learning (LightGBM) trên máy chủ CPU.

## 🏗 Kiến trúc hệ thống
- **VPC & Subnets:** Mạng riêng biệt với Public Subnet (chứa Bastion Host) và Private Subnet (chứa CPU Node).
- **Bastion Host:** Trạm trung chuyển bảo mật để SSH vào các máy chủ nội bộ.
- **CPU Node:** Máy chủ chạy các tác vụ Machine Learning (đã cấu hình cho dòng `t3.micro`).
- **NAT Gateway:** Cho phép máy chủ nội bộ tải dữ liệu từ Internet.
- **Application Load Balancer (ALB):** Điều phối lưu lượng truy cập vào hệ thống.

## 📁 Cấu trúc thư mục (Repo Skeleton)
```text
Day16-Track2-Assignment/
├── terraform/                           # Thư mục cấu hình Terraform (IaC)
│   ├── main.tf                          # Khai báo tài nguyên AWS (VPC, EC2, ALB...)
│   ├── outputs.tf                       # Khai báo các thông tin đầu ra (IP, DNS)
│   ├── providers.tf                     # Cấu hình nhà cung cấp AWS
│   ├── variables.tf                     # Khai báo các biến đầu vào
│   └── user_data.sh                     # Script khởi tạo cho máy chủ (GPU mode)
├── screenshots/                         # Screenshots các kết quả
│   ├── Billing.png                      # Billing
│   ├── EC2.png                          # EC2 instances
│   ├── NATgateway.png                   # NAT gateway
│   └── TerminalBenchmark.png            # Terminal benchmark
├── benchmark.py                         # Script Python chạy thử nghiệm LightGBM
├── report.md                            # Báo cáo kết quả thực hành & lý do dùng CPU
├── benchmark.png                        # Hình ảnh kết quả benchmark
└── README.md                            # Hướng dẫn sử dụng dự án
```


## 🚀 Hướng dẫn triển khai

### 1. Chuẩn bị
- Đã cài đặt [Terraform](https://www.terraform.io/downloads.html).
- Đã cài đặt [AWS CLI](https://aws.amazon.com/cli/) và cấu hình Access Key (`aws configure`).
- Tài khoản Kaggle để tải dataset.

### 2. Khởi tạo hạ tầng
```bash
cd terraform
terraform init
terraform apply
```

### 3. Truy cập và chạy Benchmark
1. **Lấy SSH Key:** File `lab-key` nằm trong thư mục `terraform`.
2. **SSH vào Bastion:** 
   ```bash
   ssh -i lab-key ubuntu@<BASTION_PUBLIC_IP>
   ```
3. **SSH vào CPU Node (từ Bastion):** 
   ```bash
   ssh -i lab-key ec2-user@<CPU_PRIVATE_IP>
   ```
4. **Cài đặt môi trường & Chạy ML:**
   ```bash
   pip3 install lightgbm scikit-learn pandas numpy kaggle
   kaggle datasets download -d mlg-ulb/creditcardfraud --unzip
   python3 benchmark.py
   ```

## 🧹 Dọn dẹp tài nguyên
Sau khi hoàn thành bài lab, chạy lệnh sau để tránh phát sinh chi phí:
```bash
terraform destroy
```

## 📝 Kết quả
Kết quả benchmark được lưu tại file `benchmark_result.json` và tóm tắt trong file `report.md`.
