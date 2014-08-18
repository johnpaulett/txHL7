from hl7 import parse

_ACK_TEMPLATE = u'MSH|^~\\&|{send_app}|{send_fac}|{recv_app}|{recv_fac}|{dttm}||ACK^001|{msgid}|P|{version}\rMSA|{ack_code}|{msgid}'


def ACK(original_message, ack_code='AA'):
    """
    Build a basic ACK message

    ``ack_code`` options are one of `AA` (accept), `AR` (reject), `AE` (error)
    (2.15.8)

    .. warning:

        Does not currently conform to spec (2.9.2).

        -
        -

    """
    # hl7.parse requires the message is unicode already or can be easily
    # converted via unicode()
    msh = parse(original_message).segment('MSH')

    # easy-access function to make sure unicode is always called
    def m(element):
        return unicode(msh[element])

    # TODO actually build the message instead of using string interpolation
    return _ACK_TEMPLATE.format(
        # switch the sending & receiving
        # TODO allow customization
        send_app=m(5),
        send_fac=m(6),
        recv_app=m(3),
        recv_fac=m(4),

        dttm=m(7),
        msgid=m(10),
        version=m(12),
        ack_code=ack_code,
    )
