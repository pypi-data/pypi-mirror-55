from flask import request
from google.cloud import kms_v1
import base64


def run():


  action = request.values.get("action");
  data = request.values.get("data");

  project_id = os.environ.get('CLOUD_KMS_PROJECT')
  location_id = os.environ.get('CLOUD_KMS_LOCATION')
  key_ring_id = os.environ.get('CLOUD_KMS_KEYRING') 
  crypto_key_id = os.environ.get('CLOUD_KMS_KEY')

  client = kms_v1.KeyManagementServiceClient()
  name = client.crypto_key_path_path(project_id, location_id, key_ring_id,
                                     crypto_key_id)
  out = ""
  if action == "encrypt":
    encr = client.encrypt(name, data.encode("utf-8")).ciphertext
    out = base64.b64encode(encr).decode("utf-8")
  elif action == "decrypt":
    out = client.decrypt(name, base64.b64decode(data)).plaintext.decode("utf-8")
  else:
    out = """
  Source (Secret or encoded base64):
<FORM name=form1 method=POST target='out' action='/kms'>
  <INPUT NAME='action' TYPE='HIDDEN'>
  <TEXTAREA name='data' style='width:800px;height:300px'></TEXTAREA>
  <BR/>
  <INPUT VALUE='Encode' type=button onclick='encrypt()'>
  <INPUT VALUE='Decode' type=button onclick='decrypt()'>
</FORM>
<BR/>
Encoded base64
<BR/>
<IFRAME name='out' style='width:800px;height:300px'></IFRAME>
<script>
function encrypt() {
  document.form1.action.value='encrypt';
  document.form1.submit();
}
function decrypt(){
  document.form1.action.value='decrypt';
  document.form1.submit();
}
</script>
  """

  return out 
