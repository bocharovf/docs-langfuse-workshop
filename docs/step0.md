# Инструментируем код

Вы, как разработчики, сами управляете тем, как выглядит трейс и можете добавлять спаны так, чтобы дерево было понятнее.

В нашем проекте все прекрасно, кроме того, что часть алгоритма не видна в трейсе! Функция `choose_prompt` в файле `agent.py`, с которой нам еще предстоит поработать, вызывается в коде, но в трейсе не видна!

## Как сделать вызов функции наблюдаемым

Примеры инструментирования можно подглядеть в функциях `ask_llm` или `choose_model`.

Самый простой, но ограниченный способ - навесить на функцию декоратор @observe.

```python

@observe(name="choose_prompt")
def choose_prompt():

    ### code here ...
```

Более продвинутый и рекомендуемый способ - обернуть нужный фрагмент кода в блок `with langfuse.start_as_current_observation`

```python
def choose_prompt():

    with langfuse.start_as_current_observation(
        as_type="span",
        name="choose_prompt"
    ) as span:

        ### code here ...

        span.update(
            output=prompt
        )

    return prompt
```

В этом случае мы можем явно задать `input` и `output` спана, а также дополнительную метаинформацию.

Перезапустите агент:
```
docker compose up -d --force-recreate cookbook-agent
```

И сделай новый запрос рецепта, чтобы проверить изменения в трейсе.

[Официальная документация](https://langfuse.com/docs/observability/sdk/instrumentation)

## Задача

Инструментировать код функции `choose_prompt` так, чтобы в трейсе появился соответствующий ей спан. 

В спане в `output` должен присутствовать текст выбранного промпта.
