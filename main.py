import sys
from SourceCode.Console import  get_commands
from SourceCode.Transformation import  creat_pickle_dump

from SourceCode.Parser.get_names import get_names
from SourceCode.Parser.get_mkb import get_mkb
from SourceCode.Parser.get_ra_la import get_ra,get_la
from SourceCode.Parser.get_age import get_age
from SourceCode.Parser.get_sex import get_sex
from SourceCode.Parser.get_weight import get_weight
from SourceCode.Parser.get_height import get_height
from SourceCode.Parser.get_coagulology import get_coagulology
from SourceCode.Parser.get_ef import get_ef
from SourceCode.Parser.get_chss import get_chss
from SourceCode.Parser.get_diabete import get_diabete



from SourceCode.Connection.set_data_on_file import set_data_on_file
from SourceCode.Connection.adding_names import adding_names
from SourceCode.Connection.adding_mkb import adding_mkb
from SourceCode.Connection.adding_ra import adding_ra
from SourceCode.Connection.adding_la import adding_la
from SourceCode.Connection.adding_age import adding_age
from SourceCode.Connection.adding_sex import adding_sex
from SourceCode.Connection.adding_weight import adding_weight
from SourceCode.Connection.adding_height import adding_height
from SourceCode.Connection.adding_coagulology import adding_coagulology_before,adding_coagulology_after
from SourceCode.Connection.adding_ef import adding_ef
from SourceCode.Connection.adding_chss import adding_chss
from SourceCode.Connection.adding_diabete import adding_diabete



path_path = r'C:\Users\bisma\Desktop\Ucheba\Diser\DataPreprocessing\DataPreprocessing\path.txt'

data_path = {}

def load_path():
    print( "Load path" )
    try:
        path_file = open( path_path, 'r' )
        path_text = path_file.read()
        for path in path_text.split('\n') :
            path = path.split(';')
            data_path[ path[0] ] = path[1]
    except:
        sys.exit(0)

