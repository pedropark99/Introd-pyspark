import re


def is_trunc_needed(lines, n_chars):
    ns = [len(line) > n_chars for line in lines]
    if any(ns):
        return True
    else:
        return False
    

def truncate_line(line, n_chars):
    truncated_text = list()
    current_line = line
    max_index = n_chars

    while True:
        if len(current_line) <= n_chars:
            truncated_text.append(current_line)
            break

        trunc_text = current_line[:max_index]
        truncated_text.append(trunc_text)
        current_line = current_line[max_index:]

    truncated_text = '\n'.join(truncated_text)
    return truncated_text
    


def print_big_text(text, n_chars = 80):
    lines = text.split('\n')
    if is_trunc_needed(lines, n_chars) == False:
        return text
    
    truncated_text = list()
    for line in lines:
        n = len(line)
        if n > n_chars:
            truncated_text.append(
                truncate_line(line, n_chars)
            )
        else:
            truncated_text.append(line)

    truncated_text = '\n'.join(truncated_text)
    return truncated_text

    
test_text = '''Py4JError: An error occurred while calling o216.and. Trace:
py4j.Py4JException: Method and([class java.lang.Integer]) does not exist
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaat py4j.reflection.ReflectionEngine.getMethod(ReflectionEngine.java:318)
at py4j.reflection.ReflectionEngine.getMethod(ReflectionEngine.java:326)
at py4j.Gateway.invoke(Gateway.java:274)
at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
at py4j.commands.CallCommand.execute(CallCommand.java:79)
at py4j.ClientServerConnection.waitForCommands(ClientServerConnection.java:182)
at py4j.ClientServerConnection.run(ClientServerConnection.java:106)
at java.base/java.lang.Thread.run(Thread.java:829)'''

# t = print_big_text(test_text)
# print(t)