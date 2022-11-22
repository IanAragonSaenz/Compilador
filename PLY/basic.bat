@ECHO OFF

ECHO Compilando y Ejecutando programa

python parser.py %1
python vm.py %2

