# xDevices
Обработка данных от xDevices

xDevices, это устройства с модулем беспроводной передачи данных xBee 802.15.4 от Digi International Inc. 

Виды устройств:
  1. xCoordinator - 3 дискретных входа, 3 выхода "сухой контакт" (реле), связь с PC по USB (виртуальный COM-порт). 
  2. xSlave - 6 дискретных/аналоговых входов (выбор режима джампером), 2 выхода "сухой контакт" (реле).
  3. xMaster - 3 дискретных входа, 3 выхода "сухой контакт" (реле), подключение и работа в паре с контроллером MegaD-328 (http://ab-log.ru/smart-house/ethernet/megad-328).

xCoordinator может опрашивать все устройства в сети, отправлять им управляющие команды и отдавать полученные данные на PC.
xSlave умеет работать как в связке с xCoordinator, так и с xMaster. При втором варианте работы он образует беспроводной мост между MegaD-328 + xMaster и собой.
В этом режиме xSlave фактически является удалённым исполнительным устройством контроллера MegaD-328 (http://ab-log.ru/forum/viewtopic.php?f=1&t=875&hilit=xkit). 

# Получение данных от xCoordinator

xbee_to_zmq.py - получение данных от устройств, преобразование и отправка через сервер сообщений ZeroMQ. 
Любой клиент, подключившийся в серверу сообщений, получает обработанные данные в формате JSON.

zmq_to_flask.py - получение JSON данных от сервера сообщений ZeroMQ и передача клиенту (web browser) через web-сервер Flask.
По адресу 127.0.0.2:5000 отображаются данные с устройств. 
