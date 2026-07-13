## Выводы

**Вы молодцы!**

1. Трассировка делает работу AI-агента наблюдаемой. Для диагностики крайне важно логировать `input` и `output` вызовов LLM.

2. `LLM-as-a-judge` - один из хороших способов не допустить регресса, но он стоит денег.

3. Централизованное управление промптами крайне удобно, но нужно грамотно выстраивать процесс изменений.

4. Управление контекстом запросов к LLM – ключ к отсутствию галлюцинаций.

## Ссылки для дальнейшего изучения

- Как [визуализировать смыслы текстов](https://t.me/technosurvival/17)
- [Обзор функционала Langfuse на примере](https://youtu.be/cHArvZPFAgM?si=739AvGBlaipCjomm)
- [Документация Langfuse](https://langfuse.com/docs)
- Мы не использовали фреймворки, чтобы не скрывать детали реализации. Но на практике вы наверняка используете фреймворк наподобие `Langchain`, и ваша интеграция с Langfuse станет еще проще: [Langchain интеграция с Langfuse](https://docs.langchain.com/oss/python/integrations/providers/langfuse)
- Стандарт наблюдаемости [OpenTelemetry](https://opentelemetry.io/)
- [Отличные видео](https://www.youtube.com/@bdmitriipro) по AI агентам
- [Учебник по ML от Яндекса](https://education.yandex.ru/handbook/ml)
- [Отличная книга](https://www.piter.com/blog/kniga-system-design-podgotovka-k-slozhnomu-intervyu-po-genai) для подготовки к собеседованию по проектированию GenAI
- Как [читать мысли LLM](https://t.me/technosurvival/24)


## Авторы

**Бочаров Филипп**

Более 8 лет занимаюсь наблюдаемостью систем и рассказываю об этом на Highload++.
Автор tg-канала [@technosurvival](https://t.me/technosurvival)

![Филипп Бочаров](/img/bocharovf30.jpg)

**Дмитрий Лобач**

Запустил сервис на базе Langfuse внутри МТС Web Services, которым пользуются десятки продуктов.

![Дмитрий Лобач](/img/lobach30.jpg)

**Даниел Иванов**

Архитектор в МТС Web Services.

![Даниел Иванов](/img/ivanov30.jpg)
