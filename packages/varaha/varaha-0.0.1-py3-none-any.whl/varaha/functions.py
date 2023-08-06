def m1m2_to_mcheta(m1, m2):
    '''
    Get chirp mass and symmetric mass ratio from component masses
    '''    
    return (m1*m2)**.6/(m1+m2)**.2, m1*m2/(m1+m2)**2


def m1m2_to_mchq(m1, m2):
    '''
    Get chirp mass and mass ratio from component masses
    '''    
    return (m1*m2)**.6/(m1+m2)**.2, m2/m1


def qmch_to_m1m2(mch, q):
    '''
    Get component masses from mass ratio and chirp mass
    '''    
    return mch*(1 + q)**.2/q**.6, q**.4*mch*(1 + q)**.2
