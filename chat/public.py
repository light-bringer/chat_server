import user
import messages


users = user.Users()
a = users.add_user('A')
b = users.add_user('B')
c = users.add_user('C')
d = users.add_user('D')
e = users.add_user('E')

group = messages.Groups()
group.add_group('A_B', [a, b])
group.add_group('B_C', [b, c])
group.add_group('C_D', [c, d])
group.add_group('A_C_E', [a, c, e])


from flask import Flask, redirect, url_for, request, Response, jsonify
app = Flask(__name__)


@app.route('/groups', methods=['GET'])
def get_all_groups(user_id: int=None):
    """
    getAllRecievers(user) -> /groups  GET Header: user_id -> [receivers]
    :param user_id:
    :return:
    """
    user_id = request.headers.get('user_id')
    if not user_id:
        return Response(status=400)

    user_id = int(user_id)
    data = group.get_groups_joined(user_id)
    json_response = {'groups': data}
    return jsonify(json_response)


def send_message(user_id: int, message_body: str, group_id: int):
    status = group.send_message(group_id=group_id, sender_id=user_id, body=message_body)
    if not status:
        print('cound not send message')
    else:
        print('message sent successfully')


@app.route('/conversation', methods=['GET'])
def get_messages(user_id=None, group_id=None):
    """
    getMessages(sender, reciever) -> /conversation?group_id=[group_id] Header: user_id -> [Messages(ordered by timestamp)]

    :param user_id:
    :param group_id:
    :return:
    """
    user_id = request.headers.get('user_id')
    group_id = request.args.get('group_id')
    if not user_id or not group_id:
        return Response(status=400)

    user_id = int(user_id)
    group_id = int(group_id)

    print(f'group{group_id}, user_id {user_id}\n')
    res = group.get_conversation(user_id, group_id)
    if res == None:
        print('cannot retrieve messages')
        return Response(status=403)
    res = [str(r) for r in res]
    data = {'conversations': res}
    return jsonify(data)


# print(get_all_groups(a))
# print(get_all_groups(b))
# print(get_all_groups(c))
# print(get_all_groups(d))
# print(get_all_groups(e))

# print(get_messages(a, 1))
print(send_message(a, 'Hi', 1))
print(send_message(b, 'Hello', 1))
print(send_message(b, 'Hi', 2))
print(send_message(c, 'Hello!', 2))
# print(get_messages(a, 1))
# print(get_messages(b, 2))
# print(get_messages(b, 1))



if __name__ == '__main__':
   app.run(debug = True)