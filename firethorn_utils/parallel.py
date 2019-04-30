import os                                                                       
from multiprocessing import Pool                                                

process_list = range(200)
	
def run_process(process_counter):                                                             
    print ("Starting RUN # " + str(process_counter))
    os.system('python3 -c "import firethorn_utils.validator as validator;validator.main()" -ft=http://localhost:8081/firethorn -r=1808 -u=Soopheef1AeKeeyohtos -p=Faew3yoohuechoo8eiT6 -g=iuquae2poG8yiph7agh3')                                       
    print ("Ended RUN # " + str(process_counter))


pool = Pool(processes=20)                                                        
pool.map(run_process, process_list)   
