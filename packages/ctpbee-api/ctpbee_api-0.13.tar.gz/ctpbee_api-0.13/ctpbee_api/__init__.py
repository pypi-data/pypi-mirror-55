
__version__ = "0.1"
from ctpbee_api.ctp import MdApi,MdApiApp,TdApi,TdApiApp


def get_interface(interface_name):
    if interface_name == "ctp":
        return (MdApi, TdApi)
    
    elif interface_name == "ctp_se":
        return (MdApiApp, TdApiApp)

    else:
        raise ValueError(f"{interface_name} are not supported by ctpbee_api")
    