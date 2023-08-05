numero_inicial = int(input('Informe o número inicial: '))
numero_final = int(input('Informe o número final: '))
x = numero_inicial - 1
f= open("numeros.txt","w+")
while x < numero_final:
	x = x + 1
	value =  ('|'+ str(x) +'|')
	f.write(value + "\n")
print("Números gerados com sucesso!!!Confira o arquivo numeros.txt!!!")

	