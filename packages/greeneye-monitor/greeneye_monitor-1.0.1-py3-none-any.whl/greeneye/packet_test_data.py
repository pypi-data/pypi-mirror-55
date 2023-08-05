import datetime
from io import StringIO
import os

greeneye_dir = os.path.dirname(os.path.abspath(__file__))
greeneye_data_dir = os.path.join(greeneye_dir, 'data')

PACKETS = {
    'BIN32-ABS.bin': {
        "absolute_watt_seconds": [3123664, 9249700, 195388151, 100917236,
                                  7139112, 1440, 4, 3, 14645520, 111396601,
                                  33259670, 38296448, 1108415, 2184858,
                                  5191049, 1, 71032651, 60190845, 47638292,
                                  12017483, 36186563, 14681918, 69832947,
                                  37693, 60941899, 1685614, 902, 799182,
                                  302590, 3190972, 5, 647375119],
        "currents": [0.42, 0.44, 3.86, 0.4, 0.14, 0.0,
                     0.0, 0.0, 0.78, 1.82,
                     1.56, 0.26, 0.38, 0.08, 0.16, 0.0,
                     1.66, 0.68, 0.18,
                     0.12, 1.92, 0.74, 0.2, 0.12, 1.12,
                     0.1, 0.08, 0.4, 0.08,
                     0.18, 0.0, 14.42],
        "pulse_counts": [0, 0, 0, 0],
        "seconds": 997492,
        "serial_number": 603,
        "device_id": 11,
        "temperatures": [
            512,
            0,
            0,
            0,
            0,
            0,
            0,
            0],
        "voltage": 121.1},
    "BIN32-NET.bin": {
        "absolute_watt_seconds": [3123588, 9249122, 195352930, 100916608,
                                  7139048, 1440, 4, 3, 14639320, 111380602,
                                  33246631, 38295282, 1108344, 2184716,
                                  5190974, 1, 71017653, 60184900, 47637526,
                                  12017481, 36168994, 14675409, 69832510,
                                  37693, 60935828, 1685539, 902, 799127,
                                  302590, 3190447, 5, 647245834],
        "currents": [0.42, 0.44, 3.88, 0.46, 0.14, 0.0, 0.0,
                     0.0, 0.78, 1.84,
                     1.56, 0.26, 0.38, 0.08, 0.16, 0.0,
                     1.66, 0.68, 0.16,
                     0.12, 1.9, 0.74, 0.2, 0.1, 1.14, 0.1,
                     0.08, 0.4, 0.1,
                     0.18, 0.0, 14.42],
        "polarized_watt_seconds": [0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0,
                                   0, 0, 0, 0,
                                   0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0,
                                   0, 0, 0, 0,
                                   0, 0, 0, 0],
        "pulse_counts": [
            0,
            0,
            0,
            0],
        "seconds": 997415,
        "serial_number": 603,
        "device_id": 11,
        "temperatures": [
            512,
            0,
            0,
            0,
            0,
            0,
            0,
            0],
        "voltage": 121.5
    },
    "BIN48-ABS.bin": {
        "absolute_watt_seconds": [3123507, 9248674, 195325612, 100916122,
                                  7139001, 1440, 4, 3, 14634511, 111368220,
                                  33236493, 38294375, 1108287, 2184600,
                                  5190920, 1, 71006014, 60180284, 47636927,
                                  12017481, 36155362, 14670370, 69832182,
                                  37692, 60930993, 1685472, 902, 799075,
                                  302590, 3190044, 5, 647145389, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "currents": [0.42, 0.44, 3.86, 0.4, 0.14, 0.0, 0.0,
                     0.0, 0.78, 1.8,
                     1.58, 0.26, 0.42, 0.08, 0.18, 0.0,
                     1.66, 0.68, 0.16,
                     0.12, 1.92, 0.74, 0.2, 0.1, 1.22, 0.1,
                     0.08, 0.36, 0.08,
                     0.18, 0.0, 14.42, 0.0, 0.0, 0.0, 0.0,
                     0.0, 0.0, 0.0, 0.0,
                     1230.0, 993.52, 127.88, 471.04, 0.08,
                     63.3, 314.88,
                     11.0],
        "pulse_counts": [0, 0, 0, 0],
        "seconds": 997354,
        "serial_number": 603,
        "device_id": 11,
        "temperatures": [
            512,
            0,
            0,
            0,
            0,
            0,
            0,
            0],
        "voltage": 121.3
    },
    "BIN48-NET.bin": {
        "absolute_watt_seconds": [3123490, 9248489, 195314519, 100915929,
                                  7138977, 1440, 4, 3, 14632552, 111363102,
                                  33232371, 38294008, 1108271, 2184558,
                                  5190900, 1, 71001276, 60178405, 47636683,
                                  12017480, 36149816, 14668312, 69832044,
                                  37692, 60928981, 1685452, 902, 799053,
                                  302590, 3189879, 5, 647104414, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "currents": [0.44, 0.44, 3.96, 0.46, 0.14, 0.0, 0.0,
                     0.0, 0.76, 1.84,
                     1.54, 0.26, 0.4, 0.08, 0.18, 0.0, 1.68,
                     0.68, 0.18, 0.12,
                     1.9, 0.72, 0.2, 0.1, 1.18, 0.12, 0.08,
                     0.4, 0.1, 0.18,
                     0.0, 14.5, 0.0, 0.0, 0.0, 0.0, 0.0,
                     0.0, 0.0, 0.0,
                     1230.0, 993.52, 127.88, 1290.24, 0.14,
                     64.7, 279.04,
                     11.3],
        "polarized_watt_seconds": [0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0,
                                   0, 0, 0, 0,
                                   0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0,
                                   0, 0, 0, 0,
                                   0, 0, 0, 0,
                                   893353787397,
                                   16779521, 0,
                                   3489681664,
                                   1048746,
                                   33554688,
                                   339315458048,
                                   2816,
                                   21480407271,
                                   1392508928, 1,
                                   117440512,
                                   68831281152,
                                   47446822415,
                                   25887770890,
                                   4328719365],
        "pulse_counts": [
            0,
            0,
            0,
            0],
        "seconds": 997327,
        "serial_number": 603,
        "device_id": 11,
        "temperatures": [
            512,
            0,
            0,
            0,
            0,
            0,
            0,
            0],
        "voltage": 121.3
    },
    "BIN48-NET-TIME.bin": {
        "absolute_watt_seconds": [2973101, 8059708, 156428334, 85168830,
                                  3701996, 1417, 4, 3, 10122331, 102754614,
                                  25349121, 23541326, 910505, 1899678,
                                  3136543, 1, 50182738, 46920840, 37015191,
                                  7826156, 19817953, 11755830, 61617610,
                                  35109, 51981008, 1519294, 760, 663522,
                                  229936, 2635054, 5, 451930676, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "currents": [0.42, 0.44, 1.36, 0.54, 0.1, 0.0, 0.0,
                     0.0, 0.22, 1.28,
                     0.92, 0.26, 0.4, 0.1, 0.84, 0.0, 3.02,
                     1.1, 0.16, 0.86,
                     0.08, 0.2, 0.22, 0.12, 1.16, 0.12,
                     0.08, 0.42, 0.08,
                     0.12, 0.0, 10.66, 0.0, 0.0, 0.0, 0.0,
                     0.0, 0.0, 0.0, 0.0,
                     1230.0, 993.52, 127.88, 302.08, 0.0,
                     53.76, 1052.16,
                     3.16],
        "polarized_watt_seconds": [0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0,
                                   0, 0, 0, 0,
                                   0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0,
                                   0, 0, 0, 0,
                                   0, 0, 0, 0,
                                   554051239936,
                                   4352, 0,
                                   2097152768,
                                   8590917732,
                                   1728053504,
                                   549779603456,
                                   1677724160,
                                   21474902016,
                                   1275068416, 0,
                                   50331648,
                                   68801396736,
                                   47446822415,
                                   25887770890,
                                   4328719365],
        "pulse_counts": [
            0,
            0,
            0,
            0],
        "seconds": 841707,
        "serial_number": 603,
        "device_id": 11,
        "temperatures": [
            512,
            0,
            0,
            0,
            0,
            0,
            0,
            0],
        "time_stamp": datetime.datetime(
            2017, 12, 20, 5, 7, 26),
        "voltage": 121.7
    },
    "BIN48-NET-TIME_tricky.bin": {
        "absolute_watt_seconds": [231291827, 375937488, 2000191302, 884282444,
                                  217533987, 26818, 83, 64, 235203561,
                                  660892780, 516638549, 590071215, 16739113,
                                  46163811, 120489725, 22, 651996464,
                                  1115855892, 443956599, 187609729, 418355582,
                                  186555196, 553111232, 1396693, 868815981,
                                  27838920, 2307787, 11390311, 9790746,
                                  48429661, 62, 11386703968, 0, 0, 0, 0, 0, 0,
                                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "currents": [0.36, 0.3, 1.5, 0.34, 0.08, 0.0, 0.0,
                     0.0, 0.32, 0.76,
                     0.9, 0.28, 0.36, 0.08, 0.14, 0.0, 0.2,
                     1.54, 0.18, 0.1,
                     0.18, 0.16, 0.2, 0.08, 1.7, 0.08, 0.0,
                     0.3, 0.08, 0.12,
                     0.0, 7.32, 0.0, 0.0, 0.0, 0.0, 0.0,
                     0.0, 0.0, 0.0,
                     1230.0, 993.52, 127.88, 250.88, 655.52,
                     41.28, 384.0,
                     659.16],
        "polarized_watt_seconds": [0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0,
                                   0, 0, 0, 0,
                                   0, 0, 0, 0, 0,
                                   0, 0, 0, 0, 0,
                                   0, 0, 0, 0,
                                   0, 0, 0, 0,
                                   665720258565,
                                   0, 0,
                                   1375737600,
                                   4296278116,
                                   256,
                                   790274048000,
                                   2816,
                                   25769803791,
                                   2667577600, 0,
                                   67108864,
                                   68773347328,
                                   47446822415,
                                   25887770890,
                                   4328719365],
        "pulse_counts": [
            0,
            0,
            0,
            0],
        "seconds": 11988815,
        "serial_number": 603,
        "device_id": 11,
        "temperatures": [
            512,
            0,
            0,
            0,
            0,
            0,
            0,
            0],
        "time_stamp": datetime.datetime(
            2018, 6, 11, 21, 16, 58),
        "voltage": 122.2
    }
}


def read_packets(packet_file_names):
    result = bytearray()
    for packet_file_name in packet_file_names:
        result.extend(read_packet(packet_file_name))

    return bytes(result)


def read_packet(packet_file_name):
    with open(os.path.join(greeneye_data_dir, packet_file_name),
              'rb') as data_file:
        return data_file.read()


def assert_packet(packet_file_name, parsed_packet):
    expected_packet = PACKETS[packet_file_name]

    expected = StringIO()
    actual = StringIO()

    for key, expected_value in sorted(expected_packet.items(), key=lambda x: x[0]):
        actual_value = getattr(parsed_packet, key)
        if expected_value != actual_value:
            expected.write('{key}={expected},\n'.format(
                key=key,
                expected=repr(expected_value)))
            actual.write('{key}={actual},\n'.format(
                key=key,
                actual=repr(actual_value)))

    if expected.getvalue() != '':
        raise AssertionError('''
    Some packet fields did not match.
    Expected:
    {expected}
    Actual:
    {actual}'''.format(expected=expected.getvalue(), actual=actual.getvalue()))
