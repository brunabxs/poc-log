## O que gostaríamos de ter no log

### 1. Uma cadeia de requisições poderia apresentar o mesmo identificador.
A seguir, temos um exemplo de uma cadeia de requisições

```python
# Send card details
POST /cards/lost_and_stolen/

    # First, look up the card details
    GET /cards/1234567890123456/

    # Look up the owning account to ensure it's still open
    GET /accounts/123456/

    # Close the card
    DELETE /cards/1234567890123456/

    # Finally, order a new card for the member
    POST /accounts/123456/card/
```

Um identificador único é atribuído a cada requisição.
Se a requisição não possui um identificador, adicionar um;
caso contrário, utiliza o já existente e adiciona um novo

Desta forma, a cadeia de requisição descrita o exemplo anterior, poderia ser descrita como:
```python
0dadb33f-ee15-470a-bfc8-5e35926793a5 POST /cards/lost_and_stolen/
0dadb33f-ee15-470a-bfc8-5e35926793a5,ac0eabbd-122f-491c-aacf-670d255eef3d GET /cards/1234567890123456/
0dadb33f-ee15-470a-bfc8-5e35926793a5,f2aab75e-719f-4a00-8d81-a1266cfb6a81 GET /accounts/123456/
0dadb33f-ee15-470a-bfc8-5e35926793a5,639832bf-111c-40ac-abed-bf93ae15c54d DELETE /cards/1234567890123456/
0dadb33f-ee15-470a-bfc8-5e35926793a5,68493175-8a39-421b-99e9-53e937fa5d12 POST /accounts/123456/card/
```

Com essa implementação seria possível identificar o passo a passo do que aconteceu com a requisição.
O exemplo acima e a solução para o Flask podem ser vistos [aqui](http://blog.mcpolemic.com/2016/01/18/adding-request-ids-to-flask.html).


### 2. Chamadas
 
https://stackoverflow.com/questions/20173594/get-current-celery-task-id-anywhere-in-the-thread



https://structlog.readthedocs.io/en/stable/api.html#module-structlog.threadlocal




https://gist.github.com/ibeex/3257877

https://www.google.com.br/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwjs6q3xs4fXAhWDDpAKHe4sCKkQFggnMAA&url=http%3A%2F%2Fblog.mcpolemic.com%2F2016%2F01%2F18%2Fadding-request-ids-to-flask.html&usg=AOvVaw33QJHQEtBFhHER43bINVSH


https://github.com/Workable/flask-log-request-id/blob/develop/flask_log_request_id/request_id.py


## LogBook

### Advantages over Logging

If properly configured, Logbook’s logging calls will be very cheap and provide a great performance improvement over an equivalent configuration of the standard library’s logging module. While for some parts we are not quite at performance we desire, there will be some further performance improvements in the upcoming versions.

It also supports the ability to inject additional information for all logging calls happening in a specific thread or for the whole application. For example, this makes it possible for a web application to add request-specific information to each log record such as remote address, request URL, HTTP method and more.

The logging system is (besides the stack) stateless and makes unit testing it very simple. If context managers are used, it is impossible to corrupt the stack, so each test can easily hook in custom log handlers.
