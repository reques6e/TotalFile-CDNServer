# TotalFile-CDNServerLite

## Установка
Для начала требуется запустить файл ```install.bash``` и следовать инструкции, после этого CDN уже будет работать.

## Загрузка файлов на сервер

Для загрузки файлов требуется отправить POST запрос на ```/upload``` с файлом.
```python
import requests

def upload_file(file_path, upload_url):
    with open(file_path, 'rb') as file:
        files = {'file': file}
        
        response = requests.post(upload_url, files=files)
        if response.status_code == 200:
            print(response.text)
        else:
            print(f"Failed to upload file {response.text}")

if __name__ == "__main__":
    file_path = "test.txt"
    
    upload_url = "http://127.0.0.1:5001/upload"  
    
    upload_file(file_path, upload_url)
```


Script by <a href='https://github.com/reques6e' style='display: block; text-align: center;'>Requeste Project<img src='https://github.com/reques6e/reques6e/blob/main/assets/images.png?v=1' alt='Мой баннер' width='20' height='20' style='float: right;'></a>
