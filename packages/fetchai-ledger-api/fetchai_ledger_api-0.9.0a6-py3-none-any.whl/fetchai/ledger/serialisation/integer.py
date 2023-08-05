import io


def _calculate_log2_num_bytes(value: int) -> int:
    """
    Determine the number of bytes required to encode the input value.

    Artificially limited to max of 8 bytes to be compliant

    :param value:
    :return: The calculate the number of bytes
    """
    for log2_num_bytes in range(4):
        limit = 1 << ((1 << log2_num_bytes) * 8)
        if value < limit:
            return log2_num_bytes
    raise RuntimeError('Unable to calculate the number of bytes required for this value')


def decode(stream: io.BytesIO) -> int:
    """
    Decode an integer from the provided stream

    :param stream: The stream to parse
    :return: The decoded integer value
    """
    header = stream.read(1)[0]
    if (header & 0x80) == 0:
        return header & 0x7F
    else:
        type = (header & 0x60) >> 5
        if type == 3:
            return -(header & 0x1f)
        elif type == 2:
            signed_flag = bool(header & 0x10)
            log2_value_length = header & 0x0F
            value_length = 1 << log2_value_length

            value = 0
            for n in range(value_length):
                byte_value = int(stream.read(1)[0])
                shift = (value_length - (n + 1)) * 8

                byte_value <<= shift
                value |= byte_value

            if signed_flag:
                value = -value

            return value


def encode(stream: io.BytesIO, value: int):
    """
    Encode a integer value into a bytes stream

    :param value: The value to be encoded
    :return: The generated byets
    """
    is_signed = value < 0
    abs_value = abs(value)

    if not is_signed and abs_value <= 0x7f:
        stream.write(bytes([abs_value]))
    else:
        if is_signed and abs_value <= 0x1F:
            stream.write(bytes([0xE0 | abs_value]))
        else:

            # determine the number of bytes that will be needed to encode this value
            log2_num_bytes = _calculate_log2_num_bytes(abs_value)
            num_bytes = 1 << log2_num_bytes

            # define the header
            if is_signed:
                header = 0xD0 | (log2_num_bytes & 0xF)
            else:
                header = 0xC0 | (log2_num_bytes & 0xF)

            # encode all the parts fot the values
            values = [(abs_value >> (n * 8)) & 0xFF for n in reversed(range(num_bytes))]

            stream.write(bytes([header] + values))
