#!/usr/bin/env python3
"""
下载并提取 MaxMind 的 GeoLite2-Country.mmdb 数据库
- 自动读取 MAXMIND_ACCOUNT_ID 和 MAXMIND_LICENSE_KEY 环境变量
- 从 MaxMind 官方地址下载 tar.gz 压缩包
- 解压出 .mmdb 文件，保存到 ./data 目录
- 用于 GitHub Actions 或本地定期更新
"""

import os
import requests
import tarfile

# 读取 MaxMind 账号与 License Key（通过 GitHub Secrets 设置）
account_id = os.getenv("MAXMIND_ACCOUNT_ID")
license_key = os.getenv("MAXMIND_LICENSE_KEY")

# 下载地址（使用官方格式）
url = f"https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country&license_key={license_key}&suffix=tar.gz"

# 路径配置
output_dir = "data"
tar_path = "GeoLite2.tar.gz"

print("开始从 MaxMind 下载 GeoLite2-Country 数据库...")
print(f"下载地址: {url}")

try:
    r = requests.get(url, stream=True)
    r.raise_for_status()
    total_size = int(r.headers.get("Content-Length", 0))
    size_mb = total_size / 1024 / 1024
    print(f"文件大小：{size_mb:.2f} MB")

    with open(tar_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    print("下载完成")
except Exception as e:
    raise SystemExit(f"下载失败: {e}")

# 确保输出目录存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 解压出 .mmdb 文件
try:
    with tarfile.open(tar_path, "r:gz") as tar:
        for member in tar.getmembers():
            if member.name.endswith(".mmdb"):
                member.name = os.path.basename(member.name)
                tar.extract(member, output_dir)
    print(f".mmdb 文件已解压至：{output_dir}/")
except Exception as e:
    raise SystemExit(f"解压失败: {e}")
finally:
    os.remove(tar_path)
    print("临时文件已删除")