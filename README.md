# opc-eaton.py
Hlavní program je pilot ludgar.py 
redis_migrate. py běží na windows clientu  pokouší se v 30s intervalu přesuvá  data z redisu lokalního 127.0.0.1:6379 do serverového skrz wireguard a to na adresu 192.168.123.65:6379 
influx.py běži ne serveru prochází redis databaze z serveru bere data přesouvá do influd databáze 
