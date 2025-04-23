# ibcb

Instagram Business Chat Bot (IBCB)

## Overview
Bu repo, Instagram Business hesabı üzerinden gelen mesajları alıp yanıtlayan bir chatbot uygulaması için gerekli dosya ve yapıların bulunduğu ana klasördür.

## Installation
1. GitHub’dan klonlayın: `git clone https://github.com/Rastiel/ibcb.git`
2. Proje dizinine girin: `cd ibcb`
3. Çevresel değişkenleri ayarlayın (örnek `.env.example` üzerinden)
4. Docker Compose ile ayağa kaldırın: `docker-compose up -d`

## Structure
* `nginx/`: Reverse proxy konfigürasyonları
* `app/`: Bot iş mantığı ve API
* `webhook/`: Instagram webhook endpoint’i