def running_comand( comand ):

    if( comand[0] == "exit" or comand[0] == "e" ):
        sys.exit(0)
    if( comand[0] == "reload" or comand[0] == "rl" ):
        load_path()
    elif( comand[0] == "get_pickle" or comand[0] == "gp" ):
        creat_pickle_dump(data_path['HTML'],data_path["txt"],data_path["pickle"])
    
    elif( comand[0] == "get_names" or comand[0] == "gns" ):
        names = get_names(data_path["pickle"])
        set_data_on_file(data_path['names'],names[0],names[1:len(names)-1],i=1,j=1)
    elif( comand[0] == "load_names" or comand[0] == "lns" ):
        adding_names(n1=int(data_path['n1']),n2=int(data_path['n2']),path_consumer=data_path['dataset'],path_source=data_path['names'])
    
    elif( comand[0] == "get_mkb" or comand[0] == "gmkb" ):
        mkb = get_mkb( data_path["pickle"] )
        set_data_on_file(data_path['mkb'],mkb[0],mkb[1:len(mkb)-1],i=1,j=1)
    elif( comand[0] == "load_mkb" or comand[0] == "lmkb" ):
        adding_mkb(n1=int(data_path['n1']),n2=int(data_path['n2']),path_consumer=data_path['dataset'],path_source=data_path['mkb'])
    
    elif( comand[0] == "get_ra" or comand[0] == "gra" ):
        ra = get_ra( data_path["pickle"] )
        set_data_on_file(data_path['ra'],ra[0],ra[1:len(ra)-1],i=1,j=1)
    elif( comand[0] == "load_ra" or comand[0] == "lra" ):
        adding_ra(n1=int(data_path['n1']),n2=int(data_path['n2']),path_consumer=data_path['dataset'],path_source=data_path['ra'])

    elif( comand[0] == "get_la" or comand[0] == "gla" ):
        la = get_la( data_path["pickle"] )
        set_data_on_file(data_path['la'],la[0],la[1:len(la)-1],i=1,j=1)
    elif( comand[0] == "load_la" or comand[0] == "lla" ):
        adding_la(n1=int(data_path['n1']),n2=int(data_path['n2']),path_consumer=data_path['dataset'],path_source=data_path['la'])

    elif( comand[0] == "get_age" or comand[0] == "ga" ):
        age = get_age( data_path["pickle"] )
        set_data_on_file(data_path['age'],age[0],age[1:len(age)-1],i=1,j=1)
    elif( comand[0] == "load_age" or comand[0] == "la" ):
        adding_age(n1=int(data_path['n1']),n2=int(data_path['n2']),path_consumer=data_path['dataset'],path_source=data_path['age'])

    elif( comand[0] == "get_sex" or comand[0] == "gs" ):
        sex = get_sex( data_path["pickle"] )
        set_data_on_file(data_path['sex'],sex[0],sex[1:len(sex)-1],i=1,j=1)
    elif( comand[0] == "load_sex" or comand[0] == "ls" ):
        adding_sex(n1=int(data_path['n1']),n2=int(data_path['n2']),path_consumer=data_path['dataset'],path_source=data_path['sex'])
    
    elif( comand[0] == "get_weight" or comand[0] == "gw" ):
        weight = get_weight( data_path["pickle"] )
        set_data_on_file(data_path['weight'],weight[0],weight[1:len(weight)-1],i=1,j=1)
    elif( comand[0] == "load_weight" or comand[0] == "lw" ):
        adding_weight(n1=int(data_path['n1']),n2=int(data_path['n2']),path_consumer=data_path['dataset'],path_source=data_path['weight'])

    elif( comand[0] == "get_height" or comand[0] == "gh" ):
        height = get_height( data_path["pickle"] )
        set_data_on_file(data_path['height'],height[0],height[1:len(height)-1],i=1,j=1)
    elif( comand[0] == "load_height" or comand[0] == "lh" ):
        adding_height(n1=int(data_path['n1']),n2=int(data_path['n2']),path_consumer=data_path['dataset'],path_source=data_path['height'])

    elif( comand[0] == "get_coagulology" or comand[0] == "gc" ):
        coagulology = get_coagulology( data_path["HTML"] )
        set_data_on_file(data_path['coagulology'],coagulology[0],coagulology[1:len(coagulology)-1],i=1,j=1)
    elif( comand[0] == "load_coagulology_befor" or comand[0] == "lcb" ):
        adding_coagulology_before(n1=int(data_path['n1']),n2=int(data_path['n2']),path_consumer=data_path['dataset'],path_source=data_path['coagulology'])
    elif( comand[0] == "load_coagulology_befor" or comand[0] == "lca" ):
        adding_coagulology_after(n1=int(data_path['n1']),n2=int(data_path['n2']),path_consumer=data_path['dataset'],path_source=data_path['coagulology'])

    elif( comand[0] == "get_ef" or comand[0] == "gef" ):
        ef = get_ef( data_path["HTML"] )
        set_data_on_file(data_path['ef'],ef[0],ef[1:len(ef)-1],i=1,j=1)
    elif( comand[0] == "load_ef" or comand[0] == "lef" ):
        adding_ef(n1=int(data_path['n1']),n2=int(data_path['n2']),path_consumer=data_path['dataset'],path_source=data_path['ef'])

    elif( comand[0] == "get_chss" or comand[0] == "gchss" ):
        chss = get_chss( data_path["HTML"] )
        set_data_on_file(data_path['chss'],chss[0],chss[1:len(chss)-1],i=1,j=1)
    elif( comand[0] == "load_chss" or comand[0] == "lchss" ):
        adding_chss(n1=int(data_path['n1']),n2=int(data_path['n2']),path_consumer=data_path['dataset'],path_source=data_path['chss'])

    elif( comand[0] == "get_diabete" or comand[0] == "gdi" ):
        diabete = get_diabete( data_path["pickle"] )
        set_data_on_file(data_path['diabete'],diabete[0],diabete[1:len(diabete)],i=1,j=1)
    elif( comand[0] == "load_diabete" or comand[0] == "ldi" ):
        adding_diabete(n1=int(data_path['n1']),n2=int(data_path['n2']),path_consumer=data_path['dataset'],path_source=data_path['diabete'])


def main():
    print("load program")
    print( "Program begin" )
    load_path()
    while True :
        comand = get_commands()
        if( len(comand) != 0 ):
            running_comand( comand )
            


if( __name__ == '__main__' ):
    main()

    
