#interactivepython.org
def mergeSort(q):
	if len(q) < 2:
		return q
	m = len(q)//2 #get the mdle
	l = q[:m] #merge sort items from the beginning through m-1
	r = q[m:] #merge sort items m through the rest of the array
	mergeSort(l)
	mergeSort(r)

	i = j = k = 0
	while i < len(l) and j < len(r): 
		if l[i] < r[j]:
			q[k]=l[i]
			i=i+1
		else:
			q[k]=r[j]
			j=j+1
		k=k+1

	while i < len(l):
		q[k]=l[i]
		i=i+1
		k=k+1

	while j < len(r):
		q[k]=r[j]
		j=j+1
		k=k+1
	
q = [54,26,93,17,77,31,44,55,20]
print("Before mergeSort: ",q)
mergeSort(q)
print("After mergeSort: ",q)