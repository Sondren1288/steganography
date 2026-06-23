from PIL import Image
from PIL.ImageFile import ImageFile
from math import floor

ENCODE_RGB = 0
SPAN = 8
STOPWORD = "T T T T T"


def load_image(impath: str) -> ImageFile:
    # TODO validate string and such I guess
    try:
        im = Image.open(impath)
    except Exception as e:
        print(f"No such thing as: {impath}. \nReturned error: {e}")
        raise e
    return im


def bitflip(num: int) -> int:
    # Flips the last bit in an integer
    return num ^ 1

def set_even(num: int) -> int:
    # Sets the last digit even
    if num & 1:
        return bitflip(num)

    return num

def set_odd(num: int) -> int:
    # Sets the last digit odd
    if num & 1:
        return num

    return bitflip(num)

def decode_message(msg: list[str]) -> str:
    # group into SPAN

    list_of_nums = []
    end_reached = False
    iterator = 0
    while not end_reached:
        group = []

        for _ in range(0, SPAN):
            try:
                # Turn to string as well
                group.append(str(msg[iterator]))
            except IndexError:
                end_reached = True
                break
            iterator += 1

        if len(group) == 0:
            break

        group_as_num = int("".join(group), 2)
        list_of_nums.append(group_as_num)

    message = [chr(c) for c in list_of_nums]
    return "".join(message)

def encode_message(msg: str) -> list[str]:
    # Validate string is encodeable.
    # 
    # if num & 1 -> isOdd
    # else -> isEven
    # Encode char
    # ord('h') -> 104
    # chr(104) -> 'h'

    # Turn string into list, and apply ord
    ord_str = [ord(c) for c in msg]
    
    list_of_bin = []
    for l in ord_str:
        # Remove the '0b' in front
        list_of_bin.append(str(bin(l)[2:]).zfill(SPAN))

    return list_of_bin

def write_message(msg: str, image: ImageFile):
    # Can use int('0b11', 2), or int('11', 2) to get 3 (dec)
    msg += STOPWORD
    bin_list = encode_message(msg)


    for stride, char in enumerate(bin_list):
        for pos, bit in enumerate(char):
            # SPAN bits for each char
            x = (stride * SPAN + pos) % image.width
            y = floor((stride * SPAN + pos) / image.width)

            pxl = image.getpixel((x,y))
            if (not pxl):
                raise IndexError (f"Index with {x},{y} is not valid on image with width {image.width}")
            # Assume pxl of tuple type
            color_bit = pxl[ENCODE_RGB]
            if bit == "1":
                encoded_bit = set_odd(color_bit)
            else: 
                encoded_bit = set_even(color_bit)

            new_pxl = list(pxl)
            new_pxl[ENCODE_RGB] = encoded_bit
            new_pxl = tuple(new_pxl)
            image.putpixel((x, y), new_pxl)

    image.show()
    return image

def read_message(image: ImageFile):
    # TODO make message readable from wherever
    # Currently assumes message starts at 0 0

    # Read SPAN bits at a time, decode, and inspect.
    # If ends with STOPWORD, stop
    cur_x = 0
    cur_y = 0
    end_of_message = False
    message = []
    while not end_of_message:
        intermediary = []
        # read SPAN bits
        for _ in range(0, SPAN):
            pxl = image.getpixel((cur_x, cur_y))
            # Get the last digit of the binary
            intermediary.append(pxl[ENCODE_RGB] & 0b1)

            # Increment safely
            cur_x += 1
            if (cur_x >= image.width):
                cur_y += 1
                cur_x  = 0
        message.append(decode_message(intermediary))

        if "".join(message).endswith(STOPWORD):
            end_of_message = True

    return "".join(message)



def main():
    hardcoded_path = "../tester.jpg"
    im = load_image(hardcoded_path)
    msg_list = encode_message("apple")
    #message = "apple".join([str(x) for x in range(1,1000)])
    message = "I want to know if robots dream of electric sheep"
    encoded = write_message(message, im)
    print("msg len:", len(message))
    print("width:", im.width)
    print(read_message(encoded))

    pass

if __name__ == '__main__':
    main()
