# Port Scanner
**Port Scanner** es otro escaner de puertos mas, muy parecido en uso a el famoso nmap 

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)
![License](https://img.shields.io/github/license/bellcodev/port-scanner)
![Last Commit](https://img.shields.io/github/last-commit/bellcodev/port-scanner)
![Issues](https://img.shields.io/github/issues/bellcodev/port-scanner)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Stars](https://img.shields.io/github/stars/bellcodev/port-scanner?style=social)
![Forks](https://img.shields.io/github/forks/bellcodev/port-scanner?style=social)

imagenes ejemplo de uso:
| <img width="484" height="260" alt="image" src="https://github.com/user-attachments/assets/33f55c4e-d677-40c3-b049-9e3a17f640f0" /> |
|---|

| <img width="522" height="227" alt="image" src="https://github.com/user-attachments/assets/d10cf8a7-d167-4dcb-92b5-4ea840d38932" /> |
|---|

Parametros: 

            -p1,2,3,4 o --port1,2,3,4 para escanear puertos especificos

            -p- o --port- para escanear los 65536 puertos posibles
            
            -d 0 o --delay 0 para ponerle tiempo de delay entre escaneo y escaneo
            
            -o nombre.txt o --output nombre.txt para guardar el escaneo en un archivo
            
            -Pn o --noping para escanear aunque la ip no de ping
            
            -h o --help para una lista de ayuda
            
            El ultimo parametro siempre sera la ip a escanear


Uso:
```
git clone https://github.com/bellcodev/port-scanner
cd port-scanner
python3 main.py -h
```
