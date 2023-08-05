#!/usr/bin/env python
# coding: utf-8

# # Arduino SCPI Controller
# Communicates with an arduino using SCPI commands

# ## API
# 
# 
# **is_connected():** Returns if the port is open.
# 
# **connect():** Opens the port.
# 
# **disconnect():** Closes the port.
# 
# **write( msg ):** Writes a message to the controller.
# 
# **read():** Reads a message until the read termination character and returns it.
# 
# **query( msg ):** Writes the given command and returns the response.

# In[1]:


import serial
import logging


# In[2]:


class Property( object ):
        """
        Represents a scpi property of the instrument 
        """
        
        #--- static variables ---
        ON  = 'ON'
        OFF = 'OFF'
        
        
        #--- class methods ---
        
        def __init__( self, inst, name ):
            self.__inst = inst # the instrument
            self.name = name.upper()

            
        def __getattr__( self, name ):
            return Property( 
                self.__inst, 
                ':'.join( ( self.name, name.upper() ) ) 
            )

        
        def __call__( self, value = None ):
            if value is None:
                # get property
                return self.__inst.query( self.name + '?')
                
            else:
                # set value
                if not isinstance( value, str ):
                    # try to convert value to string
                    value = str( value )
                    
                return self.__inst.write( self.name + ' ' + value )
        
        
        #--- static methods ---
        
        @staticmethod
        def val2bool( val ):
            """
            Converts standard input to boolean values

            True:  'on',  '1', 1, True
            False: 'off', '0', 0, False
            """
            if isinstance( val, str ):
                # parse string input
                val = val.lower()

                if val == 'on' or val == '1':
                    return True

                elif val == 'off' or val == '0':
                    return False

                else:
                    raise ValueError( 'Invalid input' )

            return bool( val )
    
    
        @staticmethod
        def val2state( val ):
            """
            Converts standard input to scpi state

            ON:  True,  '1', 1, 'on',  'ON'
            OFF: False, '0', 0, 'off', 'OFF'
            """
            state = Property.val2bool( val )
            if state:
                return 'ON'

            else:
                return 'OFF'


# In[61]:


class Arduino_SCPI_Instrument:
    """
    Represents an arduino SCPI instrument.
    """
    
    def __init__( 
        self, 
        port, 
        read_termination  = '\n',
        write_termination = '\n',
        io_attempts = 1,
        **serial_args        
    ):
        """
        :param port: The communication port.
        :param read_termination: The read termination charater for replies.
            [Default: b'\n']
        :param write_termination: The write termination charater for commands.
            [Default: b'\n']
        :param io_attempts: The number of times to try a communication if an error is raised.
            [Default: 1]
        :param serial_args: Keyword arguments to pass to the serial resource.
            Sets default timeout paramter to 2 seconds, if not included.
        """
        self.__encoding = 'utf-8'
        
        self.__port = port
        self.__read_termination = bytes( read_termination, self.__encoding )
        self.__write_termination = write_termination
        
        if ( not isinstance( io_attempts, int ) ) or ( io_attempts < 1 ):
            raise ValueError( 'io_attempts must be an integer larger than 0.')
        
        self.io_attempts = io_attempts
        
        if 'timeout' not in serial_args:
            # default timout
            serial_args[ 'timeout' ] = 2
            
        self.__serial_args = serial_args
        
        self.__inst = serial.Serial()
        
        
    def __del__( self ):
        """
        Ensures the communication port is closed before deletion.
        """
        if self.connected:
            self.disconnect()
            
        del self.__inst
        self.__inst = None
        
        
    def __getattr__( self, name ):
        return Property( self, name )
        
        
    @property
    def port( self ):
        return self.__port
    
    @port.setter
    def port( self, port ):
        """
        :raises RuntimeError: If the port is open.
        """
        if self.is_connected():
            raise RuntimeError( "Can not change port while connected" )
            
        self.__port = port
        self.__inst.port = port
        
        
    @property
    def read_termination( self ):
        return self.__read_termination
    
    
    @property
    def write_termination( self ):
        return self.__write_termination
    
        
    @property
    def serial_args( self ):
        return self.__serial_args
    
        
    @property    
    def connected( self ):
        """
        :returns: True is the port is open, otherwise False.
        """
        if not self.__inst:
            return False
        
        return self.__inst.is_open
    
    
    @property
    def id( self ):
        """
        Returns the id of the connected instrument.
        """
        return self.query( '*IDN?' )
    
    
    def connect( self ):
        """
        Opens the port for communication with the set parameters.
        
        :raises RuntimeError: If the port is already open.
        """
        if self.__inst.is_open:
            raise RuntimeError( 'Already connected' )
            
        self.__inst.port = self.port
        for param, val in self.__serial_args.items():
            setattr( self.__inst, param, val )
            
        self.__inst.open()
        
        
    def disconnect( self ):
        self.__inst.close()
    
    
    def write( self, msg ):
        """
        Sends a command to the instrument.
        
        :param msg: The message to send.
        """
        msg += self.__write_termination
        msg = bytes( msg, self.__encoding )
        
        self.__attempt( lambda: self.__inst.write( msg ) )
        
        logging.debug( msg )
            
            
    def read( self ):
        """
        Reads the response from the arduino.
        
        :returns: The response, read until the read terminator.
        :raises TimeoutError: If the data read times out
        """
        return self.__attempt( self.__read )
    
    
    def query( self, msg ):
        """
        Queries a commad.
        
        :param msg: The command to send run.
        :returns: The command response.
        """
        def q():
            self.__write( msg )
            return self.__read()
        
        return self.__attempt( q )
    
    
    #--- helper methods ---
    
    def __attempt( self, func ):
        attempts = 0
        while attempts <= self.io_attempts:
            try:
                attempts += 1
                resp = func()
                break
                
            except Exception as err:                
                if attempts >= self.io_attempts:
                    # number of attempts exceeded
                    raise err
        
        # successful call
        return resp
                              

    def __read( self ):
        """
        (Used to manage attempts)
        Reads the response from the arduino.
        
        :returns: The response, read until the read terminator.
        :raises TimeoutError: If the data read times out
        """
        resp = self.__inst.read_until( self.__read_termination )
        logging.debug( resp )

        # check successful read by comparing termination
        termination = resp[ - len( self.__read_termination ) : ]

        if termination != self.__read_termination:
            raise TimeoutError( 'Failed to read response.' )

        resp = resp.replace( self.__read_termination, b'' )
        return resp.decode( self.__encoding )
                              
                              
    def __write( self, msg ):
        """
        (Used to manage attempts)
        Sends a command to the instrument.
        
        :param msg: The message to send.
        """
        msg += self.__write_termination
        msg = bytes( msg, self.__encoding )
        
        self.__inst.write( msg )
        
        logging.debug( msg )


# # Work

# In[62]:


# ar = Arduino_SCPI_Instrument( 
#     'COM8', 
#     read_termination = '\n\r', 
#     baudrate = 115200,
#     timeout = 5,
#     io_attempts = 2
# )


# In[63]:


# ar.connect()


# In[67]:


# ar.disconnect()
# del ar


# In[66]:


# ar.query( ':CHAN:MODE ?')


# In[65]:


# ar.query( ':CHAN:SELE 7')


# In[ ]:




