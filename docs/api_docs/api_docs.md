- [Документация API для сайта Art For Introvert](#sec-1)
  - [Регистрация/авторизация](#sec-1-1)
    - [Регистрация нового пользователя:](#sec-1-1-1)
    - [Получение access токена](#sec-1-1-2)
    - [Обновление access токенa](#sec-1-1-3)
  - [Покупка билета/видео-лекции](#sec-1-2)
    - [Добавление в корзину](#sec-1-2-1)
    - [Получение текущей корзины](#sec-1-2-2)
    - [Покупка корзины](#sec-1-2-3)
  - [Изменение данных пользователя](#sec-1-3)
    - [Изменение полей профиля](#sec-1-3-1)
    - [Изменение юзерпика](#sec-1-3-2)
  - [Фильтрация, сортировка и поиск по API](#sec-1-4)
    - [Сортировка](#sec-1-4-1)
    - [Фильтрация](#sec-1-4-2)
    - [Поиск](#sec-1-4-3)
  - [Добавление related объектов (include)](#sec-1-5)
    - [Параметр include](#sec-1-5-1)
  - [Список ендпойнтов  *api*](#sec-1-6)

# Документация API для сайта Art For Introvert<a id="sec-1"></a>

Для всех запросов используется формат "application/vnd.api+json"

## Регистрация/авторизация<a id="sec-1-1"></a>

### Регистрация нового пользователя:<a id="sec-1-1-1"></a>

`POST /api/users/`

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

### Получение access токена<a id="sec-1-1-2"></a>

После регистрации пользователя нужно получить access token (JWT <https://jwt.io/>) послав запрос `POST /api/auth-token/`

    {
          "data": {
              "type": "MyTokenObtainPairView",
              "attributes": {
                  "email": "<user_email>",
                  "password": "<user_password"
              }
          }
      }

Пример ответа:

      {
        "data": {
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1OTMyMTQxMCwianRpIjoiMzVjZDQ1NzNjN2E0NDA3MTg5OWI0MDY5Y2FjZDYzNzkiLCJ1c2VyX2VtYWlsIjoiYXNkZkB5YW5kZXgucnUifQ.ONxmCsiy3PawjMdYOwd2DCCvh8uu8RHdsY_u5ftActM",
            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA1MjQxNDEwLCJqdGkiOiJhOGU5YzczNjY2ZWE0ZDAyYTljYTA5YWM4YTg3ODgzMyIsInVzZXJfZW1haWwiOiJhc2RmQHlhbmRleC5ydSJ9.XfQVuISFkBZdmK6_T5sI1pJ61DkiTcxdyMPAgTee6Ak"
        }
    }

Время жизни токена конфигурируется через переменные окружения на <https://dashboard.heroku.com/apps/afi-backend/settings> В данный момент access токен живет 5 минут, refresh &#x2013; 1825 дней Для дальнейшей авторизации нужно при каждом запросе посылать в заголовке refresh токен:

    'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjAxNTYyNzM4LCJqdGkiOiIzYTYwYTU2ZjAxOTQ0YjRkOTM4OGYwOGY0ZjkzYTVjNiIsInVzZXJfZW1haWwiOiJka29sMjAwMEB5YW5kZXgucnUifQ.Zf-x3Pq1A15uc83nl5ZxmHLpZv1OA6xDFmQxeJpBme4'

### Обновление access токенa<a id="sec-1-1-3"></a>

После истечения времени жизни access токена нужно получить новый, используя refresh token `POST /api/auth-token/refresh/`

       {
        "data": {
            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA1NDMxNDkxLCJqdGkiOiIzOWUyMGEyMjA4ZWI0OWUxOGVlMWI0MTI4Mzg3ZTZjYiIsInVzZXJfZW1haWwiOiJhc2RmQHlhbmRleC5ydSJ9.pd6OuXtVXEtjvvv9ASywQ6JZjgF_5Da1stTdvOtln-U"
        }
    }

## Покупка билета/видео-лекции<a id="sec-1-2"></a>

### Добавление в корзину<a id="sec-1-2-1"></a>

Для покупки чего-либо нужно добавить этот объект в корзину, если корзины не было, она создастся, либо объект добавится в последнюю существующую корзину. В данный момент можно отправить параметры

-   "videolecture"
-   "ticket"

`POST /api/cart/add-to-cart/`

    {
        "data": {
            "type": "OrderItem",
            "attributes": {
                "item_type": "videolecture",
                "object_id": 1
            }
        }
    }

Пример ответа:

    {
        "data": {
            "type": "OrderItem",
            "id": "6",
            "attributes": {
                "is_paid": false,
                "created_at": "2020-10-01T20:18:27.661918+03:00",
                "total": null
            },
            "relationships": {
                "order_items": {
                    "meta": {
                        "count": 2
                    },
                    "data": [
                        {
                            "type": "OrderItem",
                            "id": "11"
                        },
                        {
                            "type": "OrderItem",
                            "id": "12"
                        }
                    ]
                }
            }
        }
    }

### Получение текущей корзины<a id="sec-1-2-2"></a>

Товары в текущей корзине можно посмотреть отправив `GET /api/cart/last-cart/` Пример ответа:

        {
        "data": {
            "type": "Cart",
            "id": "6",
            "attributes": {
                "is_paid": false,
                "created_at": "2020-10-01T20:18:27.661918+03:00",
                "total": null
            },
            "relationships": {
                "order_items": {
                    "meta": {
                        "count": 2
                    },
                    "data": [
                        {
                            "type": "OrderItem",
                            "id": "11"
                        },
                        {
                            "type": "OrderItem",
                            "id": "12"
                        }
                    ]
                }
            }
        }
    }

### Покупка корзины<a id="sec-1-2-3"></a>

Далее для покупки, используя id корзины (6, в примере выше), нужно отправить запрос на оплату корзины: параметр payment<sub>type</sub><sub>value</sub> это идентификатор платежного провайдера, сейчас подключена только Яндекс-касса, id 0, в будущем добавится еще несколько, id можно посмотреть в админке Django `POST /api/payments/`

    {
                "data": {
                    "type": "PaymentCreateView",
                    "attributes": {
                        "payment_type_value": 0,
                        "amount": 100,
                        "currency": "RUB",
                        "cart_id": 6
                    }
                }
            }

Вернется ссылка на платежную форму, которую нужно будет показать пользователю для оплаты

    {
        "data": {
            "payment_url": "https://money.yandex.ru/api-pages/v2/payment-confirm/epl?orderId=270c1d0a-000f-5000-9000-1441f6311382"
        }
    }

Для яндекс кассы тестовая карт 5555 5555 5555 4444, срок действия любой в будушем, cvv любой

после успешной оплаты пользователем приобретенные айтемы появятся в массиве `purchased_items` пользователя `GET /api/users/user@mail.com`

    {
        "data": {
            "type": "User",
            "id": "1",
            "attributes": {
                "email": "user@mail.com",
                "userpic": null,
                "name": "Denis Dionisov",
                "birthdate": "2021-09-11",
                "purchased_items": {
                    "video_lectures": [],
                    "tickets": []
                }
            },
            "links": {
                "self": "http://127.0.0.1:8000/api/users/user@mail.com/"
            }
        }
    }

## Изменение данных пользователя<a id="sec-1-3"></a>

### Изменение полей профиля<a id="sec-1-3-1"></a>

Для того, чтобы поменять данные пользователя, нужно отправить запрос `PUT /api/users/user@mail.com/`

    {
        "data": {
            "type": "User",
            "id": "asdf@yandex.ru",
            "attributes": {
                "birthdate": "2010-10-10",
                "email": "asdf@yandex.ru"
            }
        }

Поле email обязательно, остальные не обязательны. В поле id должен стоять нынешний email пользователя В случае смены email, токен перестанет действовать, так как в нем содержится старый email, нужно выпустить новый.

### Изменение юзерпика<a id="sec-1-3-2"></a>

Чтобы поменять юзерпик, нужно послать запрос form-data: `PUT /api/users/asdf@yandex.ru`

Пример запроса:

curl:

    curl --location --request PUT 'http://127.0.0.1:8000/api/users/asdf@yandex.ru/upload-userpic/' \
    --header 'Content-Type: application/vnd.api+json' \
    --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA1NDM0NjA3LCJqdGkiOiJkNDZkNzkzNjBkNWU0N2Q3YmZmZTU2YjBiNjU0ZDkyMCIsInVzZXJfZW1haWwiOiJhc2RmQHlhbmRleC5ydSJ9.S1o8Czhv53jD9LcmP5Y6FlBEHEVhl6QwBLlto3E4Tas' \
    --form 'userpic=@/Users/dkol/Desktop/Screenshot 2020-10-01 at 18.56.41.png'

JS:

    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/vnd.api+json");
    myHeaders.append("Authorization", "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA1NDM0NjA3LCJqdGkiOiJkNDZkNzkzNjBkNWU0N2Q3YmZmZTU2YjBiNjU0ZDkyMCIsInVzZXJfZW1haWwiOiJhc2RmQHlhbmRleC5ydSJ9.S1o8Czhv53jD9LcmP5Y6FlBEHEVhl6QwBLlto3E4Tas");
    
    var formdata = new FormData();
    formdata.append("userpic", fileInput.files[0], "Screenshot 2020-10-01 at 18.56.41.png");
    
    var requestOptions = {
      method: 'PUT',
      headers: myHeaders,
      body: formdata,
      redirect: 'follow'
    };
    
    fetch("http://127.0.0.1:8000/api/users/asdf@yandex.ru/upload-userpic/", requestOptions)
      .then(response => response.text())
      .then(result => console.log(result))
      .catch(error => console.log('error', error));curl --location --request PUT 'http://127.0.0.1:8000/api/users/asdf@yandex.ru/upload-userpic/' \
    --header 'Content-Type: application/vnd.api+json' \
    --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjA1NDM0NjA3LCJqdGkiOiJkNDZkNzkzNjBkNWU0N2Q3YmZmZTU2YjBiNjU0ZDkyMCIsInVzZXJfZW1haWwiOiJhc2RmQHlhbmRleC5ydSJ9.S1o8Czhv53jD9LcmP5Y6FlBEHEVhl6QwBLlto3E4Tas' \
    --form 'userpic=@/Users/dkol/Desktop/Screenshot 2020-10-01 at 18.56.41.png'

## Фильтрация, сортировка и поиск по API<a id="sec-1-4"></a>

### Сортировка<a id="sec-1-4-1"></a>

Для сортировки используется параметр `?sort` ~GET *api/users*?sort=email

       {
        "links": {
            "first": "http://127.0.0.1:8000/api/users/?page%5Bnumber%5D=1&sort=email",
            "last": "http://127.0.0.1:8000/api/users/?page%5Bnumber%5D=4&sort=email",
            "next": "http://127.0.0.1:8000/api/users/?page%5Bnumber%5D=2&sort=email",
            "prev": null
        },
        "data": [
            {
                "type": "User",
                "id": "20",
                "attributes": {
                    "email": "angela52@hotmail.com",
                    "userpic": null,
                    "name": "Ethan Ellis",
                    "birthdate": null,
                    "purchased_items": {
                        "video_lectures": [],
                        "tickets": []
                    }
                },
                "links": {
                    "self": "http://127.0.0.1:8000/api/users/angela52@hotmail.com/"
                }
            },
            {
                "type": "User",
                "id": "1",
                "attributes": {
                    "email": "asdf@yandex.ru",
                    "userpic": "http://127.0.0.1:8000/media/user_userpics/Screenshot_2020-10-01_at_18.56.41.png",
                    "name": "Denis Dionisov",
                    "birthdate": "2010-11-10",
                    "purchased_items": {
                        "video_lectures": [],
                        "tickets": []
                    }
                },
                "links": {
                    "self": "http://127.0.0.1:8000/api/users/asdf@yandex.ru/"
                }
            },
            {
                "type": "User",
                "id": "23",
                "attributes": {
                    "email": "ashleyhoward@gmail.com",
                    "userpic": null,
                    "name": "Tammy Rowland",
                    "birthdate": null,
                    "purchased_items": {
                        "video_lectures": [],
                        "tickets": []
                    }
                },
                "links": {
                    "self": "http://127.0.0.1:8000/api/users/ashleyhoward@gmail.com/"
                }
            },
            {
                "type": "User",
                "id": "19",
                "attributes": {
                    "email": "benjamin53@montoya-lucas.info",
                    "userpic": null,
                    "name": "Christine Paul",
                    "birthdate": null,
                    "purchased_items": {
                        "video_lectures": [],
                        "tickets": []
                    }
                },
                "links": {
                    "self": "http://127.0.0.1:8000/api/users/benjamin53@montoya-lucas.info/"
                }
            },
            {
                "type": "User",
                "id": "22",
                "attributes": {
                    "email": "brittany89@berg-taylor.com",
                    "userpic": null,
                    "name": "Michael Stevenson",
                    "birthdate": null,
                    "purchased_items": {
                        "video_lectures": [],
                        "tickets": []
                    }
                },
                "links": {
                    "self": "http://127.0.0.1:8000/api/users/brittany89@berg-taylor.com/"
                }
            },
            {
                "type": "User",
                "id": "9",
                "attributes": {
                    "email": "carrolllydia@gmail.com",
                    "userpic": null,
                    "name": "David Lopez",
                    "birthdate": null,
                    "purchased_items": {
                        "video_lectures": [],
                        "tickets": []
                    }
                },
                "links": {
                    "self": "http://127.0.0.1:8000/api/users/carrolllydia@gmail.com/"
                }
            },
            {
                "type": "User",
                "id": "26",
                "attributes": {
                    "email": "chadunderwood@tran.com",
                    "userpic": null,
                    "name": "Melanie Cohen",
                    "birthdate": null,
                    "purchased_items": {
                        "video_lectures": [],
                        "tickets": []
                    }
                },
                "links": {
                    "self": "http://127.0.0.1:8000/api/users/chadunderwood@tran.com/"
                }
            },
            {
                "type": "User",
                "id": "12",
                "attributes": {
                    "email": "cindypitts@yahoo.com",
                    "userpic": null,
                    "name": "Gregory Parker",
                    "birthdate": null,
                    "purchased_items": {
                        "video_lectures": [],
                        "tickets": []
                    }
                },
                "links": {
                    "self": "http://127.0.0.1:8000/api/users/cindypitts@yahoo.com/"
                }
            },
            {
                "type": "User",
                "id": "18",
                "attributes": {
                    "email": "cynthia08@king.com",
                    "userpic": null,
                    "name": "Michael Vaughan",
                    "birthdate": null,
                    "purchased_items": {
                        "video_lectures": [],
                        "tickets": []
                    }
                },
                "links": {
                    "self": "http://127.0.0.1:8000/api/users/cynthia08@king.com/"
                }
            },
            {
                "type": "User",
                "id": "2",
                "attributes": {
                    "email": "denis.kolosov@gmail.com",
                    "userpic": null,
                    "name": "",
                    "birthdate": null,
                    "purchased_items": {
                        "video_lectures": [],
                        "tickets": []
                    }
                },
                "links": {
                    "self": "http://127.0.0.1:8000/api/users/denis.kolosov@gmail.com/"
                }
            }
        ],
        "meta": {
            "pagination": {
                "page": 1,
                "pages": 4,
                "count": 32
            }
        }
    }

### Фильтрация<a id="sec-1-4-2"></a>

Для фильтра по полям нужно добавить параметр ?filter[/поле<sub>фильтрации</sub>/] `GET /api/offline-lectures/?filter[lecture_date]=1976-08-11T07:03:48`

       {
        "links": {
            "first": "http://127.0.0.1:8000/api/offline-lectures/?filter%5Blecture_date%5D=1976-08-11T07%3A03%3A48&page%5Bnumber%5D=1",
            "last": "http://127.0.0.1:8000/api/offline-lectures/?filter%5Blecture_date%5D=1976-08-11T07%3A03%3A48&page%5Bnumber%5D=1",
            "next": null,
            "prev": null
        },
        "data": [
            {
                "type": "OfflineLecture",
                "id": "18",
                "attributes": {
                    "name": "Offline lecture 0",
                    "address": "",
                    "picture": "http://127.0.0.1:8000/media/lecture_pictures/1573646089377-9wpu20ce.jpeg",
                    "lecture_date": "1976-08-11T07:03:48+03:00",
                    "lecture_date_ts": 208573428,
                    "capacity": null,
                    "description": "",
                    "tickets_sold": 0,
                    "lecture_summary_file": null,
                    "price": null,
                    "price_currency": "RUB"
                },
                "relationships": {
                    "lecturer": {
                        "data": {
                            "type": "Lecturer",
                            "id": "19"
                        }
                    },
                    "category": {
                        "data": {
                            "type": "Category",
                            "id": "19"
                        }
                    }
                }
            }
        ],
        "meta": {
            "pagination": {
                "page": 1,
                "pages": 1,
                "count": 1
            }
        }
    }

Предыдущий пример вернет лекцию с точным значением времени. Удобно возвращать объекты, меньше или или больше заданного параметра, для этого можно использовать параметры `gt` и `lt` . Также параметры можно комбинировать(не только filter, но и остальные) `GET /api/offline-lectures/?filter[lecture_date.gt]=1976-08-11T07:03:48&filter[lecture_date.lt]=2020-10-10T10:10:10`

      {
        "links": {
            "first": "http://127.0.0.1:8000/api/offline-lectures/?filter%5Blecture_date.gt%5D=1976-08-11T07%3A03%3A48&filter%5Blecture_date.lt%5D=2020-10-10T10%3A10%3A10&page%5Bnumber%5D=1",
            "last": "http://127.0.0.1:8000/api/offline-lectures/?filter%5Blecture_date.gt%5D=1976-08-11T07%3A03%3A48&filter%5Blecture_date.lt%5D=2020-10-10T10%3A10%3A10&page%5Bnumber%5D=1",
            "next": null,
            "prev": null
        },
        "data": [
            {
                "type": "OfflineLecture",
                "id": "19",
                "attributes": {
                    "name": "Offline lecture 1",
                    "address": "",
                    "picture": "http://127.0.0.1:8000/media/lecture_pictures/1573646089377-9wpu20ce.jpeg",
                    "lecture_date": "1996-09-11T09:06:21+04:00",
                    "lecture_date_ts": 842407581,
                    "capacity": null,
                    "description": "",
                    "tickets_sold": 0,
                    "lecture_summary_file": null,
                    "price": null,
                    "price_currency": "RUB"
                },
                "relationships": {
                    "lecturer": {
                        "data": {
                            "type": "Lecturer",
                            "id": "20"
                        }
                    },
                    "category": {
                        "data": {
                            "type": "Category",
                            "id": "20"
                        }
                    }
                }
            },
            {
                "type": "OfflineLecture",
                "id": "20",
                "attributes": {
                    "name": "Offline lecture 0",
                    "address": "",
                    "picture": "http://127.0.0.1:8000/media/lecture_pictures/1573646089377-9wpu20ce.jpeg",
                    "lecture_date": "1992-04-07T01:51:02+04:00",
                    "lecture_date_ts": 702586262,
                    "capacity": null,
                    "description": "",
                    "tickets_sold": 0,
                    "lecture_summary_file": null,
                    "price": "1000.00",
                    "price_currency": "RUB"
                },
                "relationships": {
                    "lecturer": {
                        "data": {
                            "type": "Lecturer",
                            "id": "21"
                        }
                    },
                    "category": {
                        "data": {
                            "type": "Category",
                            "id": "21"
                        }
                    }
                }
            },
            {
                "type": "OfflineLecture",
                "id": "24",
                "attributes": {
                    "name": "Offline lecture 1",
                    "address": "",
                    "picture": "http://127.0.0.1:8000/media/lecture_pictures/1573646089377-9wpu20ce.jpeg",
                    "lecture_date": "2013-05-25T22:16:49+04:00",
                    "lecture_date_ts": 1369491409,
                    "capacity": null,
                    "description": "",
                    "tickets_sold": 0,
                    "lecture_summary_file": null,
                    "price": "1000.00",
                    "price_currency": "RUB"
                },
                "relationships": {
                    "lecturer": {
                        "data": {
                            "type": "Lecturer",
                            "id": "25"
                        }
                    },
                    "category": {
                        "data": {
                            "type": "Category",
                            "id": "25"
                        }
                    }
                }
            },
            {
                "type": "OfflineLecture",
                "id": "25",
                "attributes": {
                    "name": "Offline lecture 2",
                    "address": "",
                    "picture": "http://127.0.0.1:8000/media/lecture_pictures/1573646089377-9wpu20ce.jpeg",
                    "lecture_date": "1990-07-21T01:50:40+04:00",
                    "lecture_date_ts": 648499840,
                    "capacity": null,
                    "description": "",
                    "tickets_sold": 0,
                    "lecture_summary_file": null,
                    "price": "1000.00",
                    "price_currency": "RUB"
                },
                "relationships": {
                    "lecturer": {
                        "data": {
                            "type": "Lecturer",
                            "id": "26"
                        }
                    },
                    "category": {
                        "data": {
                            "type": "Category",
                            "id": "26"
                        }
                    }
                }
            }
        ],
        "meta": {
            "pagination": {
                "page": 1,
                "pages": 1,
                "count": 4
            }
        }
    }

### Поиск<a id="sec-1-4-3"></a>

Для поиска по содержанию полей используется фильтр search `GET /api/offline-lectures/?filter[search]=Offline`

      {
        "links": {
            "first": "http://127.0.0.1:8000/api/offline-lectures/?filter%5Bsearch%5D=Offline&page%5Bnumber%5D=1",
            "last": "http://127.0.0.1:8000/api/offline-lectures/?filter%5Bsearch%5D=Offline&page%5Bnumber%5D=1",
            "next": null,
            "prev": null
        },
        "data": [
            {
                "type": "OfflineLecture",
                "id": "18",
                "attributes": {
                    "name": "Offline lecture 0",
                    "address": "",
                    "picture": "http://127.0.0.1:8000/media/lecture_pictures/1573646089377-9wpu20ce.jpeg",
                    "lecture_date": "1976-08-11T07:03:48+03:00",
                    "lecture_date_ts": 208573428,
                    "capacity": null,
                    "description": "",
                    "tickets_sold": 0,
                    "lecture_summary_file": null,
                    "price": null,
                    "price_currency": "RUB"
                },
                "relationships": {
                    "lecturer": {
                        "data": {
                            "type": "Lecturer",
                            "id": "19"
                        }
                    },
                    "category": {
                        "data": {
                            "type": "Category",
                            "id": "19"
                        }
                    }
                }
            },
            {
                "type": "OfflineLecture",
                "id": "19",
                "attributes": {
                    "name": "Offline lecture 1",
                    "address": "",
                    "picture": "http://127.0.0.1:8000/media/lecture_pictures/1573646089377-9wpu20ce.jpeg",
                    "lecture_date": "1996-09-11T09:06:21+04:00",
                    "lecture_date_ts": 842407581,
                    "capacity": null,
                    "description": "",
                    "tickets_sold": 0,
                    "lecture_summary_file": null,
                    "price": null,
                    "price_currency": "RUB"
                },
                "relationships": {
                    "lecturer": {
                        "data": {
                            "type": "Lecturer",
                            "id": "20"
                        }
                    },
                    "category": {
                        "data": {
                            "type": "Category",
                            "id": "20"
                        }
                    }
                }
            },
            {
                "type": "OfflineLecture",
                "id": "20",
                "attributes": {
                    "name": "Offline lecture 0",
                    "address": "",
                    "picture": "http://127.0.0.1:8000/media/lecture_pictures/1573646089377-9wpu20ce.jpeg",
                    "lecture_date": "1992-04-07T01:51:02+04:00",
                    "lecture_date_ts": 702586262,
                    "capacity": null,
                    "description": "",
                    "tickets_sold": 0,
                    "lecture_summary_file": null,
                    "price": "1000.00",
                    "price_currency": "RUB"
                },
                "relationships": {
                    "lecturer": {
                        "data": {
                            "type": "Lecturer",
                            "id": "21"
                        }
                    },
                    "category": {
                        "data": {
                            "type": "Category",
                            "id": "21"
                        }
                    }
                }
            },
            {
                "type": "OfflineLecture",
                "id": "24",
                "attributes": {
                    "name": "Offline lecture 1",
                    "address": "",
                    "picture": "http://127.0.0.1:8000/media/lecture_pictures/1573646089377-9wpu20ce.jpeg",
                    "lecture_date": "2013-05-25T22:16:49+04:00",
                    "lecture_date_ts": 1369491409,
                    "capacity": null,
                    "description": "",
                    "tickets_sold": 0,
                    "lecture_summary_file": null,
                    "price": "1000.00",
                    "price_currency": "RUB"
                },
                "relationships": {
                    "lecturer": {
                        "data": {
                            "type": "Lecturer",
                            "id": "25"
                        }
                    },
                    "category": {
                        "data": {
                            "type": "Category",
                            "id": "25"
                        }
                    }
                }
            },
            {
                "type": "OfflineLecture",
                "id": "25",
                "attributes": {
                    "name": "Offline lecture 2",
                    "address": "",
                    "picture": "http://127.0.0.1:8000/media/lecture_pictures/1573646089377-9wpu20ce.jpeg",
                    "lecture_date": "1990-07-21T01:50:40+04:00",
                    "lecture_date_ts": 648499840,
                    "capacity": null,
                    "description": "",
                    "tickets_sold": 0,
                    "lecture_summary_file": null,
                    "price": "1000.00",
                    "price_currency": "RUB"
                },
                "relationships": {
                    "lecturer": {
                        "data": {
                            "type": "Lecturer",
                            "id": "26"
                        }
                    },
                    "category": {
                        "data": {
                            "type": "Category",
                            "id": "26"
                        }
                    }
                }
            }
        ],
        "meta": {
            "pagination": {
                "page": 1,
                "pages": 1,
                "count": 5
            }
        }
    }

## Добавление related объектов (include)<a id="sec-1-5"></a>

### Параметр include<a id="sec-1-5-1"></a>

Для добавления относящихся объектов используется параметр `?include` Несколько объектов можно перечислять через запятую

Объекты будут находится в поле `"included"` `GET /api/offline-lectures/?include=category,lecturer`

       {
        "links": {
            "first": "http://127.0.0.1:8000/api/offline-lectures/?include=category%2Clecturer&page%5Bnumber%5D=1",
            "last": "http://127.0.0.1:8000/api/offline-lectures/?include=category%2Clecturer&page%5Bnumber%5D=1",
            "next": null,
            "prev": null
        },
        "data": [
            {
                "type": "OfflineLecture",
                "id": "18",
                "attributes": {
                    "name": "Offline lecture 0",
                    "address": "",
                    "picture": "http://127.0.0.1:8000/media/lecture_pictures/1573646089377-9wpu20ce.jpeg",
                    "lecture_date": "1976-08-11T07:03:48+03:00",
                    "lecture_date_ts": 208573428,
                    "capacity": null,
                    "description": "",
                    "tickets_sold": 0,
                    "lecture_summary_file": null,
                    "price": null,
                    "price_currency": "RUB"
                },
                "relationships": {
                    "lecturer": {
                        "data": {
                            "type": "Lecturer",
                            "id": "19"
                        }
                    },
                    "category": {
                        "data": {
                            "type": "Category",
                            "id": "19"
                        }
                    }
                }
            },
            {
                "type": "OfflineLecture",
                "id": "19",
                "attributes": {
                    "name": "Offline lecture 1",
                    "address": "",
                    "picture": "http://127.0.0.1:8000/media/lecture_pictures/1573646089377-9wpu20ce.jpeg",
                    "lecture_date": "1996-09-11T09:06:21+04:00",
                    "lecture_date_ts": 842407581,
                    "capacity": null,
                    "description": "",
                    "tickets_sold": 0,
                    "lecture_summary_file": null,
                    "price": null,
                    "price_currency": "RUB"
                },
                "relationships": {
                    "lecturer": {
                        "data": {
                            "type": "Lecturer",
                            "id": "20"
                        }
                    },
                    "category": {
                        "data": {
                            "type": "Category",
                            "id": "20"
                        }
                    }
                }
            },
            {
                "type": "OfflineLecture",
                "id": "20",
                "attributes": {
                    "name": "Offline lecture 0",
                    "address": "",
                    "picture": "http://127.0.0.1:8000/media/lecture_pictures/1573646089377-9wpu20ce.jpeg",
                    "lecture_date": "1992-04-07T01:51:02+04:00",
                    "lecture_date_ts": 702586262,
                    "capacity": null,
                    "description": "",
                    "tickets_sold": 0,
                    "lecture_summary_file": null,
                    "price": "1000.00",
                    "price_currency": "RUB"
                },
                "relationships": {
                    "lecturer": {
                        "data": {
                            "type": "Lecturer",
                            "id": "21"
                        }
                    },
                    "category": {
                        "data": {
                            "type": "Category",
                            "id": "21"
                        }
                    }
                }
            },
            {
                "type": "OfflineLecture",
                "id": "24",
                "attributes": {
                    "name": "Offline lecture 1",
                    "address": "",
                    "picture": "http://127.0.0.1:8000/media/lecture_pictures/1573646089377-9wpu20ce.jpeg",
                    "lecture_date": "2013-05-25T22:16:49+04:00",
                    "lecture_date_ts": 1369491409,
                    "capacity": null,
                    "description": "",
                    "tickets_sold": 0,
                    "lecture_summary_file": null,
                    "price": "1000.00",
                    "price_currency": "RUB"
                },
                "relationships": {
                    "lecturer": {
                        "data": {
                            "type": "Lecturer",
                            "id": "25"
                        }
                    },
                    "category": {
                        "data": {
                            "type": "Category",
                            "id": "25"
                        }
                    }
                }
            },
            {
                "type": "OfflineLecture",
                "id": "25",
                "attributes": {
                    "name": "Offline lecture 2",
                    "address": "",
                    "picture": "http://127.0.0.1:8000/media/lecture_pictures/1573646089377-9wpu20ce.jpeg",
                    "lecture_date": "1990-07-21T01:50:40+04:00",
                    "lecture_date_ts": 648499840,
                    "capacity": null,
                    "description": "",
                    "tickets_sold": 0,
                    "lecture_summary_file": null,
                    "price": "1000.00",
                    "price_currency": "RUB"
                },
                "relationships": {
                    "lecturer": {
                        "data": {
                            "type": "Lecturer",
                            "id": "26"
                        }
                    },
                    "category": {
                        "data": {
                            "type": "Category",
                            "id": "26"
                        }
                    }
                }
            }
        ],
        "included": [
            {
                "type": "Category",
                "id": "19",
                "attributes": {
                    "name": "Аниме",
                    "color": "#be78be"
                }
            },
            {
                "type": "Category",
                "id": "20",
                "attributes": {
                    "name": "Кино",
                    "color": "#df78be"
                }
            },
            {
                "type": "Category",
                "id": "21",
                "attributes": {
                    "name": "Архитектура",
                    "color": "#ad78be"
                }
            },
            {
                "type": "Category",
                "id": "25",
                "attributes": {
                    "name": "Искусство",
                    "color": "#be78be"
                }
            },
            {
                "type": "Category",
                "id": "26",
                "attributes": {
                    "name": "Кино",
                    "color": "#ad78be"
                }
            },
            {
                "type": "Lecturer",
                "id": "19",
                "attributes": {
                    "name": "Isabel Gibbs",
                    "userpic": null,
                    "bio": "Western blood yes too. Claim big event themselves cost rather story. Wide industry career have.\nBig open lose some American five those. Large guess religious me traditional road."
                }
            },
            {
                "type": "Lecturer",
                "id": "20",
                "attributes": {
                    "name": "Michelle Levy",
                    "userpic": null,
                    "bio": "Issue tonight woman before culture. Song network certainly walk our do authority American. Response bar matter oil everything start."
                }
            },
            {
                "type": "Lecturer",
                "id": "21",
                "attributes": {
                    "name": "Melissa Collins",
                    "userpic": null,
                    "bio": "Trouble when worry officer. Baby central ago keep although red interesting.\nOccur trip stop have discuss. Usually teacher and join card wife note put. Fly see section enjoy use similar."
                }
            },
            {
                "type": "Lecturer",
                "id": "25",
                "attributes": {
                    "name": "Jackson Moore",
                    "userpic": null,
                    "bio": "Ball act agency begin season never. Image knowledge professional piece serve scientist position real. Fish consider up bit know where second."
                }
            },
            {
                "type": "Lecturer",
                "id": "26",
                "attributes": {
                    "name": "Timothy Jones",
                    "userpic": null,
                    "bio": "Government nice once reflect fish street staff. Sort beyond determine chair.\nShare visit though there walk stand."
                }
            }
        ],
        "meta": {
            "pagination": {
                "page": 1,
                "pages": 1,
                "count": 5
            }
        }
    }

## Список ендпойнтов  *api*<a id="sec-1-6"></a>

-   "users": "*api/users*"
-   "payment<sub>methods</sub>": "*api/payment<sub>methods</sub>*",
-   "tickets": "*api/tickets*",
-   "events": "*api/events*",
-   "offline-lectures": "*api/offline-lectures*",
-   "video-lectures": "*api/video-lectures*",
-   "cart": "*api/cart*",
-   "order-items": "*api/order-items*",
-   "categories": "*api/categories*",
-   "lecturers": "*api/lecturers*"
