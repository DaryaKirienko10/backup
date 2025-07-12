import requests
import json
from tqdm import tqdm


# Функция для загрузки изображения на Яндекс.Диск
def upload_to_yandex_disk(token, file_name, file_content):
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {
        "Authorization": f"OAuth {token}"
    }
    
    # Создаем папку на Яндекс.Диске
    folder_name = "PYAPI-130"
    requests.put(f"https://cloud-api.yandex.net/v1/disk/resources?path={folder_name}", headers=headers)

    # Получаем ссылку для загрузки
    params = {"path": f"{folder_name}/{file_name}", "overwrite": "true"}
    upload_response = requests.get(upload_url, headers=headers, params=params)
    
    if upload_response.status_code != 200:
        raise Exception("Error obtaining upload URL")
    
    upload_link = upload_response.json().get("href")

    # Загружаем файл по полученной ссылке
    upload_result = requests.put(upload_link, data=file_content)

    if upload_result.status_code not in (201, 200):
        raise Exception("Error uploading file")
    
    return upload_result.status_code


def main():
    token = input("Введите токен с Полигона Яндекс.Диска: ")
    text_for_image = input("Введите текст для картинки: ")
    number_of_images = int(input("Введите количество изображений для загрузки: "))

    uploaded_files_info = []

    # Прогресс-бар
    with tqdm(total=number_of_images, desc='Загрузка изображений', unit='изображение',
              ncols=100, leave=True, dynamic_ncols=True) as overall_progress_bar:
        
        for i in range(number_of_images):
            cat_image_url = f"https://cataas.com/cat/cute/says/{text_for_image}"
            response = requests.get(cat_image_url, stream=True)

            if response.status_code != 200:
                print(f"\nОшибка при получении изображения {i + 1}")
                overall_progress_bar.update(1)
                continue
                
            file_name = f"{text_for_image}_{i + 1}.jpg"
            file_content = response.content

            # Загружаем изображение на Яндекс.Диск
            upload_status = upload_to_yandex_disk(token, file_name, file_content)

            if upload_status in (201, 200):
                uploaded_files_info.append({
                    "file_name": file_name,
                    "file_size": len(file_content)
                })
            
            overall_progress_bar.update(1)

    # Сохраняем информацию в JSON файл
    with open("uploaded_files_info.json", "w") as json_file:
        json.dump(uploaded_files_info, json_file, indent=4)
    
    print("\nВсе изображения загружены на Яндекс.Диск!")

if __name__ == "__main__":
    main()