import dialogflow
from google.api_core.exceptions import InvalidArgument
from google.oauth2 import service_account

#設定dialogflow初始化
DIALOGFLOW_PROJECT_ID = 'library-agent-yvtpud' 
DIALOGFLOW_LANGUAGE_CODE = 'Chinese (Traditional) — zh-TW'
GOOGLE_APPLICATION_CREDENTIALS = service_account.Credentials.from_service_account_file('library-agent-yvtpud-eee9b54c8a39.json')
SESSION_ID = 'eee9b54c8a3977ad387cf39e7b4e6c1bbe9351ca' #金鑰

#create a session client
session_client = dialogflow.SessionsClient(credentials=GOOGLE_APPLICATION_CREDENTIALS)
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

def dialogflow_library_agent(t):       
        #print("client>>",end="")
    text_to_be_analyzed = t #輸入的文字
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
        #print("chatbot>>", response.query_result.fulfillment_text) #輸出的文字
  
    return response.query_result.fulfillment_text , response.query_result.intent.display_name

'''
#輸入字串
print("輸入:")
text_to_be_analyzed = input() 

text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
query_input = dialogflow.types.QueryInput(text=text_input)

try:
    response = session_client.detect_intent(session=session, query_input=query_input)
except InvalidArgument:
    raise

print("Query text:", response.query_result.query_text)
print("Detected intent:", response.query_result.intent.display_name)
print("Detected intent confidence:", response.query_result.intent_detection_confidence)
print("Fulfillment text:", response.query_result.fulfillment_text)
'''