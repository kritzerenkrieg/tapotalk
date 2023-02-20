# napodoba javovskejch fcí system.ArrayCopy() a ArraysCopyOf()


def jakobyArrayCopy(
    src_arr: list, src_pos: int, dest_arr: list, dest_pos: int, length: int
) -> None:
    # nemužem nahradit trikem s vodkazama/referencí
    # dest_arr_ = dest_arr[:dest_pos] +src_arr[src_pos:src_pos + length] + dest_arr[dest_pos + length:]
    for i in range(length):
        dest_arr[dest_pos + i] = src_arr[src_pos + i]


def jakobyUtilArraysCopyOf(original: list, new_len: int) -> list:
    # mužeme nahradit trikem s vodkazama/referencí
    if new_len <= len(original):
        return original[:new_len]
    else:
        return original[:] + ([0] * (new_len - len(original)))


# manualní hlídání overflow/přetečení proměnejch který byly puvodně
# v nějakým javovským datovým typu
# hooooodně se s tim v puvodním javovským zdrojačku čarovalo pro
# optimimizalilaci kodu, pro nás je to boužel teďko nevyhoda
# a navopak nas to počitaci víkon stojí :O :/


def jakoby_byte_overflow(byte):
    if byte > 127:
        return byte - (2 * 128)
    elif byte < -128:
        return byte + (2 * 128)
    else:
        return byte


def jakoby_short_overflow(short):
    if short > 32767:
        return short - (2 * 32768)
    elif short < -32768:
        return short + (2 * 32768)
    else:
        return short


# zbejvajicí int a long nejspíš nejsou nutný ale kdo ví :D
def jakoby_int_overflow(int_):
    if int_ > 2147483647:
        return int_ - (2 * 2147483648)
    elif int_ < -2147483648:
        return int_ + (2 * 2147483648)
    else:
        return int_


def jakoby_long_overflow(long_):
    if long_ > 9223372036854775807:
        return long_ - (2 * 9223372036854775808)
    elif long_ < -9223372036854775808:
        return long_ + (2 * 9223372036854775808)
    else:
        return long_
