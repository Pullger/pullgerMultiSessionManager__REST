import logging
# class excPullger(ABC):
#     pass

loggerName = 'pullgerMultisessionManager'
logger = logging.getLogger(loggerName)

class excMultisessionManager(BaseException):
    """ test discription in 0"""
    def __init__(self, message, **kwargs):
        """ test discription in 0 init"""
        super().__init__(message)
        # Logger initialization
        if 'loggerName' in kwargs:
            logger = logging.getLogger(kwargs['loggerName'])
        # Write internal error discription
        if 'exeptation' in kwargs:
            logMessage = f"{message} Internal discription: [{str(kwargs['exeptation'])}]"
        else:
            logMessage = message
        # Logger level
        if 'level' in kwargs and type(kwargs['level']) == int:
            logger.log(kwargs['level'], logMessage)
        else:
            logger.critical(logMessage)
        pass