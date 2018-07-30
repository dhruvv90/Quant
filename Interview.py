n = 5
for i in range(n):
	for j in range(i):
		print (" "),
	for j in range(2*n-1-2*i):
		if i==n-1 and j==2*n-1-2*i-1:
			print (0),
		elif i%2==0 and j==0:
			print (0),
		elif 2*j==2*n - 1 -2*i-1:
			print (1),
		elif i%2==1 and j ==2*n - 1 -2*i-1:
			print (0),
		else: print ('*'),
	print ('\n')