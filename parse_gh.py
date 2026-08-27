import json
import re

with open('/home/vscode/.vscode-remote/data/User/workspaceStorage/-200f389f/GitHub.copilot-chat/chat-session-resources/a5228055-f7c2-4678-ad29-a5352a08eaef/call_MHxsSkU3Z3ppQ25SREVZalBEVzc__vscode-1787829660807/content.txt') as f:
    text = f.read()

objs = re.split(r'\n\}\n|\n\]\n', text)
for i, obj in enumerate(objs):
    obj = obj.strip()
    if not obj:
        continue
    if obj.startswith('{'):
        if not obj.endswith('}'):
            obj += '\n}'
    elif obj.startswith('['):
        if not obj.endswith(']'):
            obj += '\n]'
    try:
        parsed = json.loads(obj)
        if isinstance(parsed, dict) and 'comments' in parsed:
            print('--- COMMENTS ---')
            for c in parsed['comments']:
                print(f"Author: {c['author']['login']} | Created: {c.get('createdAt')} | Body snippet: {c['body'][:200].replace(chr(10), ' ')}")
        elif isinstance(parsed, list):
            if len(parsed) > 0 and 'number' in parsed[0]:
                print('--- PRS ---')
                for pr in parsed:
                    print(f"PR #{pr['number']}: {pr['title']} ({pr['state']}) base={pr['baseRefName']} head={pr['headRefName']} merged={pr['mergedAt']}")
            elif len(parsed) > 0 and 'conclusion' in parsed[0]:
                print('--- RUNS ---')
                for run in parsed[:15]:
                    print(f"Workflow Run: {run['name']} event={run['event']} branch={run['headBranch']} status={run['status']} conclusion={run['conclusion']} url={run['url']}")
    except Exception as e:
        pass
