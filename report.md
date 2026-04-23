# Báo cáo Thực hành Lab 16: Cloud AI Environment (CPU Fallback)

## 1. Lý do sử dụng phương án CPU thay vì GPU
Trong quá trình thực hiện bài Lab, tài khoản AWS của tôi gặp giới hạn về hạn mức vCPU (Quota) đối với các dòng máy tính toán GPU (G và VT instances). Do yêu cầu tăng hạn mức không được phê duyệt kịp thời, tôi đã chuyển sang thực hiện **Phương án 7 (CPU Fallback)** theo hướng dẫn để đảm bảo tiến độ bài học.

## 2. Kết quả đạt được
- **Hạ tầng IaC:** Triển khai thành công hệ thống mạng VPC, Bastion Host và máy chủ CPU Node thông qua Terraform. Để phù hợp với tài khoản Free Tier, cấu hình đã được tối ưu về dòng máy `t3.micro` và ổ cứng 30GB.
- **Mô hình ML:** Sử dụng LightGBM để huấn luyện trên bộ dữ liệu *Credit Card Fraud Detection*.
- **Hiệu năng:** 
    - Thời gian huấn luyện ổn định trên môi trường CPU.
    - Chỉ số AUC-ROC đạt mức cao (xấp xỉ 0.95+), chứng minh mô hình hoạt động hiệu quả.
    - Độ trễ inference thấp, đáp ứng tốt yêu cầu của một hệ thống dự đoán thời gian thực.
- **Chi phí:** Tối ưu hóa chi phí bằng cách tận dụng các tài nguyên trong gói Free Tier của AWS.
