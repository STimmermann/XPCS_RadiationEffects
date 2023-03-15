import configparser as configparser
import ast
import h5py

def GetConfiguration(sample='Aeroegel_e4m_02',series=1,rawdir='../../raw'): #method for extracting information out of the .fio file
    
    #open .fio file for detector, energy, pixelsize etc
    with open(rawdir+'/'+sample+'_000{:02d}/'.format(series)+sample+'_000{:02d}.fio'.format(series)) as f: #open fio file 
        fio_cont = f.read()
        fio_start = fio_cont.find('_beamtimeID')
        file_content = '[config]\n' + fio_cont[fio_start:] # add a section header to the string such that the string can be read by ConfigParser
    config_parser = configparser.RawConfigParser(comment_prefixes=('!','%')) #create Config Parser with ! and % as comment marker to skip first lines
    config_parser.read_string(file_content) # read content of string, can be accessed via config_parser['config'][id in fio file]
     
    #get detector identifier
    if(config_parser['config']['_ccd']=='e4m'):
        dataFolder = 'e4m' #subfolder where the raw data are
        detector = 'eiger4m' #detector identifier for Xana
    elif(config_parser['config']['_ccd']=='e500'):
        dataFolder = 'e500'
        detector = 'eiger500k'
    else:
        print('detector could not be identified')
        
    distance = ast.literal_eval(config_parser['config']['_distance']) #get sample detector distance in mm
    pixelSize = ast.literal_eval(config_parser['config']['_pixelsize']) #get pixelsize in mm
    pulseEnergy = ast.literal_eval(config_parser['config']['fmbenergy']) #get pulse Energy in eV
    
    #open .batchinfo file for coordinates of beam center
    with open(rawdir+'/'+sample+'_000{:02d}/'.format(series)+dataFolder +'/'+sample+'_000{:02d}.batchinfo'.format(series)) as f:
        file_content = '[batchinfo]\n' + f.read() # add a section header to the string such that the string can be read by ConfigParser
    config_parser = configparser.RawConfigParser(comment_prefixes=('!','%'),allow_no_value=True) #create Config Parser with ! and % as comment marker to skip first lines
    config_parser.read_string(file_content) # read content of string, can be accessed via config_parser['config'][id in fio file]
    
    centerX = ast.literal_eval(config_parser['batchinfo']['x0'])
    centerY = ast.literal_eval(config_parser['batchinfo']['y0'])
    
    return([dataFolder,detector,distance,pixelSize,pulseEnergy,centerX,centerY]) 

def GetConfigurationSciKit(sample='Aeroegel_e4m_02',series=1,rawdir='../../raw'): #method for extracting information out of the .fio file
    
    #open .fio file for detector, energy, pixelsize etc
    with open(rawdir+'/'+sample+'_000{:02d}/'.format(series)+sample+'_000{:02d}.fio'.format(series)) as f: #open fio file 
        fio_cont = f.read()
        fio_start = fio_cont.find('_beamtimeID')
        file_content = '[config]\n' + fio_cont[fio_start:] # add a section header to the string such that the string can be read by ConfigParser
    config_parser = configparser.RawConfigParser(comment_prefixes=('!','%')) #create Config Parser with ! and % as comment marker to skip first lines
    config_parser.read_string(file_content) # read content of string, can be accessed via config_parser['config'][id in fio file]
     
    #get detector identifier
    if(config_parser['config']['_ccd']=='e4m'):
        dataFolder = 'e4m' #subfolder where the raw data are
        detector = 'eiger4m' #detector identifier for Xana
    elif(config_parser['config']['_ccd']=='e500'):
        dataFolder = 'e500'
        detector = 'eiger500k'
    else:
        print('detector could not be identified')
        
    distance = ast.literal_eval(config_parser['config']['_distance']) #get sample detector distance in mm
    pixelSize = ast.literal_eval(config_parser['config']['_pixelsize']) #get pixelsize in mm
    
    #open master file for time between frames
    with h5py.File(rawdir+'/'+sample+'_000{:02d}/'.format(series)+dataFolder +'/' + sample +'_000{:02d}_master.h5'.format(series), 'r') as hf:
        tReadout = hf.get('/entry/instrument/detector/frame_time').value # 
        lamda = hf.get('/entry/instrument/beam/incident_wavelength').value
    with open(rawdir+'/'+sample+'_000{:02d}/'.format(series)+dataFolder +'/'+sample+'_000{:02d}.batchinfo'.format(series)) as f:
        file_content = '[batchinfo]\n' + f.read() # add a section header to the string such that the string can be read by ConfigParser
    config_parser = configparser.RawConfigParser(comment_prefixes=('!','%'),allow_no_value=True) #create Config Parser with ! and % as comment marker to skip first lines
    config_parser.read_string(file_content) # read content of string, can be accessed via config_parser['config'][id in fio file]
    
    centerX = ast.literal_eval(config_parser['batchinfo']['x0'])
    centerY = ast.literal_eval(config_parser['batchinfo']['y0'])
    detX = ast.literal_eval(config_parser['batchinfo']['col_end'])
    detY = ast.literal_eval(config_parser['batchinfo']['row_end'])
    
    return([dataFolder,detector,distance,pixelSize,lamda,centerX,centerY,tReadOut,detX,detY])

def get_methods(object, spacing=20):
    methodList = []
    for method_name in dir(object):
        try:
            if callable(getattr(object, method_name)):
                methodList.append(str(method_name))
        except:
            methodList.append(str(method_name))
    processFunc = (lambda s: ' '.join(s.split())) or (lambda s: s)
    for method in methodList:
        try:
            print(str(method.ljust(spacing)) + ' ' +
                  processFunc(str(getattr(object, method).__doc__)[0:90]))
        except:
            print(method.ljust(spacing) + ' ' + ' getattr() failed')