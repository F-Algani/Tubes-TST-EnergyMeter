# EnergyMeter

Mata Kuliah : II3160 Teknologi Sistem Terintegrasi <br/>
Nama : Farhan Algani Putra <br/>
NIM : 18221108

## Deskripsi Sistem
<p>
EnergyMeter adalah sebuah sistem yang digunakan untuk melakukan *tracking* penggunaan listrik di dalam sebuah ruangan oleh perangkat-perangkat yang terdapat di dalam ruangan tersebut. Sistem ini dibangun untuk memudahkan pengguna dalam mengetahui jumlah penggunaan listrik beserta dengan perkiraan biaya yang harus dibayarkan dari listrik yang telah digunakan.
</p>
<p>
EnergyMeter mendukung penghematan energi yang dapat dilakukan oleh pemiliki rumah karena bisa secara langsung melihat penggunaan listrik yang telah dilakukan. Dengan adanya EnergyMeter, diharapkan pengguna dapat lebih bijak lagi dalam menggunakan listrik untuk keperluan rumah tangga serta bisa menghindari tindakan pemborosan listrik dan biaya.
</p>

## Core Service
Core service yang diimplementasikan pada EnergyMeter saat ini adalah penghitungan jumlah listrik yang digunakan oleh setiap komponen dalam sebuah ruangan dan menghitung estimasi biaya yang dibutuhkan dari listrik yang telah dikonsumsi. Kedepannya, EnergyMeter ingin bisa menyediakan fitur personalisasi golongan konsumen listrik dan juga menyediakan *analytics & insight* terkait penggunaan listrik.

## Requirements
- fastapi==0.104.1
- uvicorn==0.24.0.post1
- pydantic==2.4.2
- package lainnya yang terdapat pada file requirements.txt

## Fitur
- CRUD untuk appliances
- CRUD untuk rooms
- calculate energy

## Cara Menjalankan
1. Jalankan link https://energymeter-18221108.azurewebsites.net/docs
2. Gunakan API Endpoint yang telah disediakan untuk melakukan *service* yang tersedia

## API Endpoint
- **GET /appliances/**
    - Mendapatkan seluruh *appliances* yang terdata pada file JSON
- **PUT /appliances/**
    - Mengubah/memperbaharui data dari sebuah *appliance*
- **POST /appliances/**
    - Menambahkan data *appliance* ke dalam file JSON
- **GET /appliances/{appliance_id}**
    - Mendapatkan data *appliance* berdasarkan *appliance_id*
- **DELETE /appliances/{appliance_id}**
    - Menghapus data *appliance* dari file JSON berdasarkan *appliance_id*
- **GET /rooms/**
    - Mendapatkan seluruh *rooms* yang terdata pada file JSON
- **PUT /rooms/**
    - Mengubah/memperbaharui data dari sebuah *room*
- **POST /rooms/**
    - Menambahkan data *room* ke dalam file JSON
- **GET /rooms/{room_id}**
    - Mendapatkan data *room* berdasarkan *room_id*
- **DELETE /rooms/{room_id}**
    - Menghapus data *room* dari file JSON berdasarkan *room_id*
- **GET /calculate-energy/{room_id}**
    - Menghitung estimasi biaya yang dibutuhkan untuk sebuah *room* berdasarkan *room_id*
- **GET /**
    - *Landing page*

### Credits
Frontend Page Reference:
- GitHub Repository = https://github.com/salimi2991/signin-singup.git
- Youtube Video = https://youtu.be/lcZTuM-50Pc?si=mvw4a9UFeYdRh9NA