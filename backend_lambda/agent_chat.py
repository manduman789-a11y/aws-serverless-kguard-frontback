import json
import boto3

# AWS Bedrock 클라이언트 연결
bedrock = boto3.client(service_name='bedrock-agent-runtime', region_name='ap-northeast-2')

def lambda_handler(event, context):
    # 1. 프론트엔드에서 보낸 데이터 받기
    try:
        body = json.loads(event.get('body', '{}'))
        user_input = body.get('message')
        user_id = body.get('user_id', 'guest')
    except:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON'})
        }

    # 2. Bedrock 에이전트에게 질문 던지기
    try:
        response = bedrock.invoke_agent(
            agentId='KBFKAVMJRB',       # 사용자님 에이전트 ID
            agentAliasId='TSTALIASID',  # 별칭 ID
            sessionId=user_id,
            inputText=user_input
        )

        # 3. 답변 꺼내기
        completion = ""
        for event_stream in response.get('completion'):
            if 'chunk' in event_stream:
                completion += event_stream['chunk']['bytes'].decode('utf-8')

        # 4. 결과 반환 (CORS 헤더 필수!)
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # 모든 사이트에서 접속 허용
                'Access-Control-Allow-Methods': 'POST'
            },
            'body': json.dumps({'reply': completion})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
