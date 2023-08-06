// Server output to client textarea
eel.expose(addOutput);
function addOutput(line) {
    document.getElementById('log_output').value += line; // Add the line
    document.getElementById('log_output').scrollTop = document.getElementById('log_output').scrollHeight;
}