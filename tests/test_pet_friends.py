from api import PetFriends
from settings import valid_password, valid_email, invalid_email, invalid_password, invalid_auth_key
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):

    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):

    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name="Торик", animal_type="Такса", age="1", pet_photo='images/images.jpeg'):

    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pets(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():

    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pets(auth_key, 'Барсик', 'Собака', "3", 'images/images.jpeg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Тузик', animal_type='Щенок', age='100'):

    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name

    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_new_pet_no_photo_with_valid_data(name="Игорь", animal_type="Белка", age="6"):

    """Проверяем что можно добавить питомца с корректными данными без фотографии"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца без фотографии
    status, result = pf.add_new_pets_no_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_api_set_photo(pet_photo='images/images.jpeg'):

    """Проверяем возможность добавления фотографии питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Запрашиваем и получаем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берем первого питомца
    pet_id = my_pets['pets'][0]['id']
    # Добавляем фотографию питомцу
    status, result = pf.add_pets_photo(auth_key, pet_id, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200

def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):

    """ Проверяем что запрос api ключа не возвращает статус 200 и в результате не содержится слово key при невалидном email"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    assert 'key' not in result

def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):

    """ Проверяем что запрос api ключа не возвращает статус 200 и в результате не содержится слово key при невалидном пароле"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    assert 'key' not in result

def test_get_all_pets_with_invalid_key(filter=''):

    """ Проверяем что запрос всех питомцев не возвращает список при неправильном ключе .
        Для этого сначала сохраняем в переменную auth_key не верный api ключ. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не возвращается.
        Доступное значение параметра filter - 'my_pets' либо '' """

    # Подставляем не верный api ключ и сохраняем результат
    auth_key = invalid_auth_key
    status, result = pf.get_list_of_pets(auth_key, filter)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    assert 'pets' not in result

def test_add_new_pet_with_invalid_auth_key(name="Барбос", animal_type="Крыса", age="1", pet_photo='images/images.jpeg'):

    """Проверяем что нельзя добавить питомца с корректными данными по неверному api ключу"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Подставляем не верный api ключ и сохраняем результат
    auth_key = invalid_auth_key
    status, result = pf.add_new_pets(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    assert name not in result

def test_successful_delete_self_pet_invalid_auth_key():

    """Проверяем возможность удаления питомца используя не верный api ключ"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pets(auth_key, 'Барсик', 'Собака', "3", 'images/images.jpeg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление используя неверный api ключ
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(invalid_auth_key, pet_id)
    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем что статус ответа неравен 200 и в списке питомцев нет id удалённого питомца
    assert status != 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info_invalid_auth_key(name='Дони', animal_type='змейка', age='16'):

    """Проверяем что невозможность обновления информации о питомце используя неверный api ключ"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст используя неверный api ключ
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(invalid_auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем что статус ответа неравен 200 и имя питомца несоответствует заданному
        assert status != 200
        assert result not in 'name'

    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_new_pet_no_photo_with_invalid_auth_key(name="Стрелка", animal_type="Кот", age="12"):

    """Проверяем что нельзя добавить питомца с корректными данными без фотографии используя неправильный api ключ"""
    # Подставляем не верный api ключ и сохраняем его в переменную auth_key
    auth_key = invalid_auth_key
    # Добавляем питомца
    status, result = pf.add_new_pets_no_photo(auth_key, name, animal_type, age)

    # Проверяем что статус ответа равен 403 и имя питомца несоответствует заданному
    assert status == 403
    assert result not in 'name'
