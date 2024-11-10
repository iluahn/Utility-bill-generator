### Скрипт для формирования чеков за коммунальные услуги

Данный скрипт формирует чек за месяц, где приводится долг из ЛК Кабинет-жителя.рф, Петроэлектросбыта, а также долг за Интернет.

Чек имеет следующий формат (по категориям) и записывается в файл:
```
1234.56 ку
123.45 электричество
400 интернет

Итого 1758.01
```

Для получения значений долгов по категориям используются HTTP-запросы в API Кабинет-жителя.рф и Петроэлектросбыта (долг за Интернет на данный момент является фиксированным, так как за него было оплачено на год вперед).  
Для получения об endpoint'ах API использовался функционал браузера (Просмотреть код -> Network -> Fetch/XHR). Для отладки использовался Postman.


#### Общая логика получения долга:
- POST-запрос на логин и получение токена(-ов);
- GET-запрос(ы) на получение значения долга;
- POST/DELETE-запрос на логаут и удаление полученного(-ых) токена(-ов).

Токен(ы) и сумма долга устанавливаются как атрибуты класса в конструкторе.  
При создании объекта пользователя Кабинет-жителя.рф необходимо передать в конструктор логин и юзернейм.  
При создании объекта пользователя Петроэлектросбыт необходимо также передать логин-тайп ("PHONE" либо "EMAIL") первым аргументом. Эти переменные передаются с помощью dotenv через .env-файл.

В случае, если залогиниться не удается, атрибут с суммой долга устанавливается как None.  
При этом в консоль будет выведен текст ответа от сервера (с информацией о том, что логин и пароль неверные), а в файл будет записано "получена не вся информация".

В таком случае содержимое файла выглядит примерно так:
```
None ку
None электричество
400 интернет

Info: получена не вся информация, проверьте вывод консоли
```
