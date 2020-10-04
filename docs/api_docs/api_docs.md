- [Документация API для сайта Art For Introvert](#sec-1)
  - [Регистрация/авторизация](#sec-1-1)

# Документация API для сайта Art For Introvert<a id="sec-1"></a>

## Регистрация/авторизация<a id="sec-1-1"></a>

Регистрация нового пользователя:

       POST /api/users/
       {
        "data": {
            "type": "User",
            "attributes": {
                "email": <user_email>,
                "password": <user_password>
            }
        }
        }
       Пример ответа:
       {
        "data": {
            "type": "User",
            "id": <user_id>,
            "attributes": {
                "email": <user_email>,
                "userpic": null,
                "name": "",
                "birthdate": null
            },
            "links": {
                "self": "https://afi-backend.herokuapp.com/api/users/<user_email>/"
            }
        }
    }
