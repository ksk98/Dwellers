from network import utility
import socket


def communicate_and_get_answer(concrete_socket: socket.socket, header_args: list, body_content: str) -> str:
    out_message = ""
    try:
        # Compose header
        for harg in header_args:
            out_message += harg + "\r\n"
        out_message += "\r\n"

        # Add content if not empty
        if body_content != "":
            out_message += body_content + "\r\n\r\n"

        # TODO: Encrypt content

        # Send header + content
        concrete_socket.sendall(out_message.encode("utf-8"))

        # Get response header
        in_message = utility.get_data(concrete_socket)

        # If response contains content then read it
        resp_content_length = utility.get_content_length_from_header(in_message)
        if resp_content_length != 0:
            in_message = in_message + utility.get_specific_amount_of_data(concrete_socket, resp_content_length)

        # TODO: Decrypt content

        # Give back the answer to the caller
        return in_message

    except socket.error as e:
        print(e)
        return "error"
