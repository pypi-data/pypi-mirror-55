
import base64
import hmac
import hashlib
from .constants import DPS_ENDPOINT
from azure.iot.device import ProvisioningDeviceClient
 
def derive_device_key(device_id, master_symmetric_key):
    message = device_id.encode("utf-8")
    signing_key = base64.b64decode(master_symmetric_key.encode("utf-8"))
    signed_hmac = hmac.HMAC(signing_key, message, hashlib.sha256)
    device_key_encoded = base64.b64encode(signed_hmac.digest())
    return device_key_encoded.decode("utf-8")

def register_device(registration_id,id_scope,symmetric_key):
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
            provisioning_host=DPS_ENDPOINT,
            registration_id=registration_id,
            id_scope=id_scope,
            symmetric_key=symmetric_key,
    )

    return provisioning_device_client.register()
