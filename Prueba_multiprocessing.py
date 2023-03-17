import multiprocessing

def func(i, k):
    print(i)
    print(k)
    pass

if __name__ == '__main__':
    # Define the list of values for i and create a dictionary of dfs
    lista = [1, 2, 3, 4, 5]  # Example list of numbers

    # Create a multiprocessing.Pool object with the number of processes you want to use
    pool = multiprocessing.Pool(processes=4)  # change the number of processes as desired
    k = "c"
    
    if k == "a" or k == "c":
        print("olaaa")
        [pool.apply(func, args=(i, "a")) for i in lista]
        print("fuera")
    if k == "b" or k == "c":
        print("olaaa")
        [pool.apply(func, args=(i, "b")) for i in lista]
        print("fuera")        
    # Close the pool and wait for all processes to finish
    pool.close()
    pool.join()