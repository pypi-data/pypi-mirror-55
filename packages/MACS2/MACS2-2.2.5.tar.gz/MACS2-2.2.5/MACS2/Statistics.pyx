# cython: language_level=3
# cython: profile=True
# Time-stamp: <2019-10-30 17:27:50 taoliu>

"""Module Description: Statistics function wrappers.

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD License (see the file LICENSE included with
the distribution).
"""

from MACS2.khash cimport *
from libc.math cimport log10, log
from MACS2.Prob import poisson_cdf

cdef class P_Score_Upper_Tail:
    """Unit to calculate -log10 poisson_CDF of upper tail and cache
    results in a hashtable.
    """
    cdef:
        kh_int64_t *pscore_table # a hash where key is integr, value is float
        dict pscore_dict
        
    def __init__ ( self, size_hint = 1 ):
        if size_hint is not None:
            kh_resize_int64( self.pscore_table, size_hint )
        self.pscore_dict = dict()
            
    def __cinit__( self ):
        self.pscore_table = kh_init_int64()

    def __dealloc__( self ):
        kh_destroy_int64(self.pscore_table)

    cpdef bint check_cache ( self, int x, float l ):
        """Check if the Poisson CDF(x|l) has been calculated and
        cached.
         
        """
        cdef:
            khiter_t k                  # index got from get_init64 function
            long key_value

        key_value = hash( (x, l) )
        k = kh_get_int64( self.pscore_table, key_value )
        return k != self.pscore_table.n_buckets

    cpdef float get_pscore ( self, int x, float l ):
        cdef:
            float val

        if (x, l) in self.pscore_dict:
            return self.pscore_dict[(x, l)]
        else:
            # calculate and cache
            val = -1 * poisson_cdf ( x, l, False, True )
            self.pscore_dict[(x, l)] = val
            return val

cdef class LogLR_Asym:
    """Unit to calculate asymmetric log likelihood, and cache
    results in a hashtable.
    """
    cdef:
        kh_int64_t *logLR_table # a hash where key is integr, value is float
        
    def __init__ ( self, size_hint = 1 ):
        if size_hint is not None:
            kh_resize_int64( self.logLR_table, size_hint )
            
    def __cinit__( self ):
        self.logLR_table = kh_init_int64()

    def __dealloc__( self ):
        kh_destroy_int64(self.logLR_table)

    cpdef bint check_cache ( self, float x, float y ):
        """Check if the logLR of enrich:x background:y; has been
        calculated and cached.
         
        """
        cdef:
            khiter_t k                  # index got from get_init64 function
            long key_value

        key_value = hash( (x, y) )
        k = kh_get_int64( self.logLR_table, key_value )
        return k != self.logLR_table.n_buckets

    cpdef float get_logLR_asym ( self, float x, float y ):
        cdef:
            khiter_t k                  # index got in the table; translated from hash key
            int ret = 0
            float val
            long key_value              # hash key
        key_value = hash( (x, y) )
        k = kh_get_int64(self.logLR_table, key_value) # translate hash key to index 
        if k != self.logLR_table.n_buckets: #kh_exist_int64( self.pscore_table, k ):
            return self.logLR_table.vals[k]
        else:
            # calculate and cache
            if x > y:
                val = (x*(log10(x)-log10(y))+y-x)
            elif x < y:
                val = (x*(-log10(x)+log10(y))-y+x)
            else:
                val = 0

            k = kh_put_int64( self.logLR_table, key_value, &ret )
            self.logLR_table.keys[ k ] = key_value
            self.logLR_table.vals[ k ] = val
            return val


cdef class LogLR_Sym:
    """Unit to calculate symmetric log likelihood, and cache
    results in a hashtable.

    "symmetric" means f(x,y) = -f(y,x)
    """
    cdef:
        kh_int64_t *logLR_table # a hash where key is integr, value is float
        
    def __init__ ( self, size_hint = 1 ):
        if size_hint is not None:
            kh_resize_int64( self.logLR_table, size_hint )
            
    def __cinit__( self ):
        self.logLR_table = kh_init_int64()

    def __dealloc__( self ):
        kh_destroy_int64(self.logLR_table)

    cpdef bint check_cache ( self, float x, float y ):
        """Check if the logLR of enrich:x background:y; has been
        calculated and cached.
         
        """
        cdef:
            khiter_t k                  # index got from get_init64 function
            long key_value

        key_value = hash( (x, y) )
        k = kh_get_int64( self.logLR_table, key_value )
        return k != self.logLR_table.n_buckets

    cpdef float get_logLR_sym ( self, float x, float y ):
        cdef:
            khiter_t k                  # index got in the table; translated from hash key
            int ret = 0
            float val
            long key_value              # hash key
        key_value = hash( (x, y) )
        k = kh_get_int64(self.logLR_table, key_value) # translate hash key to index 
        if k != self.logLR_table.n_buckets: #kh_exist_int64( self.pscore_table, k ):
            return self.logLR_table.vals[k]
        else:
            # calculate and cache
            if x > y:
                val = (x*(log10(x)-log10(y))+y-x)
            elif y > x:
                val = (y*(log10(x)-log10(y))+y-x)
            else:
                val = 0

            k = kh_put_int64( self.logLR_table, key_value, &ret )
            self.logLR_table.keys[ k ] = key_value
            self.logLR_table.vals[ k ] = val
            return val


cdef class LogLR_Diff:
    """Unit to calculate log likelihood for differential calling, and cache
    results in a hashtable.

    here f(x,y) = f(y,x) and f() is always positive.
    """
    cdef:
        kh_int64_t *logLR_table # a hash where key is integr, value is float
        
    def __init__ ( self, size_hint = 1 ):
        if size_hint is not None:
            kh_resize_int64( self.logLR_table, size_hint )
            
    def __cinit__( self ):
        self.logLR_table = kh_init_int64()

    def __dealloc__( self ):
        kh_destroy_int64(self.logLR_table)

    cpdef bint check_cache ( self, float x, float y ):
        """Check if the logLR of enrich:x background:y; has been
        calculated and cached.
         
        """
        cdef:
            khiter_t k                  # index got from get_init64 function
            long key_value

        key_value = hash( (x, y) )
        k = kh_get_int64( self.logLR_table, key_value )
        return k != self.logLR_table.n_buckets

    cpdef float get_logLR_diff ( self, float x, float y ):
        cdef:
            khiter_t k                  # index got in the table; translated from hash key
            int ret = 0
            float val
            long key_value              # hash key
        key_value = hash( (x, y) )
        k = kh_get_int64(self.logLR_table, key_value) # translate hash key to index 
        if k != self.logLR_table.n_buckets: #kh_exist_int64( self.pscore_table, k ):
            return self.logLR_table.vals[k]
        else:
            # calculate and cache
            if y > x: y, x = x, y
            if x == y:
                val = 0
            else:
                val = (x*(log10(x)-log10(y))+y-x)

            k = kh_put_int64( self.logLR_table, key_value, &ret )
            self.logLR_table.keys[ k ] = key_value
            self.logLR_table.vals[ k ] = val
            return val
